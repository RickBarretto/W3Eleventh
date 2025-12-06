Feature: Card rewarding
  As a game system
  I want to reward unique cards to players
  So that players can build their teams

  Background:
    Given the blockchain is running

  Scenario: Reward a unique card to a player
    Given I have a player with address "0xPLAYER1"
    When the system rewards a card named "Striker" with power 85 to "0xPLAYER1"
    Then the card exists and belongs to "0xPLAYER1"
    And the card has name "Striker"
    And the card has power 85

  Scenario: Each card is unique
    Given I have a player with address "0xPLAYER2"
    When the system rewards a card named "Defender" with power 70 to "0xPLAYER2"
    And the system rewards another card named "Defender" with power 70 to "0xPLAYER2"
    Then the player "0xPLAYER2" has 2 distinct cards
