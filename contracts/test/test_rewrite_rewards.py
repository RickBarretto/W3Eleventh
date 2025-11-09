import pytest
import boa

@pytest.fixture
def decks():
    return boa.load("contracts/src/decks.vy")

@pytest.fixture
def sample_card(decks):
    return decks.card("CR7", 99)


def test_initial_rewards(decks):
    assert len(decks.all_rewardings()) == 7


def test_rewrite_full(decks, sample_card):
    decks.rewrite_rewards([sample_card] * 128)
    assert len(decks.all_rewardings()) == 128
