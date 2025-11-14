import Cards

struct Team:
    name: String[64]
    won: uint256
    lost: uint256

owner: address

teams: public(HashMap[address, Team])


@deploy
def __init__():
    self.owner = msg.sender


@external
def new(_team_name: String[64]) -> Team:
    _team: Team = Team(name=_team_name, won=0, lost=0)
    self.teams[msg.sender] = _team
    return _team

@external
def mine() -> Team:
    _team: Team = self.teams[msg.sender]
    return _team

@external
def win(user: address):
    self.teams[user].won += 1

@external
def lose(user: address):
    self.teams[user].lost += 1