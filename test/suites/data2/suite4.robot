*** Settings ***
Resource      test_resource.robot
Library       String
Documentation   Some sort of docs would appear in the junit format also as properties

*** Variables ***
${FOO}                    FOO
${BAR}                    BAR

*** Keywords ***
Another Dummy
  [Arguments]             ${msg}
  Log To Console          Another Dummy: ${msg}


*** Test Cases ***
Fifth Test Case
  [Tags]                  working
  Another Dummy           ${FOO} vs ${BAR}

Sixth Test Case
  [Tags]                  notworking
  Should Be Equal         ${FOO}    ${BAR}

Seventh Test Case
  [Tags]                  not-working
  non existing keyword     foofofo   fofof
