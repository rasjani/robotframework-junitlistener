*** Settings ***
Resource      test_resource.robot

*** Variables ***
${FOO}                    FOO
${BAR}                    BAR

*** Keywords ***
Second Keyword Example
  [Arguments]             ${msg}
  Log To Console          Second Keyword Example: ${msg}


*** Test Cases ***
Second Test Case
  Second Keyword Example   ${FOO} vs ${BAR}

Third Test Case
  Second Keyword Example   ${FOO} vs ${BAR} for the second time
  FAIL

