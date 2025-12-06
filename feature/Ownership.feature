Feature: Card Ownership and Registering
    To keep the game integrity,
    The cards must be unique, trackable, and registered on the blockchain.

    Background:
        Given the blockchain is operational
        And players have unique identifiers


    Scenario: Gaining Claim rights for beginners
        Given a player without any cards
        When the player registers on the platform
        Then the player is granted rights to claim a beginner card pack


    Scenario: Gaining Claim rights for winners
        Given a player that has won a match
        When the player reaches a win milestone of 5 sequential wins
        Then the player is granted rights to claim a special card pack


    Scenario: Rejected Claim
        Given a player without claiming rights
        When the player tries to claim a card pack
        Then the blockchain rejects the request
            And an error message is returned indicating the player cannot claim a card pack


    Scenario: Claiming a Card
        Given a player
        When the player claims a card pack
        Then the card package is created on the blockchain
            And each card has unique identifiers
            And the player is registered as the owner of the card pack
            And the package is registered as opened


    Scenario: Ownership Query
        Given a player
        When querying the blockchain for the card ownership
        Then the response shows the owner of that card


    Scenario: Owned Card Query
        Given a player owns a card
        When querying all cards owned by the player
        Then the response includes all cards he owns
