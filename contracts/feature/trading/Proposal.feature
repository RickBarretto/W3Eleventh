Feature: Proposal Trade

    Scenario: Sucessful Proposal
        Given a Card in auction
            And no proposals active by the Buyer
        When the Buyer proposes a trade
        Then it should go the the proposal list

    Scenario: Replacing Timed-out Proposal
        Given a Card in auction
            And a timed-out proposal by the Buyer
        When the Buyer proposes a trade
        Then it should remove the old proposal
            And the new one should go to the proposal list

    Scenario: Can't have multiple proposals
        Given a Buyer with an active proposal
        When the Buyer proposes a trade
        Then it should revert
