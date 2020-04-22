#!/usr/bin/env python
import sys
import os
import pandas as pd
import time
import getpass
from datetime import datetime
import pprint

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# print fileDir
Par_Dir = os.path.dirname(fileDir)
# print Par_Dir
sys.path.append(Par_Dir)

from csit.libraries.VersaLib import VersaLib


# from csit.libraries.HltapiLib import HltapiLib

def get_vd_details():
    # ip = raw_input("Enter Versa Director IP address:\n")
    # print "Versa director IP:" + ip
    # ldap_user = raw_input("Enter LDAP Username for making SSH connection to VD:\n")
    # print "Versa director ldap Username:" + ldap_user
    # ldap_passwd = getpass.getpass("Enter LDAP Password:\n")
    # user = raw_input("Enter VD GUI username:\n")
    # print "Versa director GUI Username:" + user
    # passwd = getpass.getpass("Enter VD GUI password::\n")
    ip = '10.91.127.194'
    ldap_user = 'Automated'
    ldap_passwd = 'Auto@12345'
    user = 'Automated'
    passwd = 'Auto@12345'
    # ip = '10.91.116.35'
    # ldap_user = 'admin'
    # ldap_passwd = 'versa123'
    # user = 'Sathish'
    # passwd = 'Jan*1234'
    # cpe_user = 'admin'
    # cpe_passwd = 'versa123'
    # node_user = 'admin'
    # node_passwd = 'versa123'
    return {'mgmt_ip': ip, 'username': ldap_user, \
            'password': ldap_passwd, 'GUIusername': user, 'GUIpassword': passwd}


def Do_Cpe_onboarding():
    # cpe_name = raw_input("Enter CPE NAME:").upper()
    # print "CPE NAME:" + cpe_name
    # spirent1 = HltapiLib("10.91.113.124", "10/1", "10/2")
    # spirent1.connect_and_reserve_ports()
    # spirent1.interface_config(spirent1.port_handle[0])
    # spirent1.interface_config(spirent1.port_handle[1])
    # device1 = spirent1.create_device(port=0, vlanid='600',
    #                        intf_ip_addr='192.169.101.3', gateway_ip_addr='192.169.101.1')
    # device2 = spirent1.create_device(port=1, vlanid='610',
    #                        intf_ip_addr='192.169.111.3', gateway_ip_addr='192.169.111.1')
    # src_dev_hdl = device1['handle'].split()[0]
    # dst_dev_hdl =  device2['handle'].split()[0]
    # src_dev_port_hdl = spirent1.port_handle[0]
    # dst_dev_port_hdl = spirent1.port_handle[1]
    # spirent1.release_ports()

    # spirent1.get_traffic_results(src_dev_port_hdl, dst_dev_port_hdl)

    cpe1_name = "CPE11-HKG-HYBRD-IPC00190"
    cpe2_name = "CPE12-HKG-HYBRD-IPC00190"
    vd1 = VersaLib('VD1', topofile="Devices.csv")
    cpe1 = VersaLib(cpe1_name, topofile="Devices.csv")
    cpe2 = VersaLib(cpe2_name, topofile="Devices.csv")

    vd1.login()
    main_logger = cpe1.main_logger
    main_logger.info("CPE NAME:" + cpe1_name)
    time.sleep(1)
    main_logger.info("SOLUTION SELECTED:" + cpe1.Solution_type)
    cpe1.Create_Node_Data(cpe1.STAGING_SERVER, "SS", wan=cpe1.STAGING_WAN)
    WC_list = cpe1.Create_Controller_List(cpe1.ORG_NAME, cpe1.ORG_ID, cpe1.NO_OF_VRFS, cpe1.NODE)
    GW_list = cpe1.Create_Gateway_List(cpe1.ORG_NAME, cpe1.ORG_ID, cpe1.NO_OF_VRFS, cpe1.NODE)
    cpe1.create_cpe_data()

    cpe2.Create_Node_Data(cpe2.STAGING_SERVER, "SS", wan=cpe1.STAGING_WAN)
    cpe2.Create_Controller_List(cpe2.ORG_NAME, cpe2.ORG_ID, cpe2.NO_OF_VRFS, cpe2.NODE)
    cpe2.Create_Gateway_List(cpe2.ORG_NAME, cpe2.ORG_ID, cpe2.NO_OF_VRFS, cpe2.NODE)
    cpe2.create_cpe_data()


    SLA_PRF_1 = "SLA10001yu"
    FWP1 = "FWP10001yu"
    IPADDOBJ = "srcip"
    SERVICE_OBJ = "tcp_src_port_2000_11yu"
    PLCYRULE = "ts_Destipaddr10001yu"

    # print vd1.move_policy_rule(cpe1.Device_name, cpe1.ORG_NAME, 'Default-Policy', PLCYRULE, 'first')
    # print vd1.config_devices_qos(cpe1.Device_name, cpe1.ORG_NAME, cpe1.WAN1_INTF)
    # print vd1.config_devices_qos(cpe2.Device_name, cpe2.ORG_NAME, cpe2.WAN1_INTF)
    cpe1.cross_login()
    print cpe1.req_clr_stats_cos_qos_plcy_all()
    print cpe1.show_cos_qos_policy_rules()


    # print vd1.config_devices_qos(cpe1.Device_name, cpe1.ORG_NAME, cpe1.WAN1_INTF)
    # cpe1.create_address_object(IPADDOBJ, "ipv4-prefix", cpe2.lan[1]['third_host']+"/32")
    print vd1.modify_qos_device_config(cpe1.Device_name, cpe1.ORG_NAME, 'qos_ip_based_premium.j2', src_address_obj=IPADDOBJ)
    print vd1.move_qos_policy_rule(cpe1.Device_name, cpe1.ORG_NAME, 'Default-Policy', 'LAN1-VRF-Premium', 'first')
    time.sleep(10)

    print vd1.modify_qos_device_config(cpe1.Device_name, cpe1.ORG_NAME, 'revert_qos_ip_based_premium.j2', src_address_obj=IPADDOBJ)
    print vd1.move_qos_policy_rule(cpe1.Device_name, cpe1.ORG_NAME, 'Default-Policy', 'LAN1-VRF-Premium', 'first')

start_time = datetime.now()
Do_Cpe_onboarding()
