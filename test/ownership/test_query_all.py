import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def context():
    return {}


def claim_card_pack(packages, context):
    player = context["player"]
    admin = context["admin"]
    with boa.env.prank(admin):
        packages.grant_claim(player)
    with boa.env.prank(player):
        pack_id = packages.claim_pack()
    context["pack_id"] = pack_id
    context["cards"] = list(packages.cards_of(player))


@given("the blockchain is operational")
def ownership_blockchain_running():
    pass


@given("players have unique identifiers")
def ownership_unique_players(players):
    return players


@scenario("Ownership.feature", "Ownership Query")
def test_claiming_a_card():
    pass

@given("a player")
def any_player(players, admin, context):
    context.setdefault("player", players["alice"])
    context.setdefault("admin", admin)


@when("querying the blockchain for the card ownership")
def query_card_owner(packages, context):
    # Ensure the player has a card to query.
    if "cards" not in context:
        claim_card_pack(packages, context)
    card_id = context["cards"][0]
    context["queried_card"] = card_id
    context["queried_owner"] = packages.card_owner(card_id)


@then("the response shows the owner of that card")
def response_shows_owner(context):
    assert context["queried_owner"] == context["player"]

