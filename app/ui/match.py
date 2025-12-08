from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, TabPane, TabbedContent


class MatchScreen(Screen):
    """Match lobby screen with tabs per player."""

    PLAYERS = ["alice", "bob", "carol", "dave"]

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

    .match-column {
        padding: 1 2;
        content-align: left top;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent(initial=self.PLAYERS[0]):
            for player in self.PLAYERS:
                with TabPane(player.title(), id=player):
                    yield Vertical(
                        Label(f"Player: {player.title()}", classes="menu-title"),
                        Label("Match status: waiting", id=f"status-{player}"),
                        Button("Choose squad", id=f"squad-{player}", variant="primary"),
                        Button("Report result", id=f"result-{player}", variant="warning"),
                        Button("Back to menu", id="back", variant="primary"),
                        classes="match-column",
                    )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id or ""
        if button_id == "back":
            self.app.pop_screen()
            return

        if "-" not in button_id:
            return

        action, player = button_id.split("-", 1)
        if player not in self.PLAYERS:
            return

        if action == "squad":
            self._set_status(player, "Squad chosen (demo only)")
        elif action == "result":
            self._set_status(player, "Result reported (demo only)")

    def _set_status(self, player: str, message: str) -> None:
        label = self.query_one(f"#status-{player}", Label)
        label.update(f"Match status: {message}")
