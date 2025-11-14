Feature: Rewarding System

    Scenario: Earning Points for Achievements
        Given I have completed some achievement
        When I check my points balance
        Then I should see that I have earned a new player
