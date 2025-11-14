Feature: Team Management

    Scenario: Creating a Team
        Given I want to create a new team named "Warriors"
        When I create the team "Warriors"
        Then the team "Warriors" should exist
            And I should have 11 players in the team

    Scenario: Listing Players in a Team
        Given a team named "Warriors" with players "Alice", "Bob", and "Charlie"
        When I list the players in the team "Warriors"
        Then I should see "Alice", "Bob", and "Charlie" in the list
