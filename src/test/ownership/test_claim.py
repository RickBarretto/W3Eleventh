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


@scenario("Ownership.feature", "Claiming a Card")
def test_claiming_a_card():
    pass


@given("a player")
def any_player(players, admin, ownership_ctx):
    ownership_ctx.setdefault("player", players["alice"])
    ownership_ctx.setdefault("admin", admin)


@when("the player claims a card pack")
def claim_card_pack(packages_contract, ownership_ctx):
    player = ownership_ctx["player"]
    admin = ownership_ctx["admin"]
    with boa.env.prank(admin):
        packages_contract.grant_claim(player)
    with boa.env.prank(player):
        pack_id = packages_contract.claim_pack()
    ownership_ctx["pack_id"] = pack_id
    ownership_ctx["cards"] = list(packages_contract.cards_of(player))


@then("the card package is created on the blockchain")
def package_created(packages_contract, ownership_ctx):
    pack_id = ownership_ctx["pack_id"]
    player = ownership_ctx["player"]
    assert pack_id > 0
    assert packages_contract.pack_owner(pack_id) == player


@then("each card has unique identifiers")
def unique_cards(ownership_ctx):
    cards = ownership_ctx["cards"]
    assert len(cards) == len(set(cards))
    assert len(cards) > 0


@then("the player is registered as the owner of the card pack")
def pack_owner_recorded(packages_contract, ownership_ctx):
    pack_id = ownership_ctx["pack_id"]
    player = ownership_ctx["player"]
    assert packages_contract.pack_owner(pack_id) == player


@then("the package is registered as opened")
def pack_marked_opened(packages_contract, ownership_ctx):
    pack_id = ownership_ctx["pack_id"]
    assert packages_contract.pack_opened(pack_id)

