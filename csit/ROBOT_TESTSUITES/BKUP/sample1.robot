*** Settings ***
Library           DebugLibrary
Library           ../../libraries/HltapiLib.py    10.91.113.124    10/1    10/2    WITH NAME    spirent1


*** Variables ***
${expected}            \\+192.169.101.0/24\\s+20.20.90.11
${actual}   LAN1-VRF BGP N/A +192.169.101.0/24 20.20.90.11 Indirect



*** Test Cases ***
Checking_test
    spirent1.Connect And Reserve Ports
    sleep    10s
    ${result}   Run Keyword And Continue On Failure    should match regexp    ${actual}    ${expected}
    log to console    ${result}
    spirent1.release_ports




*** Keywords ***
CHECK RESULT REGEXP
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log    ${actual}
    log    ${expected}
    Run Keyword And Continue On Failure    should contain    ${actual}    ${expected}