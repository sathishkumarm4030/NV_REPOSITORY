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

def Do_Cpe_onboarding(**kwargs):
    start_time = datetime.now()
    cpe_name = raw_input("Enter CPE NAME:").upper()
    print "CPE NAME:" + cpe_name
    # cpe_name = "CPE27-HKG2-SINGLE-CPE-DUAL-INTERNET"
    if kwargs is not None:
        cpe = VersaLib(cpe_name, topofile="Devices.csv", **kwargs)
    else:
        cpe = VersaLib(cpe_name, topofile="Devices.csv")
    main_logger = cpe.main_logger
    main_logger.info("LOG FILE PATH : " + cpe.logfile)
    main_logger.info("CPE NAME:" + cpe_name)
    time.sleep(1)
    main_logger.info("SOLUTION SELECTED:" + cpe.Solution_type)
    cpe.Create_Node_Data(cpe.STAGING_SERVER, "SS", wan=cpe.STAGING_WAN)
    WC_list = cpe.Create_Controller_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    GW_list = cpe.Create_Gateway_List(cpe.ORG_NAME, cpe.ORG_ID, cpe.NO_OF_VRFS, cpe.NODE)
    cpe.create_cpe_data()
    run_result = ""
    for WC in WC_list:
        cpe.check_org_for_controller(WC)
    if cpe.PST_CREATION == "YES":
        cpe.create_and_deploy_poststaging_template()
    if cpe.DG_CREATION == "YES":
        cpe.create_and_deploy_device_group()
    if cpe.DEV_TEMPALTE_CREATION == "YES":
        cpe.pre_onboard_work()
    if cpe.DEV_ONBAORD == "YES":
        cpe.cpe_onboard_call()
        cpe_result = cpe.get_device_info()
        if isinstance(cpe_result, dict):
            main_logger.info("\n \t >>>>>>>>>>>> CPE ONBOARDING PASSED <<<<<<<<<<<<"
                             "\n \t >>>>>>>>>>>>    CPE DETAILS        <<<<<<<<<<<<")
            main_logger.info(pprint.pprint(cpe.get_device_info()))
        else:
            main_logger.info(">>>>>>>>>>>> CPE ONBOARDING FAILED <<<<<<<<<<<<")
            main_logger.info(cpe_result)
    if cpe.DEV_VRRP_LIB_CONFIG == "YES":
        cpe.config_devices_vrrp_and_lib()
    main_logger.info("CPE ONBOARDINIG SCRIPT COMPLETED")
    main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))
    main_logger.info("LOG FILE PATH : " + cpe.logfile)

Do_Cpe_onboarding()
# Do_Cpe_onboarding(loglevel='DEBUG')
