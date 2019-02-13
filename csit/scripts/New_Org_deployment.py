#!/usr/bin/env python
import sys
import os
import pandas as pd
import time
import getpass
from datetime import datetime

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# print fileDir
Par_Dir = os.path.dirname(fileDir)
# print Par_Dir
sys.path.append(Par_Dir)

from csit.libraries.VersaLib import VersaLib

def get_vd_details():
    # ip = raw_input("Enter Versa Director IP address:\n")
    # print "Versa director IP:" + ip
    # ldap_user = raw_input("Enter LDAP Username for making SSH connection to VD:\n")
    # print "Versa director ldap Username:" + ldap_user
    # ldap_passwd = getpass.getpass("Enter LDAP Password:\n")
    # user = raw_input("Enter VD GUI username:\n")
    # print "Versa director GUI Username:" + user
    # passwd = getpass.getpass("Enter VD GUI password::\n")
    ip = '10.91.116.35'
    ldap_user = 'admin'
    ldap_passwd = 'versa123'
    user = 'Sathish'
    passwd = 'Jan*1234'
    cpe_user = 'admin'
    cpe_passwd = 'versa123'
    node_user = 'admin'
    node_passwd = 'versa123'
    return {'mgmt_ip' : ip, 'username' : ldap_user,\
            'password' : ldap_passwd, 'GUIusername' : user, 'GUIpassword' : passwd}


def Do_New_Org_Deployment():
    # vd_dict = get_vd_details()
    # vd_dict['device_type'] = 'versa_director'
    # VD1 = VersaLib('Versa_director', **vd_dict)
    org_name = raw_input("Enter ORG NAME:")
    org_id = raw_input("Enter ORG ID :")
    no_of_vrfs = raw_input("NUMBER OF VRFS :")
    # org_name = "JAN232"
    # org_id = "232"
    # no_of_vrfs = "4"

    VD1 = VersaLib('VD1', topofile="Devices.csv")
    main_logger = VD1.main_logger
    main_logger.info("ORG NAME:" + org_name)
    run_result = ""
    print "AVAILBALE NODEs:" + str(VD1.ctlr_dict.keys())
    nodes = raw_input("Enter Node names. eg: MUM BLR\n")
    nodes = nodes.upper()
    # nodes = "BLR"
    WC_list = VD1.Create_Controller_List(org_name, org_id, no_of_vrfs, nodes)
    GW_list = VD1.Create_Gateway_List(org_name, org_id, no_of_vrfs, nodes)
    print WC_list
    print GW_list
    # print VD1.get_data_dict()
    # nc = VD1.login()
    # device_list = WC_list + GW_list
    # for device in device_list:
    #     result = VD1.request_sync_from_device(nc, device)
    #     print result
    result = VD1.Create_Org(org_name, org_id, WC_list, no_of_vrfs)
    run_result += "ORG DEPLOYMENT : " + result + "\n"
    if "FAIL" in run_result:
        main_logger.info("\n" + "*" * 20 + "\n" + "RESULT:" + "\n" + run_result + "\n" + "*" * 20 + "\n")
        exit()
    main_logger.info(result)
    for WC in WC_list:
        result = VD1.Config_Node_Devices(WC, "WC", nodes)
        run_result += WC + ": " + result + "\n"

    for GW in GW_list:
        result = VD1.Config_Node_Devices(GW, "GW", nodes, no_of_vrfs=no_of_vrfs)
        run_result += GW + ": " + result + "\n"

    main_logger.info("\n" + "*" * 20 + "\n" + "RESULT:" + "\n" + run_result + "\n"+ "*" * 20 + "\n")
    main_logger.info("LOG FILE PATH : " + VD1.logfile)

    # cpe1 = VersaLib('JAN18_CPE1_MUM', topofile="Devices.csv")
    # cpe1.create_PS_and_DG()
    # cpe1.pre_onboard_work()
    # cpe1.cpe_onboard_call()
    # cpe1_dev_info_on_vd = cpe1.get_device_info()
    # print cpe1_dev_info_on_vd
    # cpe2 = VersaLib('JAN18_CPE2_MUM', topofile="Devices.csv")
    # cpe2.pre_onboard_work()
    # cpe2.cpe_onboard_call()
    # cpe2_dev_info_on_vd = cpe1.get_device_info()
    # print cpe2_dev_info_on_vd


start_time = datetime.now()
Do_New_Org_Deployment()
print "Time elapsed: {}\n".format(datetime.now() - start_time)
