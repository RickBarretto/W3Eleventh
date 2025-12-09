from __future__ import annotations

from typing import List

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, CenterMiddle
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, TabPane, TabbedContent, Placeholder

from app.ui.match import MatchScreen


class MenuScreen(Screen):
	"""Menu screen with a tab per user."""

	PLAYERS: List[str] = ["alice", "bob", "carol", "dave"]

	CSS = """
	TabbedContent {
		width: 100%;
		height: 1fr;
	}

	TabPane > .menu-layout {
		height: 1fr;
	}

	.menu-column {
		width: 32;
		min-width: 28;
		padding: 1 2;
		content-align: left top;
	}

	.menu-column Button {
		padding: 0 1;
		height: auto;
		content-align: left middle;
		border: round $accent;
	}

	.menu-status {
		width: 1fr;
		height: 1fr;
		padding: 1 2;
		content-align: left top;
	}

	.menu {
		border: vkey $accent;
	}

	.menu-title {
		text-style: bold;
	}

	.claim-status {
		color: green;
	}

	.action-status {
		color: yellow;
	}
	"""

	def __init__(self) -> None:
		super().__init__()
		self.claim_rights: dict[str, bool] = {}
		self.action_messages: dict[str, str] = {}
		self.player_cards: dict[str, list[int]] = {}
		self.match_history: list[dict] = []
		self.next_card_id: int = 1

	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)
		with TabbedContent(initial=self.PLAYERS[0]):
			for player in self.PLAYERS:
				with TabPane(player.title(), id=player):
					with Horizontal(classes="menu-layout"):
						yield CenterMiddle(
							Label(f"Player: {player.title()}", classes="menu-title"),
							Button("Start", id=f"enter-{player}", compact=True),
							Button("Team", id=f"cards-{player}", compact=True),
							Button("History", id=f"old-{player}", compact=True),
							Button("Claim", id=f"claim-{player}", compact=True),
							classes="menu menu-column",
						)
						with VerticalScroll(classes="menu menu-status"):
							yield Label("Claim status", classes="menu-title")
							yield Label("", id=f"claim-status-{player}", classes="claim-status")
							yield Label("Details", classes="menu-title")
							yield Label("", id=f"action-status-{player}", classes="action-status")
		yield Footer()

	def on_mount(self) -> None:
		self.player_cards = {player: [] for player in self.PLAYERS}
		self._recompute_claim_rights()
		self.action_messages = {player: "Idle" for player in self.PLAYERS}
		self._refresh_all_claim_status()
		self._refresh_all_action_status()

	def on_show(self) -> None:
		self._recompute_claim_rights()
		self._refresh_all_claim_status()

	def _recompute_claim_rights(self) -> None:
		win_counts = {player: 0 for player in self.PLAYERS}
		for entry in self.match_history:
			winner = entry.get("winner")
			if winner in win_counts:
				win_counts[winner] += 1

		self.claim_rights = {}
		for player in self.PLAYERS:
			has_cards = bool(self.player_cards.get(player))
			has_streak = win_counts.get(player, 0) >= 5
			self.claim_rights[player] = (not has_cards) or has_streak

	def on_button_pressed(self, event: Button.Pressed) -> None:
		button_id = event.button.id or ""
		if "-" not in button_id:
			return

		action, player = button_id.split("-", 1)
		if player not in self.PLAYERS:
			return

		if action == "claim":
			try:
				new_cards = self._claim_pack(player)
				card_lines = "\n".join(f"- Card {card_id}" for card_id in new_cards)
				self._set_action_status(player, f"Pack claimed:\n{card_lines}")
			except Exception as exc:
				self._set_action_status(player, f"Claim failed: {exc}")
			self._refresh_claim_status(player)
		elif action == "enter":
			self._set_action_status(player, "Entering the match lobby.")
			self.app.push_screen(MatchScreen(self.player_cards, self.match_history))
		elif action == "cards":
			cards = self.player_cards.get(player, [])
			if cards:
				lines = "\n".join(f"- Card {card_id}" for card_id in cards)
				self._set_action_status(player, f"Owned cards:\n{lines}")
			else:
				self._set_action_status(player, "Owned cards: none")
		elif action == "old":
			self._show_history(player)
		else:
			self._set_action_status(player, "Unknown action")

	def _show_history(self, player: str) -> None:
		if not self.match_history:
			self._set_action_status(player, "No completed matches yet.")
			return
		last = self.match_history[-10:]
		summaries = [
			f"Winner: {entry['winner']} | Squads: {entry['squads']}"
			for entry in last
		]
		self._set_action_status(player, "Recent matches:\n" + "\n".join(summaries))

	def _claim_pack(self, player: str) -> list[int]:
		"""Claim a pack for the player, mirroring contract behavior with errors."""
		if not self.claim_rights.get(player, False):
			raise PermissionError("no claim rights")

		pack_size = 5
		new_cards = list(range(self.next_card_id, self.next_card_id + pack_size))
		self.next_card_id += pack_size

		self.player_cards[player].extend(new_cards)
		self.claim_rights[player] = False
		return new_cards

	def _refresh_all_claim_status(self) -> None:
		for player in self.PLAYERS:
			self._refresh_claim_status(player)

	def _refresh_claim_status(self, player: str) -> None:
		allowed = self.claim_rights.get(player, False)
		label = self.query_one(f"#claim-status-{player}", Label)
		state = "Claim rights: available" if allowed else "Claim rights: locked"
		label.update(state)
		self._set_claim_button_state(player, allowed)

	def _set_claim_button_state(self, player: str, allowed: bool) -> None:
		button = self.query_one(f"#claim-{player}", Button)
		button.disabled = not allowed

	def _refresh_all_action_status(self) -> None:
		for player in self.PLAYERS:
			self._set_action_status(player, self.action_messages.get(player, ""))

	def _set_action_status(self, player: str, message: str) -> None:
		self.action_messages[player] = message
		label = self.query_one(f"#action-status-{player}", Label)
		label.update(message)
