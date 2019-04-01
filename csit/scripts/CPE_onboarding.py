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
    cpe_name = raw_input("Enter CPE NAME:").upper()
    # print "CPE NAME:" + cpe_name
    cpe = VersaLib(cpe_name, topofile="Devices.csv")
    main_logger = cpe.main_logger
    main_logger.info("CPE NAME:" + cpe_name)
    time.sleep(1)
    print "AVAILABLE SOLUTIONS:"
    # for sol in cpe.SOLUTIONS_list:
    #     print "\t" + sol
    for i in range(len(cpe.SOLUTIONS_list)):
        print str(i + 1) + "." + cpe.SOLUTIONS_list[i]
    cpe.Solution_type = cpe.SOLUTIONS_list[int(raw_input("Enter Solution number [eg: 1]:"))-1]
    main_logger.info("SOLUTION SELECTED:" + cpe.Solution_type)
    cpe.Create_Node_Data(cpe.SATGING_SERVER, "SS", wan=cpe.SATGING_WAN)
    WC_list = cpe.Create_Controller_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    GW_list = cpe.Create_Gateway_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    cpe.create_cpe_data()
    run_result = ""
    if cpe.PST_CREATION == "YES":
        cpe.create_and_deploy_poststaging_template()
    if cpe.DG_CREATION == "YES":
        cpe.create_and_deploy_device_group()
    if cpe.DEV_TEMPALTE_CREATION == "YES":
        cpe.pre_onboard_work()
    cpe.cpe_onboard_call()
    cpe_result = cpe.get_device_info()
    if isinstance(cpe_result, dict):
        main_logger.info("\n \t >>>>>>>>>>>> CPE ONBOARDING PASSED <<<<<<<<<<<<"
                         "\n \t >>>>>>>>>>>>    CPE DETAILS        <<<<<<<<<<<<")
        main_logger.info(pprint.pprint(cpe.get_device_info()))
    else:
        main_logger.info(">>>>>>>>>>>> CPE ONBOARDING FAILED <<<<<<<<<<<<")
        main_logger.info(cpe_result)
    main_logger.info("CPE ONBOARDINIG SCRIPT COMPLETED")
    main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))
    # cpe_name = raw_input("Enter CPE NAME:").upper()
    # # print "CPE NAME:" + cpe_name
    # cpe1 = VersaLib(cpe_name, topofile="Devices.csv")
    # main_logger = cpe.main_logger
    # main_logger.debug("CPE NAME:" + cpe.Device_name)
    # cpe.username = raw_input("Enter CPE username:")
    # cpe.password = raw_input("Enter CPE password:")
    # print "AVAILBALE NODEs:" + str(cpe.ctlr_dict.keys())
    # cpe.NODE = (raw_input("Enter NODE NAME:")).upper()
    # print "AVAILBALE STAGING SERVERS:" + str(cpe.staging_servers_dict[cpe.NODE])
    # cpe.SATGING_SERVER = raw_input("Enter staging server NAME:")
    # cpe.SATGING_WAN = raw_input("Enter staging WAN (MPLS/INT):").upper()
    # cpe.ORG_NAME = raw_input("Enter ORG NAME:").upper().replace("_", "-")
    # cpe.ORG_ID = raw_input("Enter ORG ID :")
    # cpe.NO_OF_VRFS = int(raw_input("NUMBER OF VRFS :"))
    # PST_CREATION = (raw_input("Want to do PS creation ENTER YES/NO:")).upper()
    # DG_CREATION = (raw_input("Want to do DG creation ENTER YES/NO:")).upper()
    # DEV_TEMPALTE_CREATION = (raw_input("Want to do Device template creation. ENTER YES/NO:")).upper()
    # cpe.__init__(cpe_name, topofile="Devices.csv")
    # print "AVAILABLE Solutions:"
    # for sol in cpe.SOLUTIONS_list:
    #     print "\t" + sol
    # cpe.Solution_type = raw_input("Enter Solution :")
    # if "MPLS" not in cpe.Solution_type:
    #     cpe.INT_INTF_IP_ALLOC = (raw_input("INTERNET intf address allocation ( ENTER DHCP/STATIC):")).upper()
    #     cpe.LIB = (raw_input("do you want LIB. ENTER YES/NO:")).upper()
    #
    # cpe.Create_Node_Data(cpe.SATGING_SERVER, "SS", wan=cpe.SATGING_WAN)
    # WC_list = cpe.Create_Controller_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    # GW_list = cpe.Create_Gateway_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    # cpe.create_cpe_data()
    # run_result = ""
    # if PST_CREATION == "YES":
    #     cpe.create_and_deploy_poststaging_template()
    # if DG_CREATION == "YES":
    #     cpe.create_and_deploy_device_group()
    # if DEV_TEMPALTE_CREATION == "YES":
    #     cpe.pre_onboard_work()
    # cpe.cpe_onboard_call()




start_time = datetime.now()
Do_Cpe_onboarding()
