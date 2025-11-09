import pytest
import boa

@pytest.fixture
def decks():
    return boa.load("contracts/src/decks.vy")


def test_initial_rewards(decks):
    assert len(decks.all_rewardings()) == 7
    
def test_claim(decks):
    card = decks.claim() 
    
    assert card.name == "Chech" 
    assert card.power == 100 
    assert len(decks.all_rewardings()) == 6
 
