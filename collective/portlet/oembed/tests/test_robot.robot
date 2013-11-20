*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Assert: I can hit the home page
    Given I'm not loggedin
      And I'm on the home page

*** Keywords ***

#LOGIN / LOGOUT
I'm not loggedin
    Go to  ${PLONE_URL}/logout

I'm loggedin as a test user
    Log in as test user

I'm loggedin as the site owner
    Log in as site owner

#LOCATIONS
I'm on the home page
    Go to  ${PLONE_URL}
