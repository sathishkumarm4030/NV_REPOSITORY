*** Settings ***
Library           DebugLibrary


*** Variables ***
${expected}            \\+192.169.101.0/24\\s+20.20.90.11
${actual}   LAN1-VRF BGP N/A +192.169.101.0/24 20.20.90.11 Indirect



*** Test Cases ***
Checking_test
    ${result}   Run Keyword And Continue On Failure    should match regexp    ${actual}    ${expected}
    log to console    ${result}



*** Keywords ***
CHECK RESULT REGEXP
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log    ${actual}
    log    ${expected}
    Run Keyword And Continue On Failure    should contain    ${actual}    ${expected}