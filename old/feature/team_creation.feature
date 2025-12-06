Feature: Team creation
  As a player
  I want to create a team
  So that I can collect cards and play matches

  Background:
    Given the blockchain is running

  Scenario: Create a new team successfully
    Given I have an account with address "0xPLAYER1"
    When I create a team for "0xPLAYER1"
    Then the team for "0xPLAYER1" exists
    And the team has zero cards

  Scenario: Creating a team twice should be idempotent
    Given I have an account with address "0xPLAYER2"
    When I create a team for "0xPLAYER2"
    And I create a team for "0xPLAYER2" again
    Then the team for "0xPLAYER2" exists
    And the team has zero cards
