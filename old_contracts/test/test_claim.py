import pytest
import boa

@pytest.fixture
def rewardings():
    return boa.load("contracts/src/Rewardings.vy")


def test_initial_rewards(rewardings):
    assert len(rewardings.all()) == 7


def test_claim(rewardings):
    card = rewardings.claim() 
    
    assert card.name == "Chech" 
    assert card.power == 100 
    assert len(rewardings.all()) == 6
 
