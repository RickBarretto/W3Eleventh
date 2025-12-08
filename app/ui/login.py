from __future__ import annotations

from typing import List

from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal, ItemGrid, Grid
from textual.screen import Screen
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Label, Rule

from app.ui.menu import MenuScreen


DEFAULT_USERS: List[str] = ["alice", "bob", "carol"]


class LoginScreen(Screen):

	username: str = reactive(None)

	CSS = """
	#title {
		text-align: center;
		width: auto;
	}
	
	Input {
		width: 50%;
	}
	"""

	def __init__(self) -> None:
		super().__init__()
		self.username_input: Input | None = None

	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)

		yield Label("[b]Login[/b]", id="title")
		with Horizontal():
			with Center():	
				self.username_input = Input(placeholder="Username", id="username", compact=True)
				yield self.username_input
				yield Button(">> Enter as User <<", id="login-user", compact=True)
			yield Rule(orientation="vertical")
			with Center():
				yield Label("Or...")
				yield Button(">> Enter as Admin <<", id="login-admin", compact=True)

		yield Footer()

	def on_button_pressed(self, event: Button.Pressed) -> None:
		assert self.username_input is not None
		username = self.username_input.value.strip() or DEFAULT_USERS[0]

		if event.button.id == "login-admin":
			active_user = "admin"
			users = ["admin", *DEFAULT_USERS]
		elif event.button.id == "login-user":
			active_user = username.lower()
			users = [active_user, *DEFAULT_USERS]
		else:
			return

		self.app.push_screen(MenuScreen(users=users, active_user=active_user))
