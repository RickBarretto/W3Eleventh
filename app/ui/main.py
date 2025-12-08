from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import Footer, Header, Label, Button

from app.ui.menu import MenuScreen

class Eleventh(App):

    TITLE = "Eleventh"
    SUB_TITLE = "Web3 ed."

    CSS = """

    Screen {
        align: center middle;
    }

    #title {
        text-align: center;
        width: 50%;
        border: round white;
    }

    #start {
        align: center middle;
    }

    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Center():
            yield Label("[b]Eleventh[/b]", id="title", expand=True)
        with Center():
            yield Button(">> Start <<", id="start", compact=True)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.push_screen(MenuScreen())
