*** Settings ***
Documentation     A test suite with tests for SDWAN SINGLE CPE Solution.
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
Suite Setup       STARTUP
Suite Teardown    CLEANUP
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ../libraries/Variables.py
Library           Collections
Library           String
Variables         SINGLE_CPE_SOLUTION_TEST_TOPOLOGY.py
Library           ../libraries/VersaLib.py    VD1    topofile=Devices.csv    WITH NAME    VD1
Library           ../libraries/VersaLib.py    ${CPE1}    topofile=Devices.csv    WITH NAME    CPE1
Library           ../libraries/VersaLib.py    ${CPE2}    topofile=Devices.csv    WITH NAME    CPE2
Library           ../libraries/LinuxLib.py    ${VM1}    topofile=VM_Devices.csv    WITH NAME    VM1
Library           ../libraries/LinuxLib.py    ${VM2}    topofile=VM_Devices.csv    WITH NAME    VM2
Library           ../libraries/HltapiLib.py    ${Spirent_chasis1[0]}    ${Spirent_chasis1[1]}    ${Spirent_chasis1[2]}    WITH NAME    spirent1
Library           DebugLibrary

*** Variables ***
${est}            Established
${unit_o}         .0
${up}             up
${bw}             30000

*** Test Cases ***
NV_SINGLE_CPE_TRAFFIC_STEERING_01
    [Documentation]    Traffic steering based on Source IP
    [Tags]    P1
    CPE1.create_policy_rule    ${plcyrule_1}    ${fwp_1}    src_address_obj=${ipaddobj_1}
    VD1.move_policy_rule  ${CPE1['Device_name']}       ${cpe1['ORG_NAME']}    Default-Policy      ${plcyrule_1}    first
    ${result}   CPE1.req_clr_sess_all
    Log To Console  ${result}

    spirent1.Start Stream Traffic   ${stream1['stream_id']}
    sleep    40s
    spirent1.Start Stream Traffic    ${stream2['stream_id']}
    sleep    40s
    spirent1.Start Stream Traffic    ${stream3['stream_id']}
    sleep    40s
    ${result}   CPE1.show_session_sdwan_detail  source_port=2000
    CHECK RESULT    actual=${result}    expected=tx-wan-ckt${SPACE*17}${CPE1['WAN1_NAME']}
    CHECK RESULT    actual=${result}    expected=sdwan-rule-name${SPACE*12}${plcyrule_1}

    ${result}   CPE1.show_session_sdwan_detail    source_port=2001
    CHECK RESULT    actual=${result}    expected=tx-wan-ckt${SPACE*17}${CPE1['WAN2_NAME']}
    CHECK RESULT    actual=${result}    expected=sdwan-rule-name${SPACE*12}${plcyrule_1}

    ${result}   CPE1.show_session_sdwan_detail    source_port=2002
    CHECK RESULT    actual=${result}    expected=tx-wan-ckt${SPACE*17}${CPE1['WAN2_NAME']}
    CHECK RESULT    actual=${result}    expected=sdwan-rule-name${SPACE*12}${plcyrule_1}

    spirent1.stop_stream_traffic    ${stream3['stream_id']}
    spirent1.stop_stream_traffic    ${stream2['stream_id']}
    spirent1.stop_stream_traffic    ${stream1['stream_id']}

    CPE1.delete_policy_rule    ${plcyrule_1}

NV_SINGLE_CPE_TRAFFIC_STEERING_02
    [Documentation]    Traffic steering based on Destination IP
    [Tags]    P1
    CPE1.create_policy_rule    ${plcyrule_1}    ${fwp_1}    dest_address_obj=${ipaddobj_2}
    VD1.move_policy_rule  ${CPE1['Device_name']}       ${cpe1['ORG_NAME']}    Default-Policy      ${plcyrule_1}    first
    ${result}   CPE1.req_clr_sess_all
    Log To Console  ${result}
    spirent1.Start Stream Traffic   ${stream1['stream_id']}
    sleep    40s
    spirent1.Start Stream Traffic    ${stream2['stream_id']}
    sleep    40s
    spirent1.Start Stream Traffic    ${stream3['stream_id']}
    sleep    40s
    ${result}   CPE1.show_session_sdwan_detail  source_port=2000
    CHECK RESULT    actual=${result}    expected=tx-wan-ckt${SPACE*17}${CPE1['WAN1_NAME']}
    CHECK RESULT    actual=${result}    expected=sdwan-rule-name${SPACE*12}${plcyrule_1}

    ${result}   CPE1.show_session_sdwan_detail    source_port=2001
    CHECK RESULT    actual=${result}    expected=tx-wan-ckt${SPACE*17}${CPE1['WAN2_NAME']}
    CHECK RESULT    actual=${result}    expected=sdwan-rule-name${SPACE*12}${plcyrule_1}

    ${result}   CPE1.show_session_sdwan_detail    source_port=2002
    CHECK RESULT    actual=${result}    expected=tx-wan-ckt${SPACE*17}${CPE1['WAN2_NAME']}
    CHECK RESULT    actual=${result}    expected=sdwan-rule-name${SPACE*12}${plcyrule_1}

    spirent1.stop_stream_traffic    ${stream3['stream_id']}
    spirent1.stop_stream_traffic    ${stream2['stream_id']}
    spirent1.stop_stream_traffic    ${stream1['stream_id']}

    CPE1.delete_policy_rule    ${plcyrule_1}

NV_SINGLE_CPE_HYBRID_SANITY_01
    [Documentation]    SANITY CHECKS on vCPE
    [Tags]    SANITY
    CHECK MPLS WAN INTERFACE UP in CPE1 & CPE2
    CHECK INTERNET WAN INTERFACE UP in CPE1 & CPE2
    CHECK WC1 PTVI INTERFACE STATUS in CPE1
    CHECK WC2 PTVI INTERFACE STATUS in CPE2
    CHECK WC1 PTVI INTERFACE STATUS in CPE1
    CHECK WC2 PTVI INTERFACE STATUS in CPE2
    CHECK WC1 BGP NEIGHBOR STATUS in CPE1 & CPE2
    CHECK WC2 BGP NEIGHBOR STATUS in CPE1 & CPE2
    CHECK CPE2 LAN ROUTE Present in CPE1
    CHECK CPE1 LAN ROUTE Present in CPE2

NV_SINGLE_CPE_HYBRID_SANITY_02
    [Documentation]    Ping test CPE1 LAN1 VM to CPE2 LAN1 VM
    [Tags]    PING
    Ping Test VM1 To VM2(1 LAN)
    Ping Test VM2 To VM1(1 LAN)

NV_SINGLE_CPE_HYBRID_SANITY_03
    [Documentation]    Ping test CPE1 ALL LAN VM to CPE2 ALL LAN VM
    [Tags]    PING
    Ping Test VM1 To VM2(ALL LANS)
    Ping Test VM2 To VM1(ALL LANS)

NV_SINGLE_CPE_HYBRID_SANITY_04
    [Documentation]    Iperf test VM1 to VM2
    [Tags]    IPERF
    Iperf3 Test VM1 To VM2

*** Keywords ***
CREATE FWD PROFILE
    ${curr_intf_bw}    CPE1.get_vni_interface_bw    ${CPE1['WAN1_INTF']}
    set suite variable  ${curr_intf_bw}
    CPE1.modify_interface_bandwidth   ${CPE1['WAN1_INTF']}    ${bw}    ${bw}
    CPE1.get_vni_interface_bw    ${CPE1['WAN1_INTF']}
    CPE1.create_sla_profile    ${sla_prf_1}    circuit_transmit_utilization=5
    CPE1.create_fowarding_profile    ${fwp_1}    ${CPE1['WAN1_NAME']}    ${CPE1['WAN2_NAME']}    sla_name=${sla_prf_1}    evaluate_continuously=disable
    CPE1.create_address_object    ${ipaddobj_1}    ipv4-prefix    ${CPE1['lan'][1]['third_host']}/32
    CPE1.create_address_object    ${ipaddobj_2}    ipv4-prefix    ${CPE2['lan'][1]['third_host']}/32

DELETE FWD PROFILE
    CPE1.delete_address_object    ${ipaddobj_1}
    CPE1.delete_address_object    ${ipaddobj_2}
    CPE1.delete_fowarding_profile    ${fwp_1}
    CPE1.delete_sla_profile    ${sla_prf_1}
    CPE1.modify_interface_bandwidth    ${CPE1['WAN1_INTF']}    ${curr_intf_bw['bandwidth']['uplink']}    ${curr_intf_bw['bandwidth']['downlink']}
    CPE1.get_vni_interface_bw    ${CPE1['WAN1_INTF']}


CHECK MPLS WAN INTERFACE UP in CPE1 & CPE2
    ${result}=    CPE1.get interface status    intf_name=${CPE1['WAN1_INTF']}${unit_o} | match MPLS
    #CHECK RESULT    actual=${result}    expected=${up}
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2    up not presnt 2 times
    ${result}=    CPE2.get interface status    intf_name=${CPE2['WAN1_INTF']}${unit_o} | match MPLS
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK INTERNET WAN INTERFACE UP in CPE1 & CPE2
    ${result}=    CPE1.get interface status    intf_name=${CPE1['WAN2_INTF']}${unit_o} | match INT
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2
    ${result}=    CPE2.get interface status    intf_name=${CPE2['WAN2_INTF']}${unit_o} | match INT
    Run Keyword And Continue On Failure    Should Contain X Times    ${result}    ${up}    2

CHECK WC1 BGP NEIGHBOR STATUS in CPE1 & CPE2
    ${result}=    CPE1.get bgp nbr status    nbr_ip=${CPE1['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE2.get bgp nbr status    nbr_ip=${CPE2['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}

CHECK WC2 BGP NEIGHBOR STATUS in CPE1 & CPE2
    ${result}=    CPE1.get bgp nbr status    nbr_ip=${CPE1['WC2_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE2.get bgp nbr status    nbr_ip=${CPE2['WC2_ESP_IP']}
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

CHECK WAN INTERFACES STATUS in CPE1
    ${result}=    CPE1.get interface status    intf_name=${CPE1['ptvi_intf_wc1']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE1.get interface status    intf_name=${CPE1['ptvi_intf_wc2']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE2.get interface status    intf_name=${CPE2['ptvi_intf_wc1']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE2.get interface status    intf_name=${CPE2['ptvi_intf_wc2']}
    CHECK RESULT    actual=${result}    expected=up

CHECK CPE2 LAN ROUTE Present in CPE1
    ${result}=    CPE1.check lan route    lan=1
    #    log to console    ${result}
    ${active_dest_route} =    Convert To String    \+${CPE2['lan'][1]['nw']} ${CPE2['ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${active_dest_route}

CHECK CPE1 LAN ROUTE Present in CPE2
    ${result}=    CPE2.check lan route    lan=1
    ${active_dest_route} =    Convert To String    \+${CPE1['lan'][1]['nw']} ${CPE1['ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${active_dest_route}

STARTUP
    [Documentation]    Make connecection to Versa devices
    VD1.login
    ${VD1}    VD1.get_data_dict
    set suite variable    ${VM1}
    set suite variable    ${VM2}
    CPE1.cross login
    CPE2.cross_login
    spirent1.Connect And Reserve Ports
    ${CPE1_dev_info_on_vd} =    CPE1.get_device_info
    #    CPE1.set_variable    Solution_type    SINGLE-CPE-HYBRID
    #    CPE2.set_variable    Solution_type    SINGLE-CPE-MPLS-ONLY
    #    log to console    ${CPE1_dev_info_on_vd}
    ${CPE1}    CPE1.get_data_dict
    ${CPE2}    CPE2.get_data_dict
    CPE1.Create_Controller_List    ${CPE1['ORG_NAME']}    ${CPE1['ORG_ID']}    ${CPE1['NO_OF_VRFS']}    ${CPE1['NODE']}
    CPE1.Create_Gateway_List    ${CPE1['ORG_NAME']}    ${CPE1['ORG_ID']}    ${CPE1['NO_OF_VRFS']}    ${CPE1['NODE']}
    CPE1.create_cpe_data
    CPE2.Create_Controller_List    ${CPE2['ORG_NAME']}    ${CPE2['ORG_ID']}    ${CPE2['NO_OF_VRFS']}    ${CPE2['NODE']}
    CPE2.Create_Gateway_List    ${CPE2['ORG_NAME']}    ${CPE2['ORG_ID']}    ${CPE2['NO_OF_VRFS']}    ${CPE2['NODE']}
    CPE2.create_cpe_data
    ${CPE1}    CPE1.get_data_dict
    set suite variable    ${CPE1}
    ${CPE2}    CPE2.get_data_dict
    set suite variable    ${CPE2}
    #log variables
    #####VM preops #####
    VM1.VM_pre_op
    VM2.VM_pre_op
    ${VM1}    VM1.get_data_dict
    ${VM2}    VM2.get_data_dict
    set suite variable    ${VM1}
    set suite variable    ${VM2}
    : FOR    ${i}    IN RANGE    1    ${VM1['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM1['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM1['lan'][${i}]['vlan']}
    \    ${destination_nw} =    set variable    ${VM2['lan'][${i}]['nw']}
    \    VM1.send_commands_and_expect    sudo ip route add ${destination_nw} via ${gw} dev ${VM1['LAN_INTF']}.${vlan}
    : FOR    ${i}    IN RANGE    1    ${VM2['NO_OF_VRFS']} + 1
    \    ${gw} =    set variable    ${VM2['lan'][${i}]['first_host']}
    \    ${vlan} =    set variable    ${VM2['lan'][${i}]['vlan']}
    \    ${destination_nw} =    set variable    ${VM1['lan'][${i}]['nw']}
    \    VM2.send_commands_and_expect    sudo ip route add ${destination_nw} via ${gw} dev ${VM2['LAN_INTF']}.${vlan}
    ###########spirent ###########
    SPIRENT_STARTUP
    CREATE FWD PROFILE

SPIRENT_STARTUP
    ${device1}    spirent1.Create Device    port=0    vlanid=${CPE1['lan'][1]['vlan']}    intf_ip_addr=${CPE1['lan'][1]['third_host']}    gateway_ip_addr=${CPE1['lan'][1]['first_host']}
    ${device2}    spirent1.Create Device    port=1    vlanid=${CPE2['lan'][1]['vlan']}    intf_ip_addr=${CPE2['lan'][1]['third_host']}    gateway_ip_addr=${CPE2['lan'][1]['first_host']}
    ${stream1}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=2000    rate_mbps=2
    ${stream2}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=2001    rate_mbps=2
    ${stream3}    spirent1.Create Udp Stream Block   ${device1}    ${device2}    src_port=2002    rate_mbps=2
    set suite variable    ${device1}
    set suite variable    ${device2}
    set suite variable    ${stream1}
    set suite variable    ${stream2}
    set suite variable    ${stream3}

CLEANUP
    DELETE FWD PROFILE
    log to console    "cleanup done"
    spirent1.release_ports
    sleep    40s

CHECK RESULT
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log    ${actual}
    log    ${expected}
    Run Keyword And Continue On Failure    should contain    ${actual}    ${expected}

Ping Test VM1 to VM2(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM2['lan'][1]['second_host']}
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
