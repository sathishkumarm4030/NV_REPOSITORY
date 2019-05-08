*** Settings ***
Documentation     A test suite with tests for SDWAN HYBRID Solution.
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
...               1. CHECK IF IP ADDRESS IS SET AND INTERFACE IS UP.
Suite Setup       STARTUP
Suite Teardown    CLEANUP
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ../libraries/Variables.py
Library           Collections
Library           String
Library           ../libraries/VersaLib.py    CPE11-BLR-HYBRID    topofile=Devices.csv    WITH NAME    CPE1
Library           ../libraries/VersaLib.py    CPE12-BLR-MPLS    topofile=Devices.csv    WITH NAME    CPE2
Library           ../libraries/LinuxLib.py    CPE11_LAN_HOST1    topofile=VM_Devices.csv    WITH NAME    VM1
Library           ../libraries/LinuxLib.py    CPE12_LAN_HOST1    topofile=VM_Devices.csv    WITH NAME    VM2

*** Variables ***
${Topo_file}      ${CURDIR}/../Topology/Devices.csv
${j2_templates_path}    ${CURDIR}/../libraries/J2_temps
${PST}            Post_staging_template.j2
${est}            Established

*** Test Cases ***
Testcase: CHECK WAN INTERFACES STATUS
    ${result}=    CPE1.get interface status    intf_name=${CPE1['ptvi_intf_wc1']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE1.get interface status    intf_name=${CPE1['ptvi_intf_wc2']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE2.get interface status    intf_name=${CPE2['ptvi_intf_wc1']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE2.get interface status    intf_name=${CPE2['ptvi_intf_wc2']}
    CHECK RESULT    actual=${result}    expected=up

Testcase: CHECK BGP NEIGHBOR STATUS
    ${result}=    CPE1.get bgp nbr status    nbr_ip=${CPE1['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE1.get bgp nbr status    nbr_ip=${CPE1['WC2_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}

Testcase: CHECK LAN ROUTE
    [Tags]    LAN
    ${result}=    CPE1.check lan route    lan=1
    ${dest_route} =    Convert To String    ${CPE2['lan'][1]['nw']}
    CHECK RESULT    actual=${result}    expected=${dest_route}
    ${result}=    CPE2.check lan route    lan=1
    ${dest_route} =    Convert To String    ${CPE1['lan'][1]['nw']}
    CHECK RESULT    actual=${result}    expected=${dest_route}


Testcase: Ping Test VM1 To VM2(1 LAN)
    [Tags]    PING
    Ping Test VM1 To VM2(1 LAN)

Testcase: Ping Test VM2 To VM1(1 LAN)
    [Tags]    PING
    Ping Test VM2 To VM1(1 LAN)

Testcase: Ping Test VM1 To VM2(10 LANS)
    [Tags]    PING
    Ping Test VM1 To VM2(10 LANS)

Testcase: Ping Test VM2 To VM1(10 LANS)
    [Tags]    PING
    Ping Test VM2 To VM1(10 LANS)

Testcase: Iperf3 Test VM1 To VM2
    [Tags]    IPERF
    Iperf3 Test VM1 To VM2

*** Keywords ***
STARTUP
    [Documentation]    Make connecection to Versa devices
    CPE1.cross login
    CPE2.cross_login
    ${CPE1_dev_info_on_vd} =    CPE1.get_device_info
    #    CPE1.set_variable    Solution_type    SINGLE-CPE-HYBRID
    #    CPE2.set_variable    Solution_type    SINGLE-CPE-MPLS-ONLY
    log to console    ${CPE1_dev_info_on_vd}
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
    log variables
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
    log to console    "sasasa"

CHECK RESULT
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log to console    ${actual}
    log to console    ${expected}
    Run Keyword And Continue On Failure    should contain    ${actual}    ${expected}

Ping Test VM1 to VM2(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM2['lan'][1]['second_host']}
    ${result}=    VM1.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM1 to VM2(10 LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    1    ${VM1['NO_OF_VRFS']} + 1
    \    ${destip}=    set variable    ${VM2['lan'][${vlan}]['second_host']}
    \    log to console    ${destip}
    \    ${result}=    VM1.Shell Ping    ${destip}
    \    CHECK RESULT    actual=${result}

Ping Test VM2 to VM1(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${VM1['lan'][1]['second_host']}
    ${result}=    VM2.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM2 to VM1(10 LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    1    ${VM2['NO_OF_VRFS']} + 1
    \    ${destip}=    set variable    ${VM1['lan'][${vlan}]['second_host']}
    \    log to console    ${destip}
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
