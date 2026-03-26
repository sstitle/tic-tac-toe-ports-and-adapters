"""Textual TUI: wires ``GameSession`` (port) to widgets."""

from __future__ import annotations

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static

from tictactoe.application import GameSession
from tictactoe.presentation import header_line
from tictactoe.types import cell_index


class TicTacToeTui(App[None]):
    """Board grid + status; uses :class:`~tictactoe.application.GameSession` only."""

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self.session = GameSession()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="status")
        with Vertical(id="board"):
            for r in range(3):
                with Horizontal():
                    for c in range(3):
                        i = r * 3 + c
                        yield Button("·", id=f"c{i}")
        yield Button("New game", id="reset", variant="warning")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_ui()

    def action_quit(self) -> None:
        self.exit()

    def refresh_ui(self) -> None:
        self.query_one("#status", Static).update(header_line(self.session.state))
        for i in range(9):
            btn = self.query_one(f"#c{i}", Button)
            cell = self.session.state.board[i]
            btn.label = cell.value if cell else "·"

    @on(Button.Pressed)
    def handle_button(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid == "reset":
            self.session.reset()
            self.refresh_ui()
            return
        if bid.startswith("c") and bid[1:].isdigit():
            i = int(bid[1:])
            err = self.session.place(cell_index(i))
            if err:
                self.notify(err, severity="error")
            self.refresh_ui()


def main() -> None:
    TicTacToeTui().run()


if __name__ == "__main__":
    main()
