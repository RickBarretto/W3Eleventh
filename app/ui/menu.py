from __future__ import annotations

from typing import Iterable, List

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, TabPane, TabbedContent


class MenuScreen(Screen):
	"""Menu screen with a tab per user."""

	def __init__(self, users: Iterable[str], active_user: str) -> None:
		super().__init__()
		self.users = list(users)
		self.active_user = reactive(active_user)

	def compose(self):
		yield Header(show_clock=True)

		with TabbedContent():
			for user in self.users:
				with TabPane(user, id=f"tab-{user}"):
					yield Label(f"[b]Welcome, {user}![/b]", id="welcome-label")

		yield Footer()
