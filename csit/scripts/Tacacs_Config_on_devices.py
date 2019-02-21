#!/usr/bin/env python
import sys
import os
import pandas as pd
import time
import getpass


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
    ip = '10.91.116.35'
    ldap_user = 'admin'
    ldap_passwd = 'versa123'
    user = 'Sathish'
    passwd = 'Jan*1234'
    cpe_user = 'admin'
    cpe_passwd = 'versa123'
    # node_user = 'admin'
    # node_passwd = 'versa123'
    return {'mgmt_ip' : ip, 'username' : ldap_user,\
            'password' : ldap_passwd, 'GUIusername' : user, 'GUIpassword' : passwd}



def DO_config_in_VD_For_CPEs():
    vd_dict = get_vd_details()
    vd_dict['device_type'] = 'versa_director'
    VD1 = VersaLib('Versa_director', **vd_dict)
    VD1.cpe_list_file_name = vd_dict['mgmt_ip'] + '_Vcpe_List.csv'
    VD1.build_csv(VD1.get_device_list_from_vd_using_rest(dev_type="branch", ping_status_check="no"))
    raw_input("Edit " + VD1.curr_file_dir + "/Topology/" + VD1.cpe_list_file_name + " & Press enter to continue")
    VD1.vdnc = VD1.login()
    # VD1.vdnc = "1234"
    VD1.config_function(nc=VD1.vdnc, csv_file=VD1.cpe_list_file_name, template_file="tacacs_cpe_config.j2", config_for="tacacs", type="devices")
    VD1.close(VD1.vdnc)


DO_config_in_VD_For_CPEs()