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

print fileDir
Par_Dir = os.path.dirname(fileDir)
print Par_Dir
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
    cpe_name = raw_input("Enter CPE NAME:\n")
    print "CPE NAME:" + cpe_name
    cpe1 = VersaLib(cpe_name, topofile="Devices.csv")
    main_logger = cpe1.main_logger
    main_logger.info("CPE NAME:" + cpe1.Device_name)
    run_result = ""
    cpe1.create_PS_and_DG()
    cpe1.pre_onboard_work()
    cpe1.cpe_onboard_call()
    main_logger.info(cpe1.get_device_info())
    # cpe2 = VersaLib('JAN18_CPE2_MUM', topofile="Devices.csv")
    # cpe2.pre_onboard_work()
    # cpe2.cpe_onboard_call()
    # cpe2_dev_info_on_vd = cpe1.get_device_info()
    # print cpe2_dev_info_on_vd


start_time = datetime.now()
Do_Cpe_onboarding()
print "Time elapsed: {}\n".format(datetime.now() - start_time)