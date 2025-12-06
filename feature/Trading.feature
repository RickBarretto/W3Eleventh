Feature: Trading Cards
    To facilitate player interactions,
    Card trading between players must be securely recorded on the blockchain.

    Background:
        Given the blockchain is operational
        And players have unique identifiers

    Scenario: Trade after Match Victory
        Given an ended match with a winner
        When the winner proposes a trade to another player
        Then the trade is done on the blockchain
            And the offered card is transferred to the other player
            And the requested card is transferred to the winner

    Scenario: Trade Query
        Given two players have traded cards
        When querying the blockchain for trade history
        Then the response includes details of the trade
            And the involved players
            And the cards exchanged

