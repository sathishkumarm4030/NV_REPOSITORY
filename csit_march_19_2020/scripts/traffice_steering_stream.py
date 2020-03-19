##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth

##############################################################
#config the parameters for the logging
##############################################################

test_sta = sth.test_config (
		log                                              = '1',
		logfile                                          = 'traffice_steering_stream_logfile',
		vendorlogfile                                    = 'traffice_steering_stream_stcExport',
		vendorlog                                        = '1',
		hltlog                                           = '1',
		hltlogfile                                       = 'traffice_steering_stream_hltExport',
		hlt2stcmappingfile                               = 'traffice_steering_stream_hlt2StcMapping',
		hlt2stcmapping                                   = '1',
		log_level                                        = '7');

status = test_sta['status']
if (status == '0') :
	print("run sth.test_config failed")
	print(test_sta)
else:
	print("***** run sth.test_config successfully")


##############################################################
#config the parameters for optimization and parsing
##############################################################

test_ctrl_sta = sth.test_control (
		action                                           = 'enable');

status = test_ctrl_sta['status']
if (status == '0') :
	print("run sth.test_control failed")
	print(test_ctrl_sta)
else:
	print("***** run sth.test_control successfully")


##############################################################
#connect to chassis and reserve port list
##############################################################

i = 0
device = "10.91.113.124"
port_list = ['10/1','10/2']
port_handle = []
intStatus = sth.connect (
		device                                           = device,
		port_list                                        = port_list,
		break_locks                                      = 1,
		offline                                          = 0 )

status = intStatus['status']

if (status == '1') :
	for port in port_list :
		port_handle.append(intStatus['port_handle'][device][port])
		print("\n reserved ports",port,":", port_handle[i])
		i += 1
else :
	print("\nFailed to retrieve port handle!\n")
	print(port_handle)


##############################################################
#interface config
##############################################################

int_ret0 = sth.interface_config (
		mode                                             = 'config',
		port_handle                                      = port_handle[0],
		create_host                                      = 'false',
		intf_mode                                        = 'ethernet',
		phy_mode                                         = 'copper',
		scheduling_mode                                  = 'RATE_BASED',
		port_loadunit                                    = 'MEGABITS_PER_SECOND',
		port_load                                        = '1',
		enable_ping_response                             = '0',
		control_plane_mtu                                = '1500',
		speed                                            = 'ether1000',
		duplex                                           = 'full',
		autonegotiation                                  = '1');

status = int_ret0['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret0)
else:
	print("***** run sth.interface_config successfully")

int_ret1 = sth.interface_config (
		mode                                             = 'config',
		port_handle                                      = port_handle[1],
		create_host                                      = 'false',
		intf_mode                                        = 'ethernet',
		phy_mode                                         = 'copper',
		scheduling_mode                                  = 'PORT_BASED',
		port_loadunit                                    = 'MEGABITS_PER_SECOND',
		port_load                                        = '1',
		enable_ping_response                             = '0',
		control_plane_mtu                                = '1500',
		speed                                            = 'ether1000',
		duplex                                           = 'full',
		autonegotiation                                  = '1');

status = int_ret1['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret1)
else:
	print("***** run sth.interface_config successfully")


##############################################################
#create device and config the protocol on it
##############################################################

#start to create the device: Device 1
device_ret0 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '610',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.5',
		count                                            = '1',
		enable_ping_response                             = '1',
		mac_addr                                         = '00:10:94:00:00:05',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.111.3',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.111.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f4:4f:63',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret0['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret0)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 2
device_ret1 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '600',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.7',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:07',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.101.3',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.101.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f1:9a:5d',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret1['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret1)
else:
	print("***** run sth.emulation_device_config successfully")


##############################################################
#create traffic
##############################################################

src_hdl = device_ret1['handle'].split()[0]

dst_hdl = device_ret0['handle'].split()[0]


streamblock_ret1 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'udp',
		udp_src_port                                     = '1024',
		udp_dst_port                                     = '1024',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '17',
		ip_fragment_offset                               = '0',
		ip_mbz                                           = '0',
		ip_precedence                                    = '6',
		ip_tos_field                                     = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '128',
		name                                             = 'StreamBlock_11-2',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '128',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		dest_port_list                                   = port_handle[0],
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '1',
		mac_discovery_gw                                 = '192.169.101.1');

status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
else:
	print("***** run sth.traffic_config successfully")

#config part is finished

##############################################################
#start devices
##############################################################


##############################################################
#start traffic
##############################################################

traffic_ctrl_ret = sth.traffic_control (
		port_handle                                      = [port_handle[0],port_handle[1]],
		action                                           = 'run');

status = traffic_ctrl_ret['status']
if (status == '0') :
	print("run sth.traffic_control failed")
	print(traffic_ctrl_ret)
else:
	print("***** run sth.traffic_control successfully")


##############################################################
#start to get the device results
##############################################################


##############################################################
#start to get the traffic results
##############################################################

traffic_results_ret = sth.traffic_stats (
		port_handle                                      = [port_handle[0],port_handle[1]],
		mode                                             = 'all');

status = traffic_results_ret['status']
if (status == '0') :
	print("run sth.traffic_stats failed")
	print(traffic_results_ret)
else:
	print("***** run sth.traffic_stats successfully, and results is:")
	print(traffic_results_ret)


##############################################################
#clean up the session, release the ports reserved and cleanup the dbfile
##############################################################

cleanup_sta = sth.cleanup_session (
		port_handle                                      = [port_handle[0],port_handle[1]],
		clean_dbfile                                     = '1');

status = cleanup_sta['status']
if (status == '0') :
	print("run sth.cleanup_session failed")
	print(cleanup_sta)
else:
	print("***** run sth.cleanup_session successfully")


print("**************Finish***************")
