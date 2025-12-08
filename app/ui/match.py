from __future__ import annotations

from time import time

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, TabPane, TabbedContent, Checkbox


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

    def __init__(self, player_cards: dict[str, list[int]] | None = None, match_history: list[dict] | None = None) -> None:
        super().__init__()
        self.player_cards: dict[str, list[int]] = player_cards or {p: [] for p in self.PLAYERS}
        self.match_history = match_history if match_history is not None else []
        self.squads: dict[str, list[int]] = {}
        self.submitted: dict[str, bool] = {}
        self.winner: str | None = None

    def on_mount(self) -> None:
        for player in self.PLAYERS:
            self.submitted[player] = False
        self.winner = None
        self._refresh_report_buttons()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent(initial=self.PLAYERS[0]):
            for player in self.PLAYERS:
                with TabPane(player.title(), id=player):
                    yield Vertical(
                        Label(f"Player: {player.title()}", classes="menu-title"),
                        Label("Choose up to 5 cards:"),
                        Vertical(
                            *[
                                Checkbox(f"Card #{card}", id=f"card-{player}-{card}")
                                for card in self.player_cards.get(player, [])
                            ],
                            id=f"cards-{player}",
                        ),
                        Button("Submit squad", id=f"submit-{player}", variant="success"),
                        Label("Match status: waiting", id=f"status-{player}"),
                        Button("Report result as winner", id=f"result-{player}", variant="warning"),
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

        if action == "submit":
            self._submit_squad(player)
        elif action == "result":
            self._report_result(player)

    def _submit_squad(self, player: str) -> None:
        if self.winner:
            self._set_status(player, "Match already reported")
            return
        if self.submitted.get(player, False):
            self._set_status(player, f"Squad already submitted: {self.squads.get(player, [])}")
            return

        cards_box = self.query_one(f"#cards-{player}")
        card_checks = list(cards_box.query(Checkbox))
        if not card_checks:
            self._set_status(player, "No cards available to choose")
            return
        selected = [
            int(cb.id.split("-")[-1])
            for cb in card_checks
            if cb.value
        ]
        if len(selected) != 5:
            self._set_status(player, "Select exactly 5 cards before submit")
            return

        self.squads[player] = selected
        self.submitted[player] = True
        self._set_status(player, f"Squad submitted and locked: {selected}")
        self._refresh_report_buttons()

    def _report_result(self, player: str) -> None:
        if self.winner:
            self._set_status(player, f"Winner already set: {self.winner}")
            return
        submitted_players = [p for p, done in self.submitted.items() if done]
        if len(submitted_players) < 2:
            self._set_status(player, "Need two submitted squads before reporting")
            return
        self.winner = player
        for p in self.PLAYERS:
            self._set_status(p, f"Result reported, winner: {player}")
        self.match_history.append(
            {
                "winner": player,
                "squads": {k: v[:] for k, v in self.squads.items()},
                "timestamp": time(),
            }
        )
        self._refresh_report_buttons()

    def _set_status(self, player: str, message: str) -> None:
        label = self.query_one(f"#status-{player}", Label)
        label.update(f"Match status: {message}")

    def _refresh_report_buttons(self) -> None:
        ready = len([p for p, done in self.submitted.items() if done]) >= 2 and not self.winner
        for player in self.PLAYERS:
            btn = self.query_one(f"#result-{player}", Button)
            btn.disabled = not ready
