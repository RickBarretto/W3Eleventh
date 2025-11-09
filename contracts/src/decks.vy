struct Card:
    name: String[64]
    power: uint8
    
event Claimed:
    by: address
    card: Card
    
event Rewrote:
    old_cards: Card[128]
    new_cards: Card[128]


rewardings: public(DynArray[Card, 128])
decks: public(HashMap[address, DynArray[Card, 64]])


@deploy
def __init__():
    self.rewardings.append(Card(name="Lionel Messi", power=99))
    self.rewardings.append(Card(name="Cristiano Ronaldo", power=99))
    self.rewardings.append(Card(name="Ronaldinho", power=99))
    self.rewardings.append(Card(name="Ronaldo", power=99))
    self.rewardings.append(Card(name="Pele", power=100))
    self.rewardings.append(Card(name="Maradona", power=100))
    self.rewardings.append(Card(name="Chech", power=100))


@external
def card(_name: String[64], _power: uint8) -> Card:
    return Card(name=_name, power=_power)
    
@view
@external
def all_rewardings() -> DynArray[Card, 128]:
    return self.rewardings


@external
def claim() -> Card:
    assert len(self.rewardings) > 0, "No rewardings available at the moment."
    assert len(self.decks[msg.sender]) < 64, "User's deck must have available stock."
    
    claimed: Card = self.rewardings.pop()
    self.decks[msg.sender].append(claimed)
    
    log Claimed(by=msg.sender, card=claimed)
    return claimed


@external
def rewrite_rewards(cards: DynArray[Card, 128]):    
    self.empty_rewardings()
    self.fill_rewardings(cards)

@internal
def empty_rewardings():
    self.rewardings = empty(DynArray[Card, 128])

        
@internal
def fill_rewardings(cards: DynArray[Card, 128]):
    self.rewardings = cards
