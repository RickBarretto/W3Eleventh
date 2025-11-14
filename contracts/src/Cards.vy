
struct Card:
    id: uint256
    name: String[64]
    power: uint8


owner: address
id_count: uint256


@deploy
def __init__():
    self.owner = msg.sender


@external
def new(_name: String[64], _power: uint8) -> Card:
    assert msg.sender == self.owner, "Must be Owner"
    assert _power > 60
    assert _power < 100 

    card_id: uint256 =  self.next_id()
    card: Card = Card(id=card_id, name=_name, power=_power)
    return card


def next_id() -> uint256:
    self.id_count += 1
    return self.id_count
