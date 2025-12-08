from __future__ import annotations

from typing import List

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, TabPane, TabbedContent


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
		self.claim_rights = {player: player == "alice" for player in self.PLAYERS}
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
			if self.claim_rights.get(player, False):
				self.claim_rights[player] = False
				self._set_action_status(player, "Pack claimed; claim rights reset.")
			else:
				self._set_action_status(player, "Claim rejected: no rights yet.")
			self._refresh_claim_status(player)
		elif action == "enter":
			self._set_action_status(player, "Entering the match lobby.")
		elif action == "cards":
			self._set_action_status(player, "Listing owned cards (see Ownership.feature).")
		elif action == "old":
			self._set_action_status(player, "Showing completed matches.")

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
