"""Textual TUI: wires ``GameSession`` (port) to widgets."""

from __future__ import annotations

import sys

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static

from tictactoe.application import GameSession
from tictactoe.errors import GameError
from tictactoe.minimax import best_move
from tictactoe.presentation import header_line
from tictactoe.types import Outcome, cell_index


class TicTacToeTui(App[None]):
    """Board grid + status; uses :class:`~tictactoe.application.GameSession` only."""

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, vs_computer: bool = False) -> None:
        super().__init__()
        self.session = GameSession()
        self.vs_computer = vs_computer

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
            try:
                self.session.place(cell_index(i))
            except GameError as exc:
                self.notify(str(exc), severity="error")
                return
            # AI response after a valid human move.
            if self.vs_computer and self.session.state.outcome is Outcome.IN_PROGRESS:
                ai_cell = best_move(self.session.state)
                if ai_cell is not None:
                    self.session.place(ai_cell)
            self.refresh_ui()


def main() -> None:
    vs_computer = "--vs-computer" in sys.argv
    TicTacToeTui(vs_computer=vs_computer).run()


if __name__ == "__main__":
    main()
