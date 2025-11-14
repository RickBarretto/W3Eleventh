# pragma version ^0.4.3
# pragma nonreentrancy on

import Cards
import Inventory
import Admins

uses: Admins
initializes: Cards
initializes: Inventory

event Claimed:
    by: address
    card: Cards.Card

event Rewrote:
    old_cards: Cards.Card[128]
    new_cards: Cards.Card[128]


rewardings: public(DynArray[Cards.Card, 128])


@deploy
def __init__():
    Cards.__init__()
    Inventory.__init__()
    self.rewardings.append(Cards._new("Lionel Messi", 99))
    self.rewardings.append(Cards._new("Cristiano Ronaldo", 99))
    self.rewardings.append(Cards._new("Ronaldinho", 99))
    self.rewardings.append(Cards._new("Ronaldo", 99))
    self.rewardings.append(Cards._new("Pele", 100))
    self.rewardings.append(Cards._new("Maradona", 100))
    self.rewardings.append(Cards._new("Chech", 100))

@external
def all() -> DynArray[Cards.Card, 128]:
    Admins.must_be(msg.sender)

    return self.rewardings


@external
def claim() -> Cards.Card:
    assert len(self.rewardings) > 0, "No rewardings available at the moment."
    assert len(Inventory._deck_of(msg.sender)) < 64, "User's deck must have available stock."

    claimed: Cards.Card = self.rewardings.pop()
    Inventory.add_to(msg.sender, claimed)

    log Claimed(by=msg.sender, card=claimed)
    return claimed


@external
def set(cards: DynArray[Cards.Card, 128]):
    Admins.must_be(msg.sender)

    self.clear()
    self.fill(cards)


def clear():
    self.rewardings = empty(DynArray[Cards.Card, 128])


def fill(cards: DynArray[Cards.Card, 128]):
    self.rewardings = cards
