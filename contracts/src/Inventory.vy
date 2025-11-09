
import Cards

decks: public(HashMap[address, DynArray[Cards.Card, 64]])


@view
@external
def deck_of(user: address) -> DynArray[Cards.Card, 64]:
    return self._deck_of(user)

@view
def _deck_of(user: address) -> DynArray[Cards.Card, 64]:
    return self.decks[user]


def add_to(user: address, card: Cards.Card):
    self.decks[user].append(card)


def remove_from(user: address, index: uint256) -> Cards.Card:
    assert index < len(self.decks[user]), "Index out of bounds."

    card: Cards.Card = self.decks[user][index]
    last_index: uint256 = len(self.decks[user]) - 1

    if index != last_index:
        self.decks[user][index] = self.decks[user][last_index]

    self.decks[user].pop()
    return card
