*** Settings ***
Resource      test_resource.robot

*** Variables ***
${FOO}                    FOO
${BAR}                    BAR

*** Keywords ***
First Keyword Example
  [Arguments]             ${msg}
  Log To Console          First Keyword Example: ${msg}


*** Test Cases ***
First Test Case
  First Keyword Example   ${FOO} vs ${BAR}

