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


def Do_Cpe_onboarding():
    # cpe_name = raw_input("Enter CPE NAME:").upper()
    # print "CPE NAME:" + cpe_name
    cpe_name = "CPE11-HKG-HYBRD-IPC00190"
    cpe = VersaLib(cpe_name, topofile="Devices.csv")
    main_logger = cpe.main_logger
    main_logger.info("CPE NAME:" + cpe_name)
    time.sleep(1)
    main_logger.info("SOLUTION SELECTED:" + cpe.Solution_type)
    cpe.Create_Node_Data(cpe.STAGING_SERVER, "SS", wan=cpe.STAGING_WAN)
    WC_list = cpe.Create_Controller_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    GW_list = cpe.Create_Gateway_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    cpe.create_cpe_data()
    ckt_pr_1_lcl_intf = "MPLS_WAN"
    ckt_pr_2_lcl_intf = "INT_WAN"
    cpe.create_fowarding_profile("NEW", ckt_pr_1_lcl_intf, ckt_pr_2_lcl_intf)
    cpe.delete_fowarding_profile("NEW")
    run_result = ""

start_time = datetime.now()
Do_Cpe_onboarding()
