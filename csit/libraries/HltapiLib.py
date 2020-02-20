import sth
import time
from sys import argv

class HltapiLib:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, device, port1, port2, **kwargs):
        self.device = device
        self.port_list = [port1, port2]
        self.port_handle = []
        # Config the parameters for the logging
        test_sta = sth.test_config(
            log='1',
            logfile='HLTAPI_InterfaceConfig_Port_Load_logfile',
            vendorlogfile='HLTAPI_InterfaceConfig_Port_Load_stcExport',
            vendorlog='1',
            hltlog='1',
            hltlogfile='HLTAPI_InterfaceConfig_Port_Load_hltExport',
            hlt2stcmappingfile='HHLTAPI_InterfaceConfig_Port_Load_hlt2StcMapping',
            hlt2stcmapping='1',
            log_level='7')

        status = test_sta['status']
        if status == '0':
            print "run sth.test_config failed"
            print test_sta
        else:
            print "***** run sth.test_config successfully"





########################################
# Step1. Reserve and connect chassis ports
########################################
    def connect_and_reserve_ports(self):
        intStatus = sth.connect(device=self.device, port_list=self.port_list);
        status = intStatus['status']
        i = 0
        if status == '1':
            for port in self.port_list:
                self.port_handle.append(intStatus['port_handle'][self.device][port])
                print "\n reserved ports", port, ":", self.port_handle[i], ": port_handle[%s]" % i
                i += 1
        else:
            print "\nFailed to retrieve port handle!\n"
            print self.port_handle

        self.interface_config(0)
        self.interface_config(1)

##############################################################
# interface config
##############################################################
    def interface_config(self, port):
        int_ret0 = sth.interface_config(
            mode='config',
            port_handle=self.port_handle[int(port)],
            create_host='false',
            intf_mode='ethernet',
            phy_mode='copper',
            scheduling_mode='RATE_BASED',
            port_loadunit='MEGABITS_PER_SECOND',
            port_load='5',
            enable_ping_response='0',
            control_plane_mtu='1500',
            speed='ether1000',
            duplex='full',
            autonegotiation='1');

        status = int_ret0['status']
        if (status == '0'):
            print("run sth.interface_config failed")
            print(int_ret0)
        else:
            print("***** run sth.interface_config successfully")

##############################################################
# create device and config the protocol on it
##############################################################
    def create_device(self, port, vlanid, intf_ip_addr, gateway_ip_addr, **kwargs):
        # start to create the device: Device 1
        device_ret0 = sth.emulation_device_config(
            mode='create',
            ip_version='ipv4',
            encapsulation='ethernet_ii_vlan',
            port_handle=self.port_handle[int(port)],
            vlan_id=vlanid,
            enable_ping_response='1',
            intf_ip_addr=intf_ip_addr,
            gateway_ip_addr=gateway_ip_addr,
            resolve_gateway_mac = 'true');


        status = device_ret0['status']
        if (status == '0'):
            print("run sth.emulation_device_config failed")
            print(device_ret0)
        else:
            device_ret0['port'] = self.port_handle[int(port)]
            device_ret0['gateway_ip_addr'] = gateway_ip_addr
            device_ret0['vlanid'] = vlanid
            device_ret0['intf_ip_addr'] = gateway_ip_addr
            print("***** run sth.emulation_device_config successfully")
            return device_ret0

##############################################################
# get the device info
##############################################################
    def get_device_info(self, port, vlanid, mac_addr, intf_ip_addr, gateway_ip_addr, **kwargs):
        device_info = sth.device_info(
            ports='',
            port_handle=[port],
            fspec_version='');

        status = device_info['status']
        if (status == '0'):
            print("run sth.device_info failed")
            print(device_info)
        else:
            print("***** run sth.device_info successfully")

##############################################################
# create tcp stream block
##############################################################
    def create_tcp_stream_block(self, src_device, dst_device, src_port, rate_mbps):
        streamblock_ret1 = sth.traffic_config(
            mode='create',
            port_handle=src_device['port'],
            emulation_src_handle=src_device['handle'],
            emulation_dst_handle=dst_device['handle'],
            l3_protocol='ipv4',
            l4_protocol='tcp',
            tcp_src_port=src_port,
            tcp_dst_port='1024',
            ip_id='0',
            ip_ttl='255',
            ip_hdr_length='5',
            ip_fragment_offset='0',
            ip_mbz='0',
            ip_precedence='6',
            ip_tos_field='0',
            enable_control_plane='0',
            l3_length='160',
            fill_type='constant',
            fcs_error='0',
            fill_value='0',
            frame_size='160',
            traffic_state='1',
            high_speed_result_analysis='1',
            length_mode='fixed',
            dest_port_list=dst_device['port'],
            tx_port_sending_traffic_to_self_en='false',
            disable_signature='0',
            enable_stream_only_gen='1',
            pkts_per_burst='1',
            inter_stream_gap_unit='bytes',
            burst_loop_count='30',
            transmit_mode='continuous',
            inter_stream_gap='12',
            rate_mbps=rate_mbps,
            mac_discovery_gw=src_device['gateway_ip_addr']);

        status = streamblock_ret1['status']
        if (status == '0'):
            print("run sth.traffic_config failed")
            print(streamblock_ret1)
        else:
            print("***** run sth.traffic_config successfully")
            return streamblock_ret1

##############################################################
# create udp stream block
##############################################################
    def create_udp_stream_block(self, src_device, dst_device, src_port, rate_mbps):
        streamblock_ret1 = sth.traffic_config(
            mode='create',
            port_handle=src_device['port'],
            emulation_src_handle=src_device['handle'],
            emulation_dst_handle=dst_device['handle'],
            l3_protocol='ipv4',
            l4_protocol='udp',
            udp_src_port=src_port,
            udp_dst_port='1025',
            ip_id='0',
            ip_ttl='255',
            ip_hdr_length='5',
            ip_protocol='17',
            ip_fragment_offset='0',
            ip_mbz='0',
            ip_precedence='6',
            ip_tos_field='0',
            enable_control_plane='0',
            l3_length='160',
            fill_type='constant',
            fcs_error='0',
            fill_value='0',
            frame_size='160',
            traffic_state='1',
            high_speed_result_analysis='1',
            length_mode='fixed',
            dest_port_list=dst_device['port'],
            tx_port_sending_traffic_to_self_en='false',
            disable_signature='0',
            enable_stream_only_gen='1',
            pkts_per_burst='1',
            inter_stream_gap_unit='bytes',
            burst_loop_count='30',
            transmit_mode='continuous',
            inter_stream_gap='12',
            rate_mbps=rate_mbps,
            mac_discovery_gw=src_device['gateway_ip_addr']);

        status = streamblock_ret1['status']
        if (status == '0'):
            print("run sth.traffic_config failed")
            print(streamblock_ret1)
        else:
            print("***** run sth.traffic_config successfully")
            return streamblock_ret1


##############################################################
# start traffic
##############################################################
    def start_stream_traffic(self, strm_hdl):
        print strm_hdl
        traffic_ctrl_ret = sth.traffic_control(
            stream_handle=[strm_hdl],
            action='run');

        status = traffic_ctrl_ret['status']
        if (status == '0'):
            print("run sth.traffic_control failed")
            print(traffic_ctrl_ret)
        else:
            print("***** run sth.traffic_control successfully")
            return traffic_ctrl_ret

    ##############################################################
    # start traffic
    ##############################################################
    def stop_stream_traffic(self, strm_hdl):
        traffic_ctrl_ret = sth.traffic_control(
            stream_handle=[strm_hdl],
            action='stop');

        status = traffic_ctrl_ret['status']
        if (status == '0'):
            print("run sth.traffic_control failed")
            print(traffic_ctrl_ret)
        else:
            print("***** run sth.traffic_control successfully")


##############################################################
# start to get the traffic results
##############################################################
    def get_traffic_results(self, src_dev_port_hdl, dst_dev_port_hdl):
        traffic_results_ret = sth.traffic_stats(
            port_handle=[src_dev_port_hdl, dst_dev_port_hdl],
            mode='all');

        status = traffic_results_ret['status']
        if (status == '0'):
            print("run sth.traffic_stats failed")
            print(traffic_results_ret)
        else:
            print("***** run sth.traffic_stats successfully, and results is:")
            print(traffic_results_ret)
##############################################################
# Step4. Release resources
##############################################################
    def release_ports(self):
        print "Release resources"
        cleanup_sta = sth.cleanup_session(port_handle=[self.port_handle[0], self.port_handle[1]], clean_dbfile='1')
        status = cleanup_sta['status']
        if status == '0':
            print "run sth.cleanup_session failed"
            print cleanup_sta
        else:
            print "***** run sth.cleanup_session successfully"

