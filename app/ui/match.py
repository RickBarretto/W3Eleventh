from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label


class MatchScreen(Screen):
    """Simple match placeholder screen."""

    CSS = """
    Screen {
        align: center middle;
    }
    #match-title {
        text-align: center;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Center():
            yield Label("Match lobby (todo: wire gameplay)", id="match-title")
        with Center():
            yield Button("Back to menu", id="back", variant="primary", tooltip="Return to menu")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
