

interface Cards:
    def card() -> uint256: view

cards: address

@deploy
def __init__(_cards: address):
    self.cards = _cards


@external
@view
def get_card() -> uint256:
    return staticcall Cards(self.cards).card()
