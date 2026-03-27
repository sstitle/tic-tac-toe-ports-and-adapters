"""Textual TUI: wires ``GameSession`` (port) to widgets."""

from __future__ import annotations

import sys

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static

from tictactoe.application import GameSession
from tictactoe.minimax import MinimaxStrategy
from tictactoe.ports import MoveStrategyPort
from tictactoe.reducer import GameError, describe_outcome
from tictactoe.types import Player, cell_index

_EMPTY = "·"


def _status_markup(state) -> str:
    oc = describe_outcome(state)
    if oc:
        return f"[bold green]{oc}[/bold green]"
    color = "cyan" if state.current_player is Player.X else "magenta"
    return f"Turn: [bold {color}]{state.current_player.value}[/bold {color}]"


class TicTacToeTui(App[None]):
    """Board grid + status; uses :class:`~tictactoe.application.GameSession` only."""

    BINDINGS = [("q", "quit", "Quit")]
    CSS = """
    #status { padding: 0 1; }
    .x-cell { color: cyan; text-style: bold; }
    .o-cell { color: magenta; text-style: bold; }
    """

    def __init__(self, vs_computer: bool = False) -> None:
        super().__init__()
        self.session = GameSession()
        self.strategy: MoveStrategyPort | None = MinimaxStrategy() if vs_computer else None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="status")
        with Vertical(id="board"):
            for r in range(3):
                with Horizontal():
                    for c in range(3):
                        i = r * 3 + c
                        yield Button(_EMPTY, id=f"c{i}")
        yield Button("New game", id="reset", variant="warning")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_ui()

    def action_quit(self) -> None:
        self.exit()

    def refresh_ui(self) -> None:
        self.query_one("#status", Static).update(_status_markup(self.session.state))
        for i in range(9):
            btn = self.query_one(f"#c{i}", Button)
            cell = self.session.state.board[i]
            btn.label = cell.value if cell else _EMPTY
            btn.set_class(cell is Player.X, "x-cell")
            btn.set_class(cell is Player.O, "o-cell")

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
            if self.strategy is not None and not self.session.is_over:
                ai_cell = self.strategy.choose_move(self.session.state)
                if ai_cell is not None:
                    self.session.place(ai_cell)
            self.refresh_ui()


def main() -> None:
    vs_computer = "--vs-computer" in sys.argv
    TicTacToeTui(vs_computer=vs_computer).run()


if __name__ == "__main__":
    main()
