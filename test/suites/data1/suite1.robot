*** Settings ***
Resource      test_resource.robot

*** Variables ***
${FOO}                    FOO
${BAR}                    BAR

*** Keywords ***
First Keyword Example
  [Arguments]             ${msg}
  Import Library          Collections
  Log To Console          First Keyword Example: ${msg}


*** Test Cases ***
First Test Case
  First Keyword Example   ${FOO} vs ${BAR}

