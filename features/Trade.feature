Feature: Trade Management

    Scenario: Proposing a Trade
        Given I have a team named "Eagles" with players "John" and "Mike"
            And another team named "Tigers" with players "Sam" and "Tom"
        When I propose a trade to exchange "John" for "Sam"
        Then the trade proposal should be sent to the "Tigers" team

    Scenario: Accepting a Trade
        Given there is a trade proposal from team "Eagles" to team "Tigers"
            And the proposal is to exchange "John" for "Sam"
        When the "Tigers" team accepts the trade proposal
        Then the players "John" and "Sam" should be exchanged between the teams

    Scenario: Rejecting a Trade
        Given there is a trade proposal from team "Eagles" to team "Tigers"
            And the proposal is to exchange "John" for "Sam"
        When the "Tigers" team rejects the trade proposal
        Then the players "John" and "Sam" should remain with their original teams