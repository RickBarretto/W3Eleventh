import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def ownership_ctx():
    return {}


def claim_card_pack(packages_contract, ownership_ctx):
    player = ownership_ctx["player"]
    admin = ownership_ctx["admin"]
    with boa.env.prank(admin):
        packages_contract.grant_claim(player)
    with boa.env.prank(player):
        pack_id = packages_contract.claim_pack()
    ownership_ctx["pack_id"] = pack_id
    ownership_ctx["cards"] = list(packages_contract.cards_of(player))


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
def any_player(players, admin, ownership_ctx):
    ownership_ctx.setdefault("player", players["alice"])
    ownership_ctx.setdefault("admin", admin)


@when("querying the blockchain for the card ownership")
def query_card_owner(packages_contract, ownership_ctx):
    # Ensure the player has a card to query.
    if "cards" not in ownership_ctx:
        claim_card_pack(packages_contract, ownership_ctx)
    card_id = ownership_ctx["cards"][0]
    ownership_ctx["queried_card"] = card_id
    ownership_ctx["queried_owner"] = packages_contract.card_owner(card_id)


@then("the response shows the owner of that card")
def response_shows_owner(ownership_ctx):
    assert ownership_ctx["queried_owner"] == ownership_ctx["player"]

