Feature: Team Management

    Scenario: Creating a Team
        Given I want to create a new team named "Warriors"
        When I create the team "Warriors"
        Then I should own this team
            And its name should be "Warriors"
            And its should have 0 lost and won

    Scenario: Winning a match
        Given a Team "Warriors" with 0 won
        When it wins a match
        Then it has 1 won

    Scenario: Losing a match
        Given a Team "Warriors" with 0 lost
        When it loses a match
        Then it has 1 lost
