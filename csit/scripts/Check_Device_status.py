    #!/usr/bin/env python
import sys
import os
import pandas as pd
from datetime import datetime
import time
import getpass


if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# print fileDir
Par_Dir = os.path.dirname(fileDir)
# print Par_Dir
sys.path.append(Par_Dir)



if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

curr_file_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))

from csit.libraries.VersaLib import VersaLib

def get_vd_details():
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
    ip = '10.91.127.194'
    ldap_user = 'Automated'
    ldap_passwd = 'Auto@12345'
    user = 'Automated'
    passwd = 'Auto@12345'
    return {'mgmt_ip' : ip, 'username' : ldap_user,\
            'password' : ldap_passwd}



def Check_Device_Status():
    start_time = datetime.now()
    vd_dict = get_vd_details()
    vd_dict['device_type'] = 'versa_director'
    VD1 = VersaLib('Versa_director', **vd_dict)
    # org_csv = raw_input("Enter Org names csv file:\n")
    org_csv = "ORGS.csv"
    csv_data_read = pd.read_csv(curr_file_dir + "/DATA/" + org_csv)
    # org_name = raw_input("Enter Org name:\n")
    # csv_file = raw_input("Enter Devices csv file name:\n")
    # org_name = "IPC00190"
    csv_file = "WC1_DEVICES.csv"
    VD1.vdnc = VD1.login()
    # VD1.vdnc = "1234"
    for idx, row in csv_data_read.iterrows():
        dev_dict = row.to_dict()
        VD1.generic_config_function(nc=VD1.vdnc, csv_file=csv_file, template_file="ipsec_ike_transform_device_config.j2", config_for="ipsec_ike_transform", type="device_check", org_name=dev_dict['ORG_NAME'])
    VD1.main_logger.info("Result stored in : " + VD1.file_name_with_path)
    VD1.close(VD1.vdnc)
    VD1.main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))


Check_Device_Status()