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


def Do_Cpe_onboarding():
    cpe_name = raw_input("Enter CPE NAME:").upper()
    # print "CPE NAME:" + cpe_name
    cpe1 = VersaLib(cpe_name, topofile="Devices.csv")
    main_logger = cpe1.main_logger
    main_logger.debug("CPE NAME:" + cpe1.Device_name)
    WC_list = cpe1.Create_Controller_List(cpe1.ORG_NAME, cpe1.ORG_ID, cpe1.NO_OF_VRFS, cpe1.NODE)
    GW_list = cpe1.Create_Gateway_List(cpe1.ORG_NAME, cpe1.ORG_ID, cpe1.NO_OF_VRFS, cpe1.NODE)
    cpe1.create_cpe_data()
    run_result = ""
    if cpe1.PST_CREATION == "YES":
        cpe1.create_and_deploy_poststaging_template()
    if cpe1.DG_CREATION == "YES":
        cpe1.create_and_deploy_device_group()
    if cpe1.DEV_TEMPALTE_CREATION == "YES":
        cpe1.pre_onboard_work()
    cpe1.cpe_onboard_call()
    # cpe_name = raw_input("Enter CPE NAME:").upper()
    # # print "CPE NAME:" + cpe_name
    # cpe1 = VersaLib(cpe_name, topofile="Devices.csv")
    # main_logger = cpe1.main_logger
    # main_logger.debug("CPE NAME:" + cpe1.Device_name)
    # cpe1.username = raw_input("Enter CPE username:")
    # cpe1.password = raw_input("Enter CPE password:")
    # print "AVAILBALE NODEs:" + str(cpe1.ctlr_dict.keys())
    # cpe1.NODE = (raw_input("Enter NODE NAME:")).upper()
    # print "AVAILBALE STAGING SERVERS:" + str(cpe1.staging_servers_dict[cpe1.NODE])
    # cpe1.SATGING_SERVER = raw_input("Enter staging server NAME:")
    # cpe1.SATGING_WAN = raw_input("Enter staging WAN (MPLS/INT):").upper()
    # cpe1.ORG_NAME = raw_input("Enter ORG NAME:").upper().replace("_", "-")
    # cpe1.ORG_ID = raw_input("Enter ORG ID :")
    # cpe1.NO_OF_VRFS = int(raw_input("NUMBER OF VRFS :"))
    # PST_CREATION = (raw_input("Want to do PS creation ENTER YES/NO:")).upper()
    # DG_CREATION = (raw_input("Want to do DG creation ENTER YES/NO:")).upper()
    # DEV_TEMPALTE_CREATION = (raw_input("Want to do Device template creation. ENTER YES/NO:")).upper()
    # cpe1.__init__(cpe_name, topofile="Devices.csv")
    # print "AVAILABLE Solutions:"
    # for sol in cpe1.SOLUTIONS_list:
    #     print "\t" + sol
    # cpe1.Solution_type = raw_input("Enter Solution :")
    # if "MPLS" not in cpe1.Solution_type:
    #     cpe1.INT_INTF_IP_ALLOC = (raw_input("INTERNET intf address allocation ( ENTER DHCP/STATIC):")).upper()
    #     cpe1.LIB = (raw_input("do you want LIB. ENTER YES/NO:")).upper()
    #
    # cpe1.Create_Node_Data(cpe1.SATGING_SERVER, "SS", wan=cpe1.SATGING_WAN)
    # WC_list = cpe1.Create_Controller_List(cpe1.ORG_NAME, cpe1.ORG_ID, cpe1.NO_OF_VRFS, cpe1.NODE)
    # GW_list = cpe1.Create_Gateway_List(cpe1.ORG_NAME, cpe1.ORG_ID, cpe1.NO_OF_VRFS, cpe1.NODE)
    # cpe1.create_cpe_data()
    # run_result = ""
    # if PST_CREATION == "YES":
    #     cpe1.create_and_deploy_poststaging_template()
    # if DG_CREATION == "YES":
    #     cpe1.create_and_deploy_device_group()
    # if DEV_TEMPALTE_CREATION == "YES":
    #     cpe1.pre_onboard_work()
    # cpe1.cpe_onboard_call()
    main_logger.info(cpe1.get_device_info())



start_time = datetime.now()
Do_Cpe_onboarding()
print "Time elapsed: {}\n".format(datetime.now() - start_time)