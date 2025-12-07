import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def ownership_ctx():
    return {}



@given("the blockchain is operational")
def ownership_blockchain_running():
    pass


@given("players have unique identifiers")
def ownership_unique_players(players):
    return players


@scenario("Ownership.feature", "Owned Card Query")
def test_owned_card_query():
    pass

@given("a player owns a card")
def player_owns_card(players, admin, packages_contract, ownership_ctx):
    player = players["dave"]
    ownership_ctx["player"] = player
    ownership_ctx["admin"] = admin
    with boa.env.prank(admin):
        packages_contract.grant_claim(player)
    with boa.env.prank(player):
        packages_contract.claim_pack()
    ownership_ctx["cards"] = list(packages_contract.cards_of(player))


@when("querying all cards owned by the player")
def query_owned_cards(packages_contract, ownership_ctx):
    player = ownership_ctx["player"]
    ownership_ctx["owned_cards_response"] = list(packages_contract.cards_of(player))


@then("the response includes all cards he owns")
def response_includes_all_cards(ownership_ctx):
    expected = set(ownership_ctx["cards"])
    returned = set(ownership_ctx["owned_cards_response"])
    assert expected == returned
