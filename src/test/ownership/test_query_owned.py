import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def context():
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
def player_owns_card(players, admin, packages, context):
    player = players["dave"]
    context["player"] = player
    context["admin"] = admin
    with boa.env.prank(admin):
        packages.grant_claim(player)
    with boa.env.prank(player):
        packages.claim_pack()
    context["cards"] = list(packages.cards_of(player))


@when("querying all cards owned by the player")
def query_owned_cards(packages, context):
    player = context["player"]
    context["owned_cards_response"] = list(packages.cards_of(player))


@then("the response includes all cards he owns")
def response_includes_all_cards(context):
    expected = set(context["cards"])
    returned = set(context["owned_cards_response"])
    assert expected == returned
