Feature: Test registration and login/logout workflow
  Scenario: Successful registration
    Given There are no other users with the same name
    When I send correct register credentials
    Then I successfully register a new user