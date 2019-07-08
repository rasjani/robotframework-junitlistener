*** Settings ***
Resource      ../data1/test_resource.robot
Documentation   Does this get overwritten somehow
MetaData        Version   1.0
MetaData        RF        3.1.2

*** Variables ***
${FOO}                    FOO
${BAR}                    BAR

*** Keywords ***
Dummy Keyword
  [Arguments]             ${msg}
  [Tags]                  working
  Log To Console          Dummy Keyword: ${msg}


*** Test Cases ***
Fourth Test Case
  [Tags]                  working
  Dummy Keyword           ${FOO} vs ${BAR}

