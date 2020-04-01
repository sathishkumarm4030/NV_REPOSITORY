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
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ../libraries/Variables.py
Library           Collections
Library           String
Variables         SINGLE_CPE_SOLUTION_TEST_TOPOLOGY.py
Library           DebugLibrary
Library           ../libraries/HltapiLib.py    ${Spirent_Spec1[0]}    ${Spirent_Spec1[1]}    ${Spirent_Spec1[2]}    WITH NAME    spirent1

*** Variables ***
${est}            Established
${unit_o}         .0
${up}             up

*** Test Cases ***
NV_SINGLE_CPE_TRAFFIC_STEERING_01
    [Documentation]    Traffic steering based on Source IP
    [Tags]    P1
    spirent1.Connect And Reserve Ports
    ${device1}    spirent1.Create Device    port=0    vlanid=600    intf_ip_addr=192.169.101.3    gateway_ip_addr=192.169.101.1
    ${device2}    spirent1.Create Device    port=1    vlanid=610    intf_ip_addr=192.169.111.3    gateway_ip_addr=192.169.111.1
    ${stream111}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=3180    rate_mbps=2
    ${stream222}    spirent1.Create Tcp Stream Block   ${device1}    ${device2}    src_port=4101    rate_mbps=2
    Debug
    spirent1.Start Stream Traffic   ${stream111['stream_id']}
    sleep    40s
    spirent1.Start Stream Traffic    ${stream222['stream_id']}
    sleep    40s


