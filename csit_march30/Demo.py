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
		logfile                                          = 'Demo_logfile',
		vendorlogfile                                    = 'Demo_stcExport',
		vendorlog                                        = '1',
		hltlog                                           = '1',
		hltlogfile                                       = 'Demo_hltExport',
		hlt2stcmappingfile                               = 'Demo_hlt2StcMapping',
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
		scheduling_mode                                  = 'PORT_BASED',
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
		scheduling_mode                                  = 'RATE_BASED',
		port_loadunit                                    = 'PERCENT_LINE_RATE',
		port_load                                        = '10',
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

#start to create the device: Device 11
device_ret0 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '600',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.1',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:01',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.101.4',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.101.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f1:9a:5d',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret0['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret0)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 12
device_ret1 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '600',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.1',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:01',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.101.5',
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

#start to create the device: Device 13
device_ret2 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '600',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.1',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:01',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.101.6',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.101.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f1:9a:5d',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret2['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret2)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 14
device_ret3 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '600',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.1',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:01',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.101.7',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.101.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f1:9a:5d',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret3['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret3)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 15
device_ret4 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '600',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.1',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:01',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.101.8',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.101.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f1:9a:5d',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret4['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret4)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 16
device_ret5 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '610',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.2',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:02',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.111.4',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.111.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f4:4f:63',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret5['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret5)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 17
device_ret6 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '610',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.2',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:02',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.111.5',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.111.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f4:4f:63',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret6['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret6)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 18
device_ret7 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '610',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.2',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:02',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.111.6',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.111.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f4:4f:63',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret7['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret7)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 19
device_ret8 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '610',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.2',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:02',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.111.7',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.111.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f4:4f:63',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret8['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret8)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 20
device_ret9 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '7',
		vlan_cfi                                         = '0',
		vlan_id                                          = '610',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.2',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:02',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '192.169.111.8',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '192.169.111.1',
		gateway_ip_addr_step                             = '0.0.0.0',
		gateway_mac                                      = '00:0b:ab:f4:4f:63',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret9['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret9)
else:
	print("***** run sth.emulation_device_config successfully")


##############################################################
#create traffic
##############################################################

src_hdl = device_ret0['handle'].split()[0]

dst_hdl = device_ret5['handle'].split()[0]


streamblock_ret1 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '179',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_dscp                                          = '46',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		l3_length                                        = '160',
		name                                             = 'Premium-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '160',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.101.1',
		enable_stream                                    = 'false');

status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret1['handle'].split()[0]

dst_hdl = device_ret6['handle'].split()[0]


streamblock_ret2 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '179',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_dscp                                          = '26',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		name                                             = 'Business1-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.101.1',
		enable_stream                                    = 'false');

status = streamblock_ret2['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret2)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret2['handle'].split()[0]

dst_hdl = device_ret7['handle'].split()[0]


streamblock_ret3 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '1024',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_dscp                                          = '18',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		name                                             = 'BUsiness2-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.101.1',
		enable_stream                                    = 'false');

status = streamblock_ret3['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret3)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret3['handle'].split()[0]

dst_hdl = device_ret8['handle'].split()[0]


streamblock_ret4 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
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
		ip_dscp                                          = '10',
		udp_src_port_count                               = '1000',
		udp_src_port_repeat_count                        = '1',
		udp_src_port_step                                = '1',
		udp_src_port_mode                                = 'increment',
		enable_control_plane                             = '0',
		name                                             = 'Business3-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.101.1',
		enable_stream                                    = 'false');

status = streamblock_ret4['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret4)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret4['handle'].split()[0]

dst_hdl = device_ret9['handle'].split()[0]


streamblock_ret5 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '1024',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_mbz                                           = '0',
		ip_precedence                                    = '6',
		ip_tos_field                                     = '0',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		name                                             = 'BE-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.101.1',
		enable_stream                                    = 'false');

status = streamblock_ret5['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret5)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret0['handle'].split()[0]

dst_hdl = device_ret5['handle'].split()[0]


streamblock_ret6 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
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
		ip_dscp                                          = '46',
		enable_control_plane                             = '0',
		l3_length                                        = '128',
		name                                             = 'StreamBlock_11-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '128',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		dest_port_list                                   = port_handle[1],
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

status = streamblock_ret6['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret6)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret0['handle'].split()[0]

dst_hdl = device_ret5['handle'].split()[0]


streamblock_ret7 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '1024',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_mbz                                           = '0',
		ip_precedence                                    = '6',
		ip_tos_field                                     = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '128',
		name                                             = 'AAA-2',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '128',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		dest_port_list                                   = port_handle[1],
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

status = streamblock_ret7['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret7)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret5['handle'].split()[0]

dst_hdl = device_ret0['handle'].split()[0]


streamblock_ret8 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '179',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_dscp                                          = '46',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		l3_length                                        = '160',
		name                                             = 'Premium-4',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '160',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.111.1',
		enable_stream                                    = 'false');

status = streamblock_ret8['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret8)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret6['handle'].split()[0]

dst_hdl = device_ret1['handle'].split()[0]


streamblock_ret9 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '179',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_dscp                                          = '26',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		name                                             = 'Business1-4',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.111.1',
		enable_stream                                    = 'false');

status = streamblock_ret9['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret9)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret7['handle'].split()[0]

dst_hdl = device_ret2['handle'].split()[0]


streamblock_ret10 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '1024',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_dscp                                          = '18',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		name                                             = 'Business2-4',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.111.1',
		enable_stream                                    = 'false');

status = streamblock_ret10['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret10)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret8['handle'].split()[0]

dst_hdl = device_ret3['handle'].split()[0]


streamblock_ret11 = sth.traffic_config (
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
		ip_dscp                                          = '10',
		udp_src_port_count                               = '1000',
		udp_src_port_repeat_count                        = '1',
		udp_src_port_step                                = '1',
		udp_src_port_mode                                = 'increment',
		enable_control_plane                             = '0',
		name                                             = 'Business3-4',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.111.1',
		enable_stream                                    = 'false');

status = streamblock_ret11['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret11)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret9['handle'].split()[0]

dst_hdl = device_ret4['handle'].split()[0]


streamblock_ret12 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		l4_protocol                                      = 'tcp',
		tcp_ack_num                                      = '234567',
		tcp_seq_num                                      = '123456',
		tcp_urg_flag                                     = '0',
		tcp_fin_flag                                     = '0',
		tcp_ack_flag                                     = '1',
		tcp_data_offset                                  = '5',
		tcp_rst_flag                                     = '0',
		tcp_window                                       = '4096',
		tcp_urgent_ptr                                   = '0',
		tcp_psh_flag                                     = '0',
		tcp_syn_flag                                     = '0',
		tcp_checksum                                     = '0',
		tcp_src_port                                     = '1024',
		tcp_reserved                                     = '0',
		tcp_dst_port                                     = '1024',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '6',
		ip_fragment_offset                               = '0',
		ip_mbz                                           = '0',
		ip_precedence                                    = '6',
		ip_tos_field                                     = '0',
		tcp_src_port_count                               = '1000',
		tcp_src_port_mode                                = 'increment',
		tcp_src_port_repeat_count                        = '1',
		tcp_src_port_step                                = '1',
		enable_control_plane                             = '0',
		name                                             = 'BE-4',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'imix',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		l3_imix1_ratio                                   = '45',
		l3_imix1_size                                    = '64',
		l3_imix2_ratio                                   = '8',
		l3_imix2_size                                    = '80',
		l3_imix3_ratio                                   = '15',
		l3_imix3_size                                    = '200',
		l3_imix4_ratio                                   = '2',
		l3_imix4_size                                    = '576',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = '10',
		mac_discovery_gw                                 = '192.169.111.1',
		enable_stream                                    = 'false');

status = streamblock_ret12['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret12)
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
