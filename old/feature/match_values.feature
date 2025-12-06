Feature: Match values
  As a player
  I want matches to use card power to decide outcome
  So that stronger cards tend to win

  Background:
    Given the blockchain is running

  Scenario: Higher-power card wins
    Given player A has a card with power 90
    And player B has a card with power 70
    When they play a match between those two cards
    Then the card with power 90 wins the match

  Scenario: Equal-power cards draw
    Given player A has a card with power 80
    And player B has a card with power 80
    When they play a match between those two cards
    Then the match result is a draw
