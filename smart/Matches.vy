"""
Match management contract.
Status codes: 0 = waiting, 1 = in progress, 2 = completed.
"""

SQUAD_CAPACITY: constant(uint256) = 64
MATCHES_IN_CHAMPIONSHIP: constant(uint256) = 256

struct Match:
	host: address
	guest: address
	status: uint256
	host_squad: Bytes[SQUAD_CAPACITY]
	guest_squad: Bytes[SQUAD_CAPACITY]
	winner: address

event MatchCreated:
	match_id: uint256
	host: address

event MatchJoined:
	match_id: uint256
	guest: address

event SquadChosen:
	match_id: uint256
	player: address
	squad: Bytes[SQUAD_CAPACITY]

event ResultReported:
	match_id: uint256
	winner: address

matches: public(HashMap[uint256, Match])
next_match_id: public(uint256)
player_active_match: public(HashMap[address, uint256])
player_matches: HashMap[address, DynArray[uint256, MATCHES_IN_CHAMPIONSHIP]]


@deploy
def __init__():
	self.next_match_id = 1


@view
@external
def get_player_matches(
	player: address
) -> DynArray[uint256, MATCHES_IN_CHAMPIONSHIP]:
	return self.player_matches[player]


@external
def create_match() -> uint256:
	assert self.player_active_match[msg.sender] == 0, "player already in a match"

	match_id: uint256 = self.next_match_id
	self.next_match_id += 1

	new_match: Match = Match(
		host=msg.sender,
		guest=empty(address),
		status=0,
		host_squad=b"",
		guest_squad=b"",
		winner=empty(address),
	)

	self.matches[match_id] = new_match
	self.player_active_match[msg.sender] = match_id
	self._append_player_match(msg.sender, match_id)

	log MatchCreated(match_id=match_id, host=msg.sender)
	return match_id


@external
def join_match(match_id: uint256):
	match_: Match = self.matches[match_id]
	assert match_.host != empty(address), "unknown match"
	assert match_.status == 0, "match not waiting"
	assert self.player_active_match[msg.sender] == 0, "player already in a match"
	assert match_.host != msg.sender, "host already in match"

	match_.guest = msg.sender
	match_.status = 1
	self.matches[match_id] = match_

	self.player_active_match[msg.sender] = match_id
	self._append_player_match(msg.sender, match_id)

	log MatchJoined(match_id=match_id, guest=msg.sender)


@external
def choose_squad(match_id: uint256, squad: Bytes[SQUAD_CAPACITY]):
	match_: Match = self.matches[match_id]
	assert match_.host != empty(address), "unknown match"
	assert match_.status != 2, "match completed"
	assert msg.sender == match_.host or msg.sender == match_.guest, "not participant"
	assert len(squad) > 0, "squad required"

	if msg.sender == match_.host:
		assert len(match_.host_squad) == 0, "squad already set"
		match_.host_squad = squad
	else:
		assert len(match_.guest_squad) == 0, "squad already set"
		match_.guest_squad = squad

	self.matches[match_id] = match_

	log SquadChosen(match_id=match_id, player=msg.sender, squad=squad)


@external
def report_result(match_id: uint256, winner: address):
	match_: Match = self.matches[match_id]
	assert match_.host != empty(address), "unknown match"
	assert match_.status == 1, "match not in progress"
	assert len(match_.host_squad) > 0 and len(match_.guest_squad) > 0, "both squads required"
	assert winner == match_.host or winner == match_.guest, "invalid winner"

	match_.winner = winner
	match_.status = 2
	self.matches[match_id] = match_

	self.player_active_match[match_.host] = 0
	if match_.guest != empty(address):
		self.player_active_match[match_.guest] = 0

	log ResultReported(match_id=match_id, winner=winner)


@view
@external
def get_match(match_id: uint256) -> (
	address, 
	address, 
	uint256, 
	Bytes[SQUAD_CAPACITY], 
	Bytes[SQUAD_CAPACITY], 
	address
):
	match_: Match = self.matches[match_id]

	assert match_.host != empty(address), "unknown match"
	return match_.host, match_.guest, match_.status, match_.host_squad, match_.guest_squad, match_.winner


@internal
def _append_player_match(player: address, match_id: uint256):
	arr: DynArray[uint256, MATCHES_IN_CHAMPIONSHIP] = self.player_matches[player]
	assert len(arr) < MATCHES_IN_CHAMPIONSHIP, "too many matches"

	arr.append(match_id)
	self.player_matches[player] = arr
