# pragma version ^0.4.3
# pragma nonreentrancy on

import Admins
import Cards

initializes: Admins

decks: public(HashMap[address, DynArray[Cards.Card, 64]])

@deploy
def __init__():
    Admins.__init__()

@external
def deck_of(user: address) -> DynArray[Cards.Card, 64]:
    return self._deck_of(user)

@external
def mint_card_to(user: address, card: Cards.Card):
    Admins.must_be(msg.sender)
    self.add_to(user, card)

def _deck_of(user: address) -> DynArray[Cards.Card, 64]:
    return self.decks[user]

def has_card(user: address, card_id: uint256) -> bool:
    deck: DynArray[Cards.Card, 64] = self.decks[user]
    for card: Cards.Card in deck:
        if card.id == card_id:
            return True
    return False

def add_to(user: address, card: Cards.Card):
    self.decks[user].append(card)

def set_card(user: address, card: Cards.Card, new_card: Cards.Card):
    deck: DynArray[Cards.Card, 64] = self.decks[user]
    for i: uint256 in range(64):
        if deck[i].id == card.id:
            deck[i] = new_card
            self.decks[user] = deck
            return
