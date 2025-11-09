import boa
import pytest


@pytest.fixture
def cards():
    return boa.load("contracts/src/Cards.vy")


@pytest.fixture
def trades():
    return boa.load("contracts/src/Trades.vy")


def test_auction_card_and_shop(trades, cards):
    seller = boa.env.generate_address()
    card = cards.card("Sword", 10)

    with boa.env.prank(seller):
        trades.auction_card(card, 3)

    auction = trades.shop(0)
    assert auction.seller == seller
    assert auction.card.name == "Sword"
    assert auction.card.power == 10


def test_propose_and_proposals(trades, cards):
    seller = boa.env.generate_address()
    proposer = boa.env.generate_address()

    listed = cards.card("Axe", 12)
    offered = cards.card("Shield", 5)

    with boa.env.prank(seller):
        trades.auction_card(listed, 2)

    with boa.env.prank(proposer):
        trades.propose(0, offered)

    proposal = trades.proposals(proposer)
    assert proposal.proposer == proposer
    assert proposal.offer.name == "Shield"
    assert proposal.offer.power == 5

    with boa.env.prank(proposer):
        proposal = trades.my_proposals()

        assert proposal.proposer == proposer
        assert proposal.offer.name == "Shield"
