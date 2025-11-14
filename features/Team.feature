Feature: Team Management

    Scenario: Creating a Team
        Given I want to create a new team named "Warriors"
        When I create the team "Warriors"
        Then I should have a Team associated with my address
            And this name should be "Warriors"
            And this ratio should be zeroed

    Scenario: Winning a match
        Given a Team "Warriors" with 0 wins
        When it wins a match
        Then it has 1 wins

    Scenario: Losing a match
        Given a Team "Warriors" with 0 loses
        When it loses a match
        Then it has 1 loses
