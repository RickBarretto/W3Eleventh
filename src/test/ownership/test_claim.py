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


@scenario("Ownership.feature", "Claiming a Card")
def test_claiming_a_card():
    pass


@given("a player")
def any_player(players, admin, context):
    context.setdefault("player", players["alice"])
    context.setdefault("admin", admin)


@when("the player claims a card pack")
def claim_card_pack(packages, context):
    player = context["player"]
    admin = context["admin"]
    with boa.env.prank(admin):
        packages.grant_claim(player)
    with boa.env.prank(player):
        pack_id = packages.claim_pack()
    context["pack_id"] = pack_id
    context["cards"] = list(packages.cards_of(player))


@then("the card package is created on the blockchain")
def package_created(packages, context):
    pack_id = context["pack_id"]
    player = context["player"]
    assert pack_id > 0
    assert packages.pack_owner(pack_id) == player


@then("each card has unique identifiers")
def unique_cards(context):
    cards = context["cards"]
    assert len(cards) == len(set(cards))
    assert len(cards) > 0


@then("the player is registered as the owner of the card pack")
def pack_owner_recorded(packages, context):
    pack_id = context["pack_id"]
    player = context["player"]
    assert packages.pack_owner(pack_id) == player


@then("the package is registered as opened")
def pack_marked_opened(packages, context):
    pack_id = context["pack_id"]
    assert packages.pack_opened(pack_id)

