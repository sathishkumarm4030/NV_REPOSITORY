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
from csit.libraries.HltapiLib import HltapiLib

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
    spirent1 = HltapiLib("10.91.113.124", "10/1", "10/2")
    spirent1.connect_and_reserve_ports()
    device1 = spirent1.create_device(port=0, vlanid='600',
                           intf_ip_addr='192.169.101.3', gateway_ip_addr='192.169.101.1')
    device2 = spirent1.create_device(port=1, vlanid='610',
                           intf_ip_addr='192.169.111.3', gateway_ip_addr='192.169.111.1')
    src_dev_hdl = device1['handle'].split()[0]
    dst_dev_hdl =  device2['handle'].split()[0]
    src_dev_port_hdl = spirent1.port_handle[0]
    dst_dev_port_hdl = spirent1.port_handle[1]
    # spirent1.release_ports()

    # spirent1.get_traffic_results(src_dev_port_hdl, dst_dev_port_hdl)






    # stream1 = spirent1.create_tcp_stream_block(device1, device2,
    #                                            src_port='1060', rate_mbps='2')
    premium_tcp_stream1 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='2001', rate_mbps='2', ip_dscp ='46')
    business1_tcp_stream1 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='2002', rate_mbps='2', ip_dscp ='26')
    business2_tcp_stream1 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='2003', rate_mbps='2', ip_dscp ='18')
    business3_tcp_stream1 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='2004', rate_mbps='2', ip_dscp ='10')
    internet_default_stream1 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='2005', rate_mbps='2', tcp_src_port_count = 10, tcp_src_port_repeat_count=1)

    # stream2 = spirent1.create_udp_stream_block(device1, device2,
    #                                            src_port='1061', rate_mbps='2')
    # stream3 = spirent1.create_tcp_stream_block(device1, device2,
    #                                            src_port='1062', rate_mbps='2')

    spirent1.start_stream_traffic(strm_hdl=premium_tcp_stream1['stream_id'])
    spirent1.start_stream_traffic(strm_hdl=business1_tcp_stream1['stream_id'])
    spirent1.start_stream_traffic(strm_hdl=business2_tcp_stream1['stream_id'])
    spirent1.start_stream_traffic(strm_hdl=business3_tcp_stream1['stream_id'])
    spirent1.start_stream_traffic(strm_hdl=internet_default_stream1['stream_id'])
    # spirent1.start_stream_traffic(strm_hdl=stream2['stream_id'])
    # time.sleep(40)
    # spirent1.start_stream_traffic(strm_hdl=stream3['stream_id'])
    # time.sleep(40)

    spirent1.stop_stream_traffic(premium_tcp_stream1['stream_id'])
    spirent1.stop_stream_traffic(business1_tcp_stream1['stream_id'])
    spirent1.stop_stream_traffic(business2_tcp_stream1['stream_id'])
    spirent1.stop_stream_traffic(business3_tcp_stream1['stream_id'])
    spirent1.stop_stream_traffic(internet_default_stream1['stream_id'])

    # spirent1.stop_stream_traffic(stream2['stream_id'])
    # spirent1.stop_stream_traffic(stream3['stream_id'])


    spirent1.release_ports()
    time.sleep(60)


start_time = datetime.now()
Do_Cpe_onboarding()
