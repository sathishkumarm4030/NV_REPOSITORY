*** Settings ***
Documentation     A test suite with tests for SDWAN SINGLE CPE MPLS only Solution.
...               Topology:-
...               ____________________________
...               | VersaDirector |
...               |___________________________|
...               |
...               |
...               |
...               _____________|_______________
...               | WanCtrller1 |
...               |____________________________|
...               | |
...               | |
...               | |
...               INTERNET/MPLS
...               | |
...               | |___
...               ______|__ ___|___
...               | | | |
...               LAN1--+ CPE1 | | CPE2 +--LAN1
...               |________| |_______|
...
...
...               Testplan Goals:-
...               1. CHECK WAN INTERFACES STATUS.
...               2. CHECK BGP NEIGHBOR STATUS.
...               3. CHECK LAN ROUTE.
...               4. Ping Test.
...               5. IPERF Test.
...               6. Traffic steering Test.
...               7. QOS Test.
Suite Setup       STARTUP
Suite Teardown    CLEANUP
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ../libraries/Variables.py
Library           Collections
Library           String
Variables         SINGLE_CPE_MPLS_ONLY_SOLUTION_TEST_TOPOLOGY.py
Library           ../libraries/VersaLib.py    VD1    topofile=Devices.csv    WITH NAME    VD1
Library           ../libraries/VersaLib.py    ${CPE1}    topofile=Devices.csv    WITH NAME    CPE1
Library           ../libraries/VersaLib.py    ${CPE2}    topofile=Devices.csv    WITH NAME    CPE2
Library           ../libraries/VersaLib.py    ${CPE3}    topofile=Devices.csv    WITH NAME    CPE3
Library           ../libraries/LinuxLib.py    ${VM1}    topofile=VM_Devices.csv    WITH NAME    VM1
Library           ../libraries/LinuxLib.py    ${VM2}    topofile=VM_Devices.csv    WITH NAME    VM2
Library           ../libraries/LinuxLib.py    ${VM3}    topofile=VM_Devices.csv    WITH NAME    VM3
Library           ../libraries/HltapiLib.py    ${Spirent_chasis1[0]}    ${Spirent_chasis1[1]}    ${Spirent_chasis1[2]}    WITH NAME    spirent1
Library           DebugLibrary

*** Variables ***
${est}            Established
${unit_o}         .0
${up}             up
${bw}             30000

*** Test Cases ***
NV_SINGLE_CPE_MPLS_ONLY_SANITY_01
    [Documentation]    SANITY CHECKS on vCPE
    [Tags]    SANITY1
    CHECK MPLS WAN INTERFACE UP in CPE1
    CHECK MPLS WAN INTERFACE UP in CPE2
    CHECK INTERNET WAN INTERFACE UP in CPE2
    CHECK INTERNET WAN INTERFACE UP in CPE3
    CHECK WC1 PTVI INTERFACE STATUS in CPE1
    CHECK WC1 PTVI INTERFACE STATUS in CPE2
    CHECK WC1 PTVI INTERFACE STATUS in CPE3
    CHECK WC2 PTVI INTERFACE STATUS in CPE1
    CHECK WC2 PTVI INTERFACE STATUS in CPE2
    CHECK WC2 PTVI INTERFACE STATUS in CPE3
    CHECK WC1 BGP NEIGHBOR STATUS in CPE1 & CPE2 and CPE3
    CHECK WC2 BGP NEIGHBOR STATUS in CPE1 & CPE2 and CPE3
    CHECK CPE2 LAN ROUTE Present in CPE1
    CHECK CPE3 LAN ROUTE Present in CPE1
    CHECK CPE1 LAN ROUTE Present in CPE2
    CHECK CPE1 LAN ROUTE Present in CPE3

NV_SINGLE_CPE_MPLS_ONLY_SANITY_02
    [Documentation]    Ping test CPE1 LAN1 VM to CPE2 LAN1 VM
    [Tags]    PING    SANITY1
    Ping Test VM1 To VM2(1 LAN)
    Ping Test VM2 To VM1(1 LAN)
    Ping Test VM1 to VM3(1 LAN)
    Ping Test VM3 to VM1(1 LAN)

NV_SINGLE_CPE_MPLS_ONLY_SANITY_03
    [Documentation]    Ping test CPE1 ALL LAN VM to CPE2 ALL LAN VM
    [Tags]    PING    SANITY1
    Ping Test VM1 To VM2(ALL LANS)
    Ping Test VM2 To VM1(ALL LANS)

NV_SINGLE_CPE_MPLS_ONLY_SANITY_04
    [Documentation]    Iperf test VM1 to VM2
    [Tags]    IPERF    SANITY1
    Iperf3 Test VM1 To VM2
    Iperf3 test VM1 to VM3

NV_SINGLE_CPE_MPLS_ONLY_QOS_01
    [Documentation]    DSCP Values based QOS
    [Tags]    QOS
    REQ CLR SESSION ALL
    SHOW SESSION SDWAN DETAIL
    SHOW INTERFACE PORT STATISTICS BRIEF
    SHOW COMMIT CHANGES 0
#    Debug
    CPE1.req_clr_stats_cos_qos_plcy_all
    CPE1.show_config_cos_qos_policy_rules
    CPE1.show_cos_qos_policy_rules
    sleep  10s
    spirent1.Start Stream Traffic   ${premium_tcp_stream1['stream_id']}
    spirent1.Start Stream Traffic   ${business1_tcp_stream1['stream_id']}
    spirent1.Start Stream Traffic   ${business2_tcp_stream1['stream_id']}
    spirent1.Start Stream Traffic   ${business3_tcp_stream1['stream_id']}
    spirent1.Start Stream Traffic   ${internet_default_tcp_stream1['stream_id']}
    sleep    10s
    SHOW INTERFACE PORT STATISTICS BRIEF
    ${result}  CPE1.show_cos_qos_policy_rules
    Log To Console  ${result}
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Premium\\s+1
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business1\\s+1
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business2\\s+1
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business3\\s+1
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Internet-Default\\s+(\\d{1})

    spirent1.stop_stream_traffic    ${premium_tcp_stream1['stream_id']}
    spirent1.stop_stream_traffic    ${business1_tcp_stream1['stream_id']}
    spirent1.stop_stream_traffic    ${business2_tcp_stream1['stream_id']}
    spirent1.stop_stream_traffic    ${business3_tcp_stream1['stream_id']}
    spirent1.stop_stream_traffic    ${internet_default_tcp_stream1['stream_id']}


NV_SINGLE_CPE_MPLS_ONLY_QOS_02
    [Documentation]    Source IP address Based QOS
    [Tags]    QOS
    VD1.modify_qos_device_config    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    qos_ip_based_premium.j2    src_address_obj=${ipaddobj_1}
    VD1.move_qos_policy_rule    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    Default-Policy    LAN1-VRF-Premium    first
    sleep    10s
#    Debug
    REQ CLR SESSION ALL
    SHOW SESSION SDWAN DETAIL
    SHOW INTERFACE PORT STATISTICS BRIEF
    SHOW COMMIT CHANGES 0
#    Debug
    CPE1.show_config_object_addresses    ${ipaddobj_1}
    CPE1.req_clr_stats_cos_qos_plcy_all
    CPE1.show_config_cos_qos_policy_rules
    CPE1.show_cos_qos_policy_rules
    sleep  10s
    spirent1.Start Stream Traffic   ${stream1['stream_id']}
    sleep    10s
    SHOW INTERFACE PORT STATISTICS BRIEF
    ${result}  CPE1.show_cos_qos_policy_rules
    Log To Console  ${result}
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Premium\\s+1
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business1\\s+0
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business2\\s+0
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business3\\s+0
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Internet-Default\\s+(\\d{1})
    spirent1.stop_stream_traffic    ${stream1['stream_id']}
    VD1.modify_qos_device_config    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    revert_qos_ip_based_premium.j2    src_address_obj=${ipaddobj_1}
    VD1.move_qos_policy_rule    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    Default-Policy    LAN1-VRF-Premium    first

NV_SINGLE_CPE_MPLS_ONLY_QOS_03
    [Documentation]    Destination IP address Based QOS
    [Tags]    QOS
    VD1.modify_qos_device_config    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    qos_ip_based_premium.j2    dst_address_obj=${ipaddobj_2}
    VD1.move_qos_policy_rule    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    Default-Policy    LAN1-VRF-Premium    first
    sleep  10s
    REQ CLR SESSION ALL
    SHOW SESSION SDWAN DETAIL
    SHOW INTERFACE PORT STATISTICS BRIEF
    SHOW COMMIT CHANGES 0
#    Debug
    CPE1.show_config_object_addresses    ${ipaddobj_2}
    CPE1.req_clr_stats_cos_qos_plcy_all
    CPE1.show_config_cos_qos_policy_rules
    CPE1.show_cos_qos_policy_rules
    sleep  10s
    spirent1.Start Stream Traffic   ${stream1['stream_id']}
    sleep    10s
    SHOW INTERFACE PORT STATISTICS BRIEF
    ${result}  CPE1.show_cos_qos_policy_rules
    Log To Console  ${result}
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Premium\\s+1
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business1\\s+0
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business2\\s+0
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Business3\\s+0
    CHECK RESULT     actual=${result}    expected=LAN1-VRF-Internet-Default\\s+(\\d{1})
    spirent1.stop_stream_traffic    ${stream1['stream_id']}
    VD1.modify_qos_device_config    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    revert_qos_ip_based_premium.j2    dst_address_obj=${ipaddobj_2}
    VD1.move_qos_policy_rule    ${CPE1['Device_name']}    ${cpe1['ORG_NAME']}    Default-Policy    LAN1-VRF-Premium    first


*** Keywords ***
REQ CLR SESSION ALL
    ${result}   CPE1.req_clr_sess_all
    Log To Console  ${result}

SHOW INTERFACE PORT STATISTICS BRIEF
    ${result}   CPE1.show_intf_port_stats_br
    Log To Console  ${result}

SHOW SESSION SDWAN DETAIL
    ${result}   CPE1.show_session_sdwan_detail
    Log To Console  ${result}

SHOW COMMIT CHANGES 0
    ${result}   CPE1.show_commit_changes_0
    Log To Console  ${result}


CHECK MPLS WAN INTERFACE UP in CPE1
    ${result}=    CPE1.get interface status    intf_name=${CPE1['WAN1_INTF']}${unit_o} | match MPLS
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2    up not presnt 2 times

CHECK INTERNET WAN INTERFACE UP in CPE3
    ${result}=    CPE3.get interface status    intf_name=${CPE3['WAN1_INTF']}${unit_o} | match INT
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK MPLS WAN INTERFACE UP in CPE2
    ${result}=    CPE2.get interface status    intf_name=${CPE2['WAN1_INTF']}${unit_o} | match MPLS
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK INTERNET WAN INTERFACE UP in CPE2
    ${result}=    CPE2.get interface status    intf_name=${CPE2['WAN2_INTF']}${unit_o} | match INT
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2


CHECK WC1 BGP NEIGHBOR STATUS in CPE1 & CPE2 and CPE3
    ${result}=    CPE1.get bgp nbr status    nbr_ip=${CPE1['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE2.get bgp nbr status    nbr_ip=${CPE2['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE3.get bgp nbr status    nbr_ip=${CPE3['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}

CHECK WC2 BGP NEIGHBOR STATUS in CPE1 & CPE2 and CPE3
    ${result}=    CPE1.get bgp nbr status    nbr_ip=${CPE1['WC2_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE2.get bgp nbr status    nbr_ip=${CPE2['WC2_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE3.get bgp nbr status    nbr_ip=${CPE3['WC2_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}


CHECK WC1 PTVI INTERFACE STATUS in CPE1
    ${result}=    CPE1.get interface status    intf_name=${CPE1['ptvi_intf_wc1']}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK WC2 PTVI INTERFACE STATUS in CPE1
    ${result}=    CPE1.get interface status    intf_name=${CPE1['ptvi_intf_wc2']}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK WC1 PTVI INTERFACE STATUS in CPE2
    ${result}=    CPE2.get interface status    intf_name=${CPE2['ptvi_intf_wc1']}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK WC2 PTVI INTERFACE STATUS in CPE2
    ${result}=    CPE2.get interface status    intf_name=${CPE2['ptvi_intf_wc2']}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK WC1 PTVI INTERFACE STATUS in CPE3
    ${result}=    CPE3.get interface status    intf_name=${CPE3['ptvi_intf_wc1']}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK WC2 PTVI INTERFACE STATUS in CPE3
    ${result}=    CPE3.get interface status    intf_name=${CPE3['ptvi_intf_wc2']}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2


CHECK CPE2 LAN ROUTE Present in CPE1
    ${result}=    CPE1.check lan route    lan=1
    #    log to console    ${result}
    ${active_dest_route} =    Convert To String    \\+${CPE2['lan'][1]['nw']}\\s+${CPE2['ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${active_dest_route}

CHECK CPE3 LAN ROUTE Present in CPE1
    ${result}=    CPE1.check lan route    lan=1
    #    log to console    ${result}
    ${active_dest_route} =    Convert To String    \\+${CPE3['lan'][1]['nw']}\\s+${CPE3['GW1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${active_dest_route}

CHECK CPE1 LAN ROUTE Present in CPE2
    ${result}=    CPE2.check lan route    lan=1
    ${active_dest_route} =    Convert To String    \\+${CPE1['lan'][1]['nw']}\\s+${CPE1['ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${active_dest_route}

CHECK CPE1 LAN ROUTE Present in CPE3
    ${result}=    CPE3.check lan route    lan=1
    ${active_dest_route} =    Convert To String    \\+${CPE1['lan'][1]['nw']}\\s+${CPE1['GW1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${active_dest_route}

STARTUP
    [Documentation]    Make connecection to Versa devices
    VD1.login
    ${VD1}    VD1.get_data_dict
    set suite variable    ${VM1}
    set suite variable    ${VM2}
    set suite variable    ${VM3}
    CPE1.cross login
    CPE2.cross_login
    CPE3.cross_login
#    Debug
    spirent1.Connect And Reserve Ports
    ${CPE1_dev_info_on_vd} =    CPE1.get_device_info
    ${CPE1}    CPE1.get_data_dict
    ${CPE2}    CPE2.get_data_dict
    ${CPE3}    CPE3.get_data_dict
    CPE1.Create_Controller_List    ${CPE1['ORG_NAME']}    ${CPE1['ORG_ID']}    ${CPE1['NO_OF_VRFS']}    ${CPE1['NODE']}
    CPE1.Create_Gateway_List    ${CPE1['ORG_NAME']}    ${CPE1['ORG_ID']}    ${CPE1['NO_OF_VRFS']}    ${CPE1['NODE']}
    CPE1.create_cpe_data
    CPE2.Create_Controller_List    ${CPE2['ORG_NAME']}    ${CPE2['ORG_ID']}    ${CPE2['NO_OF_VRFS']}    ${CPE2['NODE']}
    CPE2.Create_Gateway_List    ${CPE2['ORG_NAME']}    ${CPE2['ORG_ID']}    ${CPE2['NO_OF_VRFS']}    ${CPE2['NODE']}
    CPE2.create_cpe_data
    CPE3.Create_Controller_List    ${CPE3['ORG_NAME']}    ${CPE3['ORG_ID']}    ${CPE3['NO_OF_VRFS']}    ${CPE3['NODE']}
    CPE3.Create_Gateway_List    ${CPE3['ORG_NAME']}    ${CPE3['ORG_ID']}    ${CPE3['NO_OF_VRFS']}    ${CPE3['NODE']}
    CPE3.create_cpe_data
    ${CPE1}    CPE1.get_data_dict
    set suite variable    ${CPE1}
    ${CPE2}    CPE2.get_data_dict
    set suite variable    ${CPE2}
    ${CPE3}    CPE3.get_data_dict
    set suite variable    ${CPE3}
    #log variables
    #####VM preops #####
    VM1.VM_pre_op
    VM2.VM_pre_op
    VM3.VM_pre_op
    ${VM1}    VM1.get_data_dict
    ${VM2}    VM2.get_data_dict
    ${VM3}    VM3.get_data_dict
    set suite variable    ${VM1}
    set suite variable    ${VM2}
    set suite variable    ${VM3}
    : FOR    ${i}    IN RANGE    1    ${VM1['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM1['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM1['lan'][${i}]['vlan']}
    \    ${destination_nw1} =    set variable    ${VM2['lan'][${i}]['nw']}
    \    VM1.send_commands_and_expect    sudo ip route add ${destination_nw1} via ${gw} dev ${VM1['LAN_INTF']}.${vlan}
    \    ${destination_nw2} =    set variable    ${VM3['lan'][${i}]['nw']}
    \    VM1.send_commands_and_expect    sudo ip route add ${destination_nw2} via ${gw} dev ${VM1['LAN_INTF']}.${vlan}
    : FOR    ${i}    IN RANGE    1    ${VM2['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM2['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM2['lan'][${i}]['vlan']}
    \    ${destination_nw} =    set variable    ${VM1['lan'][${i}]['nw']}
    \    VM2.send_commands_and_expect    sudo ip route add ${destination_nw} via ${gw} dev ${VM2['LAN_INTF']}.${vlan}
    : FOR    ${i}    IN RANGE    1    ${VM3['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM3['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM3['lan'][${i}]['vlan']}
    \    ${destination_nw} =    set variable    ${VM1['lan'][${i}]['nw']}
    \    VM3.send_commands_and_expect    sudo ip route add ${destination_nw} via ${gw} dev ${VM3['LAN_INTF']}.${vlan}

    ###########spirent ###########
    SPIRENT_STARTUP
    CPE1.create_address_object    ${ipaddobj_1}    ipv4-prefix    ${CPE1['lan'][1]['third_host']}/32
    CPE1.create_address_object    ${ipaddobj_2}    ipv4-prefix    ${CPE2['lan'][1]['third_host']}/32
    CPE1.create_service_object    ${serviceobj_1}    ${TCP}    source_port=2000
    VD1.config_devices_qos    ${CPE1['Device_name']}    ${CPE1['ORG_NAME']}    ${CPE1['WAN1_INTF']}

SPIRENT_STARTUP
    ${device1}    spirent1.Create Device    port=0    vlanid=${CPE1['lan'][1]['vlan']}    intf_ip_addr=${CPE1['lan'][1]['third_host']}    gateway_ip_addr=${CPE1['lan'][1]['first_host']}
    ${device2}    spirent1.Create Device    port=1    vlanid=${CPE2['lan'][1]['vlan']}    intf_ip_addr=${CPE2['lan'][1]['third_host']}    gateway_ip_addr=${CPE2['lan'][1]['first_host']}
    ${stream1}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=2000    rate_mbps=2
    ${stream2}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=2001    rate_mbps=2
    ${stream3}    spirent1.Create Udp Stream Block   ${device1}    ${device2}    src_port=2002    rate_mbps=2
    ${premium_tcp_stream1}          spirent1.create_tcp_stream_block   ${device1}     ${device2}    src_port=3001     rate_mbps=1     ip_dscp=46
    ${business1_tcp_stream1}        spirent1.create_tcp_stream_block   ${device1}     ${device2}    src_port=3002     rate_mbps=1     ip_dscp=26
    ${business2_tcp_stream1}        spirent1.create_tcp_stream_block   ${device1}     ${device2}    src_port=3003     rate_mbps=1     ip_dscp=18
    ${business3_tcp_stream1}        spirent1.create_tcp_stream_block   ${device1}     ${device2}    src_port=3004     rate_mbps=1     ip_dscp=10
    ${internet_default_tcp_stream1}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=5000    rate_mbps=1
    
    set suite variable    ${device1}
    set suite variable    ${device2}
    set suite variable    ${stream1}
    set suite variable    ${stream2}
    set suite variable    ${stream3}
    set suite variable    ${premium_tcp_stream1}
    set suite variable    ${business1_tcp_stream1}
    set suite variable    ${business2_tcp_stream1}
    set suite variable    ${business3_tcp_stream1}
    set suite variable    ${internet_default_tcp_stream1}




CLEANUP
    log to console    "cleanup done"
    CPE1.delete_service_object    ${serviceobj_1}
    CPE1.delete_address_object    ${ipaddobj_1}
    CPE1.delete_address_object    ${ipaddobj_2}
    spirent1.release_ports
    : FOR    ${i}    IN RANGE    1    ${VM1['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM1['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM1['lan'][${i}]['vlan']}
    \    ${destination_nw} =    set variable    ${VM2['lan'][${i}]['nw']}
    \    VM1.send_commands_and_expect    sudo ip route del ${destination_nw} via ${gw} dev ${VM1['LAN_INTF']}.${vlan}
    : FOR    ${i}    IN RANGE    1    ${VM2['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM2['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM2['lan'][${i}]['vlan']}
    \    ${destination_nw} =    set variable    ${VM1['lan'][${i}]['nw']}
    \    VM2.send_commands_and_expect    sudo ip route del ${destination_nw} via ${gw} dev ${VM2['LAN_INTF']}.${vlan}

CHECK RESULT1
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log    ${actual}
    log    ${expected}
    Run Keyword And Continue On Failure    should contain    ${actual}    ${expected}

CHECK RESULT
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log    ${actual}
    log    ${expected}
    Run Keyword And Continue On Failure    should match regexp    ${actual}    ${expected}


Ping Test VM1 to VM2(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM2['lan'][1]['second_host']}
    ${result}=    VM1.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM1 to VM3(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM3['lan'][1]['second_host']}
    ${result}=    VM1.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM1 to VM2(ALL LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    1    ${VM1['NO_OF_VRFS']} + 1
    \    ${destip}=    set variable    ${VM2['lan'][${vlan}]['second_host']}
    \    #    log to console    ${destip}
    \    ${result}=    VM1.Shell Ping    ${destip}
    \    CHECK RESULT    actual=${result}

Ping Test VM2 to VM1(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM1['lan'][1]['second_host']}
    ${result}=    VM2.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM3 to VM1(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM1['lan'][1]['second_host']}
    ${result}=    VM3.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM2 to VM1(ALL LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    1    ${VM2['NO_OF_VRFS']} + 1
    \    ${destip}=    set variable    ${VM1['lan'][${vlan}]['second_host']}
    \    #    log to console    ${destip}
    \    ${result}=    VM1.Shell Ping    ${destip}
    \    CHECK RESULT    actual=${result}

Iperf3 test VM1 to VM2
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM2['lan'][1]['second_host']}
    VM2.send_commands_and_expect    pkill iperf3 &
    sleep    10s
    VM2.send_commands_and_expect    iperf3 -s &
    ${result}=    VM1.send_commands_and_expect    iperf3 -c ${destip}
    Should Contain    ${result}    iperf Done.

Iperf3 test VM1 to VM3
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM3['lan'][1]['second_host']}
    VM3.send_commands_and_expect    pkill iperf3 &
    sleep    10s
    VM3.send_commands_and_expect    iperf3 -s &
    ${result}=    VM1.send_commands_and_expect    iperf3 -c ${destip}
    Should Contain    ${result}    iperf Done.