from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

class Eleventh(App):

    BINDINGS = [("escape", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

    def action_quit(self) -> None:
        self.exit()

