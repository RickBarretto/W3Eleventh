Feature: Auction Card

    Scenario: Auction Cards
        Given a seller without any active auction
        When the seller auctions a card
        Then the Auction should be registered.

    Scenario: Prevent Multiple Active Auctions
        Given a seller with an active auction
        When the seller tries to auction another card
        Then the Auction should be rejected

    Scenario: Replacing a Dead Auction
        Given a seller with a dead auction
        When the seller tries to auction another card
        Then the new Auction should be registered
