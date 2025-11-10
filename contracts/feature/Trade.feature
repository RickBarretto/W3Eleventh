Feature: Trade Cards

    Scenario: Accepted Trade
        Given a Trader A owning Card X
            And a Trader B owning Card Y
        When Trader A proposes to trade Card X for Card Y to Trader B
            And Trader B accepts the trade proposal
        Then the Trade should happen

    Scenario: Rejected Trade
        Given a Trader A owning Card X
            And a Trader B owning Card Y
        When Trader A proposes to trade Card X for Card Y to Trader B
            And Trader B rejects the trade proposal
        Then the Trade should not happen
