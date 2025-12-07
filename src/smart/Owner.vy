

interface ICards:
    def card() -> uint256: view

cards: address

@deploy
def __init__(cards_address: address):
    self.cards = cards_address


@external
@view
def get_card() -> uint256:
    return staticcall ICards(self.cards).card()
