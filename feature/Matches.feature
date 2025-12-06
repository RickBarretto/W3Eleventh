Feature: Matches and Results
    To ensure fair play and accurate records,
    All matches and their results must be recorded on the blockchain.

    Background:
        Given the blockchain is operational
        And players have unique identifiers


    Scenario: Can't join match twice
        Given a player that is alread in a match
        When the player tries to join some other match
        Then the blockchain rejects the request
            And an error message is returned indicating the player is already in a match


    Scenario: Creating a Match
        Given one player is ready to play
        When a match is initiated
        Then the match is recorded on the blockchain
            And the host is registered as the match host
            And the status is set to 0 (waiting)
            And there is no guest yet
            And there is no winner yet


    Scenario: Joining a Match
        Given a waiting match
        When another player joins the match
        Then the match is updated on the blockchain
            And the guest is registered as the guest player
            And the status is set to 1 (in progress)


    Scenario: Choosing a Squad
        Given a match is in progress
            And both players are registered
            But have not chosen their squads yet
        When a player chooses a squad
        Then the match is updated on the blockchain
            And the player's chosen squad is recorded


    Scenario: Reporting Match Result
        Given a match in progress
            And one player has chosen its squad
        When the second player chooses its squad
        Then the match is updated on the blockchain
            And the winner is recorded
            And the status is set to 2 (completed)


    Scenario: Querying Match Details
        Given a match exists on the blockchain
        When querying the blockchain for match details
        Then the response includes host, guest, status, squads, and winner


    Scenario: Querying Player Matches
        Given a player has participated in matches
        When querying the blockchain for matches involving the player
        Then the response includes all matches where the player is host or guest
