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
    # spirent1.interface_config(spirent1.port_handle[0])
    # spirent1.interface_config(spirent1.port_handle[1])
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

    ckt_pr_1_lcl_intf = cpe1.WAN1_NAME
    ckt_pr_2_lcl_intf = cpe1.WAN2_NAME
    curr_intf_bw = cpe1.get_vni_interface_bw(cpe1.WAN1_INTF)
    print cpe1.modify_interface_bandwidth(cpe1.WAN1_INTF, 30000, 30000)
    print cpe1.get_vni_interface_bw(cpe1.WAN1_INTF)

    SLA_PRF_1 = "SLA100"
    FWP1 = "FWP100"
    IPADDOBJ = "Dest_ip_add100"
    PLCYRULE = "ts_Destipaddr100"

    cpe1.cross_login()
    cpe1.create_sla_profile(SLA_PRF_1, description="description", circuit_transmit_utilization=5)
    print cpe1.get_sla_profile(SLA_PRF_1)
    cpe1.create_fowarding_profile(FWP1, ckt_pr_1_lcl_intf, ckt_pr_2_lcl_intf, sla_name=SLA_PRF_1, evaluate_continuously="disable")
    cpe1.create_address_object(IPADDOBJ, "ipv4-prefix", cpe2.lan[1]['third_host']+"/32")
    cpe1.create_policy_rule(PLCYRULE, FWP1, dest_address_obj=IPADDOBJ)
    print vd1.move_policy_rule(cpe1.Device_name, cpe1.ORG_NAME,  'Default-Policy', PLCYRULE, 'first')

    print cpe1.req_clr_sess_all()

    stream1 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='1060', rate_mbps='2')
    stream2 = spirent1.create_udp_stream_block(device1, device2,
                                               src_port='1061', rate_mbps='2')
    stream3 = spirent1.create_tcp_stream_block(device1, device2,
                                               src_port='1062', rate_mbps='2')

    spirent1.start_stream_traffic(strm_hdl=stream1['stream_id'])
    time.sleep(40)
    spirent1.start_stream_traffic(strm_hdl=stream2['stream_id'])
    time.sleep(40)
    spirent1.start_stream_traffic(strm_hdl=stream3['stream_id'])
    time.sleep(40)

    result = cpe1.show_session_sdwan_detail(source_port='1060')

    print result

    if "tx-wan-ckt                 " + ckt_pr_1_lcl_intf in result:
        print "passed"
    else:
        print result

    result = cpe1.show_session_sdwan_detail(source_port='1061')

    print result

    if "tx-wan-ckt                 " + ckt_pr_2_lcl_intf in result:
        print "passed"
    else:
        print result

    result = cpe1.show_session_sdwan_detail(source_port='1062')

    print result

    if "tx-wan-ckt                 " + ckt_pr_2_lcl_intf in result:
        print "passed"
    else:
        print result

    spirent1.stop_stream_traffic(stream1['stream_id'])
    spirent1.stop_stream_traffic(stream2['stream_id'])
    spirent1.stop_stream_traffic(stream3['stream_id'])


    spirent1.release_ports()
    time.sleep(60)











    cpe1.delete_policy_rule(PLCYRULE)
    cpe1.delete_address_object(IPADDOBJ)
    cpe1.delete_fowarding_profile(FWP1)
    cpe1.delete_sla_profile(SLA_PRF_1)

    cpe1.modify_interface_bandwidth(cpe1.WAN1_INTF, curr_intf_bw['bandwidth']['uplink'], curr_intf_bw['bandwidth']['downlink'])
    print cpe1.get_vni_interface_bw(cpe1.WAN1_INTF)








    run_result = ""

start_time = datetime.now()
Do_Cpe_onboarding()
