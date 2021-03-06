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
Library           ../libraries/VersaLib.py    ${CPE1}    topofile=Devices.csv    WITH NAME    CPE1
Library           ../libraries/VersaLib.py    ${CPE2}    topofile=Devices.csv    WITH NAME    CPE2
Library           ../libraries/LinuxLib.py    ${VM1}    topofile=VM_Devices.csv    WITH NAME    VM1
Library           ../libraries/LinuxLib.py    ${VM2}    topofile=VM_Devices.csv    WITH NAME    VM2

*** Variables ***
${est}            Established
${unit_o}         .0
${up}             up

*** Test Cases ***
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
    CPE1.cross login
    CPE2.cross_login
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

CLEANUP
    log to console    "cleanup done"

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
