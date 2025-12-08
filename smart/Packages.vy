"""
Card ownership, claiming rights, and trading.
"""

PACK_CAPACITY: constant(uint256) = 5
INVENTORY_CAPACITY: constant(uint256) = 2048
TRADES_CAPACITY: constant(uint256) = 1024
WIN_MILESTONE: constant(uint256) = 5

struct Trade:
	from_addr: address
	to_addr: address
	offered_card: uint256
	requested_card: uint256

owner: public(address)
next_card_id: public(uint256)
next_pack_id: public(uint256)
claim_rights: public(HashMap[address, bool])
card_owner: public(HashMap[uint256, address])
player_cards: HashMap[address, DynArray[uint256, INVENTORY_CAPACITY]]
pack_cards: HashMap[uint256, DynArray[uint256, PACK_CAPACITY]]
pack_owner: public(HashMap[uint256, address])
pack_opened: public(HashMap[uint256, bool])
trade_history: DynArray[Trade, TRADES_CAPACITY]
wins_in_row: public(HashMap[address, uint256])
registered: public(HashMap[address, bool])

event ClaimGranted:
	player: address

event PackClaimed:
	player: address
	pack_id: uint256

event TradeExecuted:
	from_addr: address
	to_addr: address
	offered_card: uint256
	requested_card: uint256


@deploy
def __init__(_owner: address):
	self.owner = _owner
	self.next_card_id = 1
	self.next_pack_id = 1


@external
def register_player():
	assert not self.registered[msg.sender], "already registered"
	assert len(self.player_cards[msg.sender]) == 0, "player already has cards"

	self.registered[msg.sender] = True
	self.claim_rights[msg.sender] = True

	log ClaimGranted(player=msg.sender)


@view
@external
def cards_of(player: address) -> DynArray[uint256, INVENTORY_CAPACITY]:
	return self.player_cards[player]


@view
@external
def get_trade_count() -> uint256:
	return len(self.trade_history)


@view
@external
def get_trade(index: uint256) -> (address, address, uint256, uint256):
	assert index < len(self.trade_history), "invalid trade index"
	trade: Trade = self.trade_history[index]
	return trade.from_addr, trade.to_addr, trade.offered_card, trade.requested_card


@external
def grant_claim(player: address):
	assert msg.sender == self.owner, "only owner"
	self.claim_rights[player] = True
	log ClaimGranted(player=player)


@external
def revoke_claim(player: address):
	assert msg.sender == self.owner, "only owner"
	self.claim_rights[player] = False


@external
def record_win(player: address):
	assert msg.sender == self.owner, "only owner"

	streak: uint256 = self.wins_in_row[player] + 1
	self.wins_in_row[player] = streak

	if streak >= WIN_MILESTONE:
		self.wins_in_row[player] = 0
		self.claim_rights[player] = True
		log ClaimGranted(player=player)


@external
def claim_pack() -> uint256:
	assert self.claim_rights[msg.sender], "no claim rights"
	pack_id: uint256 = self.next_pack_id
	self.next_pack_id += 1

	# Mint cards and assign ownership
	for i: uint256 in range(PACK_CAPACITY):
		card_id: uint256 = self.next_card_id
		self.next_card_id += 1

		self.card_owner[card_id] = msg.sender
		self._add_card(msg.sender, card_id)
		self.pack_cards[pack_id].append(card_id)

	self.pack_owner[pack_id] = msg.sender
	self.pack_opened[pack_id] = True
	self.claim_rights[msg.sender] = False

	log PackClaimed(player=msg.sender, pack_id=pack_id)
	return pack_id


@external
def trade(to_addr: address, offered_card: uint256, requested_card: uint256):
	assert msg.sender != to_addr, "cannot trade with self"
	assert self.card_owner[offered_card] == msg.sender, "not owner of offered card"
	assert self.card_owner[requested_card] == to_addr, "counterparty not owner"

	# Swap ownership
	self.card_owner[offered_card] = to_addr
	self.card_owner[requested_card] = msg.sender

	self._remove_card(msg.sender, offered_card)
	self._remove_card(to_addr, requested_card)

	self._add_card(to_addr, offered_card)
	self._add_card(msg.sender, requested_card)

	trade_entry: Trade = Trade(
		from_addr=msg.sender,
		to_addr=to_addr,
		offered_card=offered_card,
		requested_card=requested_card,
	)
	assert len(self.trade_history) < TRADES_CAPACITY, "too many trades"
	self.trade_history.append(trade_entry)

	log TradeExecuted(
		from_addr=msg.sender,
		to_addr=to_addr,
		offered_card=offered_card,
		requested_card=requested_card,
	)


@internal
def _add_card(player: address, card_id: uint256):
	assert len(self.player_cards[player]) < INVENTORY_CAPACITY, "too many cards"
	self.player_cards[player].append(card_id)


@internal
def _remove_card(player: address, card_id: uint256):
	length: uint256 = len(self.player_cards[player])
	for i: uint256 in range(INVENTORY_CAPACITY):
		if i >= length:
			break
		if self.player_cards[player][i] == card_id:
			last_index: uint256 = length - 1
			self.player_cards[player][i] = self.player_cards[player][last_index]
			self.player_cards[player].pop()
			return
	assert False, "card not owned"
