#######################################################################################################
# SDWAN Cloud Gateway configuration(Creation/Deletion) for private and public peer.
# CISCO device configuration for cloud peering.
# Input files : "CGW_CONFIG" folder under "csit/libraries" and "Devices.csv" file under "csit/Topology"
# Assumptions : Org and CPE on-boarding is done.
# Solution Supported : CGW SINGLE/DUAL solution.
# Sanity Checks : CPE LAN1-VRF route verification and ping test from CPE to Cloud peer loopback ips.
# Author : Sunita Martha(116616)
#######################################################################################################

import os, sys, json, yaml, re, itertools,time
from argparse import ArgumentParser, FileType
from jinja2 import meta, Environment, FileSystemLoader, StrictUndefined


if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# print fileDir
Par_Dir = os.path.dirname(fileDir)
# print Par_Dir
sys.path.append(Par_Dir)

from csit.libraries.VersaLib import VersaLib
from csit.libraries.CloudGatewayLib import  CloudGatewayLib


def get_vd_details():
    global cpe_list
    # ip = raw_input("Enter Versa Director IP address:\n")
    # print "Versa director IP:" + ip
    # ldap_user = raw_input("Enter LDAP Username for making SSH connection to VD:\n")
    # print "Versa director Username:" + ldap_user
    # ldap_passwd = getpass.getpass("Enter LDAP Password:\n")
    # user = raw_input("Enter Username for making REST actions to Versa Director :\n")
    # print "Versa director Username:" + user
    # passwd = getpass.getpass("Enter REST Password:\n")
    # cpe_user = raw_input("Enter Versa CPE Username:\n")
    # print "Versa CPE Username:" + cpe_user
    # cpe_passwd = getpass.getpass("Enter Versa CPE Password:\n")
    # node_user = raw_input("Enter Versa NODE devices Username:\n")
    # print "Versa NODE devices Username:" + node_user
    # node_passwd = getpass.getpass("Enter Versa NODE Password:\n")
    ip = '10.91.127.194'
    ldap_user = 'Automated'
    ldap_passwd = 'Auto@12345'
    user = 'Automated'
    passwd = 'Auto@12345'
    cpe_user = 'admin'
    cpe_passwd = 'versa123'
    node_user = 'admin'
    node_passwd = 'versa123'
    return {'mgmt_ip' : ip, 'username' : ldap_user,\
            'password' : ldap_passwd, 'GUIusername' : user, 'GUIpassword' : passwd}


def main():

    parser = ArgumentParser()
    parser.add_argument(
        '--action',
        '-a',
        help='action to be performed (CREATE or DELETE)',
        nargs='?')
    parser.add_argument(
        '--solution-type',
        '-s',
        help='cloud services subscribed (SINGLE or DUAL)',
        nargs='?')
    parser.add_argument(
        '--vars-file',
        '-i',
        help='vars files (YAML or JSON)',
        nargs='?')

    args = parser.parse_args()

    if args.vars_file:
        with open(fileDir + "\\libraries\\CGW_config\\" + args.vars_file) as fp1:
        #with open("C:\\NV_REPOSITORY\\csit\\libraries\\CGW_config\\" + args.vars_file) as fp1:
            input_data = yaml.safe_load(fp1)
        cpe_name = input_data["CPE_NAME"]

        csp_list = input_data["CSP_PEERINGS"]
        loopback_ip_list = []
        for peering in csp_list:
            loopback_ip_list.append(peering["LOOPBACK_IP"])

        CGW1_ESP_IP = input_data["CGW1_ESP_IP"]
        CGW2_ESP_IP = None
        if (args.solution_type == "DUAL"):
            CGW2_ESP_IP = input_data["CGW2_ESP_IP"]

    # pre-validation-1 : Verify tenant under test exists. If not, create a new tenant using available script.
    # pre-validation-2 : Verify CPE is available in VD. (CPE is successfully on-boarded for tenant under test) If not, on-board the CPE using available script.
    # pre-validation-3 : Verify WC and CGW devices are available and reachable from VD.

    obj = CloudGatewayLib()
    # step-1 : CGW command generation.
    command_result = obj.cloud_gateway_command_generation(args.action, args.solution_type)

    # step-2 : CGW device_list and command list segration.
    devices_list = obj.get_cgw_cmds(command_result)[0]
    commands_list = obj.get_cgw_cmds(command_result)[1]

    # step-3 : VD login.
    vd_dict = get_vd_details()
    vd_dict['device_type'] = 'versa_director'
    VD1 = VersaLib('Versa_director', **vd_dict)
    VD1.vdnc = VD1.login()

    # step-4 : CGW command execution from VD CLI.
    config_result = obj.cgw_config_from_vd_cli(VD1, VD1.vdnc, devices_list , commands_list)
    if (config_result == 0):
        print "CGW or WC device configuration failed for tenant under test."
        return

    # step-5 : VD logout.
    VD1.close(VD1.vdnc)

    # step-6 : CISCO device configuration.
    if(args.action == "CREATE"):
        cisco_result = obj.cloud_peer_create("cisco_device_details.yml", "cisco_creation.j2", args.solution_type)
        if (cisco_result == 0):
            print "CISCO device configuration for creation operation failed."
            return
    elif(args.action == "DELETE"):
        cisco_result = obj.cloud_peer_delete("cisco_device_details.yml", "cisco_deletion.j2", args.solution_type)
        if (cisco_result == 0):
            print "CISCO device configuration for deletion operation failed."
            return
    time.sleep(10)
    # step-7 : CPE LAN route verification.
    cpe_lan_result = obj.cpe_lan_route_verify(cpe_name, loopback_ip_list, args.solution_type, CGW1_ESP_IP, CGW2_ESP_IP=CGW2_ESP_IP)

    if((cpe_lan_result == len(loopback_ip_list)) and (args.action == "CREATE")):
        print "CGW loopback routes are available in CPE LAN1-VRF. Proceed to ping test."
    elif((cpe_lan_result == 0) and (args.action == "DELETE")):
        print "CGW loopback routes aren't available in CPE LAN1-VRF. Deletion is successful. Proceed to ping test."
    else:
        print "Availability of CGW loopback routes on CPE LAN1-VRF isn't as expected. \nTest failed : Check the logs."
        return

    # step-8 : Find CPE interface ip for LAN1-VRF.
    cpe_lan_ip = obj.get_cpe_lan_ip(cpe_name)
    if(cpe_lan_ip == ""):
        print "CPE interface ip for LAN1-VRF isn't found."
        return

    # Step-9 : Ping test to Cloud Peer Loopback IP.
    ping_test_result = obj.cpe_cgw_ping_test(cpe_name, loopback_ip_list, cpe_lan_ip)
    if((args.action == "CREATE") and (ping_test_result == len(loopback_ip_list))):
        print "Cloud Gateway New Tenant Creation is Successful."
    elif((args.action == "DELETE") and (ping_test_result == 0)):
        print "Cloud Gateway Tenant Deletion is Successful."
    else:
        print "Cloud Gateway Configuration Failed. \nTest case failed :  Check the Logs."

if __name__ == "__main__":
    main()