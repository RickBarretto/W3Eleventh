Feature: Trade Cards

    Scenario: Accepted Trade
        Given an Auction of a Card A owned by a Seller
            And a Proposal of trading Card B owned by a Proposer
        When the Seller accepts the Proposal
        Then the Seller should have Card B but not Card A
            And the Proposer should have Card A but not Card B
            And the Auction should be removed from the store
            And the Seller's associated Auction should be empty
            And the Proposer's associated Proposal should be empty

    Scenario: Timed-out Trade
        Given an Auction of a Seller without Proposals
        When some event happens
            And the auction's lifetime is timed-out
        Then the Auction should be removed from the store
            And the Seller's associated Auction should be empty

    Scenario: Timed-out Trade with Proposals
        Given an Auction of a Seller with Proposals
        When some event happens
            And the auction's lifetime is timed-out
        Then the Auction should be removed from the store
            And the Seller's associated Auction should be empty
            And the Proposer's associated Proposal should be empty
