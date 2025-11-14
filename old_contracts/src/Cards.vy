# pragma version ^0.4.3

struct Card:
    id: uint256
    name: String[64]
    power: uint8

event CardCreated:
    card: Card
    at: uint256


cards: public(HashMap[uint256, Card])
next_card_id: public(uint256)

@deploy
def __init__():
    self.next_card_id = 1

@external
def new(_name: String[64], _power: uint8) -> Card:
    return self._new(_name, _power)


def _new(_name: String[64], _power: uint8) -> Card:
    card_id: uint256 = self.new_id()
    new_card: Card = Card(
        id=card_id,
        name=_name,
        power=_power
    )

    self.register(new_card)
    log CardCreated(card=new_card, at=block.timestamp)

    return new_card

def new_id() -> uint256:
    id: uint256 = self.next_card_id
    self.next_card_id += 1
    return id

def register(_card: Card):
    self.cards[_card.id] = _card