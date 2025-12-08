from __future__ import annotations

from typing import List

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, TabPane, TabbedContent

from app.ui.match import MatchScreen


class MenuScreen(Screen):
	"""Menu screen with a tab per user."""

	PLAYERS: List[str] = ["alice", "bob", "carol", "dave"]

	CSS = """
	TabbedContent {
		width: 100%;
		height: 1fr;
	}

	TabPane > .menu-column {
		padding: 1 2;
		content-align: left top;
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
		self.next_card_id: int = 1

	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)
		with TabbedContent(initial=self.PLAYERS[0]):
			for player in self.PLAYERS:
				with TabPane(player.title(), id=player):
					yield Vertical(
						Label(f"Player: {player.title()}", classes="menu-title"),
						Button("Enter match", id=f"enter-{player}", variant="primary"),
						Button("List cards", id=f"cards-{player}", variant="primary"),
						Button("List old matches", id=f"old-{player}", variant="primary"),
						Button("Claim pack", id=f"claim-{player}", variant="success"),
						Label("", id=f"claim-status-{player}", classes="claim-status"),
						Label("", id=f"action-status-{player}", classes="action-status"),
						classes="menu-column",
					)
		yield Footer()

	def on_mount(self) -> None:
		self.player_cards = {player: [] for player in self.PLAYERS}
		self.claim_rights = {player: True for player in self.PLAYERS}
		self.action_messages = {player: "Idle" for player in self.PLAYERS}
		self._refresh_all_claim_status()
		self._refresh_all_action_status()

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
				self._set_action_status(player, f"Pack claimed: {new_cards}")
			except Exception as exc:
				self._set_action_status(player, f"Claim failed: {exc}")
			self._refresh_claim_status(player)
		elif action == "enter":
			self._set_action_status(player, "Entering the match lobby.")
			self.app.push_screen(MatchScreen(self.player_cards))
		elif action == "cards":
			cards = self.player_cards.get(player, [])
			status = f"Owned cards: {cards}" if cards else "Owned cards: none"
			self._set_action_status(player, status)
		elif action == "old":
			self._set_action_status(player, "Showing completed matches.")
		else:
			self._set_action_status(player, "Unknown action")

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

	def _refresh_all_action_status(self) -> None:
		for player in self.PLAYERS:
			self._set_action_status(player, self.action_messages.get(player, ""))

	def _set_action_status(self, player: str, message: str) -> None:
		self.action_messages[player] = message
		label = self.query_one(f"#action-status-{player}", Label)
		label.update(f"Status: {message}")
