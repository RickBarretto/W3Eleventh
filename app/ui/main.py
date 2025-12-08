from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

class Eleventh(App):

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()


