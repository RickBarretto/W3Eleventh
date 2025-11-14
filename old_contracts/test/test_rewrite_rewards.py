import pytest
import boa

@pytest.fixture
def rewardings():
    return boa.load("contracts/src/Rewardings.vy")

@pytest.fixture
def cards():
    return boa.load("contracts/src/Cards.vy")

@pytest.fixture
def sample_card(cards):
    return cards.new("CR7", 99)


def test_initial_rewards(rewardings):
    assert len(rewardings.all()) == 7


def test_rewrite_empty(rewardings):
    rewardings.set([])
    assert len(rewardings.all()) == 0


def test_rewrite_half(rewardings, sample_card):
    rewardings.set([sample_card] * 64)
    assert len(rewardings.all()) == 64


def test_rewrite_full(rewardings, sample_card):
    rewardings.set([sample_card] * 128)
    assert len(rewardings.all()) == 128

def test_non_admin_cannot_set(rewardings):
    non_admin = boa.env.generate_address()

    with boa.env.prank(non_admin):
        with boa.reverts("Only admins can perform this action."):
            rewardings.set([])
