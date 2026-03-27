"""Typer-based terminal UI: talks to :class:`~tictactoe.application.GameSession` (the port implementation)."""

from __future__ import annotations

import typer

from tictactoe.application import GameSession
from tictactoe.minimax import MinimaxStrategy
from tictactoe.ports import MoveStrategyPort
from tictactoe.presentation import board_text, header_line, intro_line
from tictactoe.reducer import GameError, describe_outcome
from tictactoe.types import cell_index

app = typer.Typer(help="Tic-tac-toe: ports & application + Typer CLI.")


@app.command()
def play(
    vs_computer: bool = typer.Option(
        False, "--vs-computer", "-c", help="Play against the minimax AI (you are X)."
    ),
) -> None:
    """Play an interactive game (cells 1–9, q to quit, r to reset)."""
    strategy: MoveStrategyPort | None = MinimaxStrategy() if vs_computer else None
    session = GameSession()
    typer.echo(header_line(session.state))
    typer.echo(intro_line())
    typer.echo(board_text(session.state))
    while True:
        state = session.state
        if session.is_over:
            msg = describe_outcome(state)
            if msg:
                typer.echo(msg)
            again = typer.confirm("New game?", default=True)
            if not again:
                raise typer.Exit(0)
            session.reset()
            typer.echo(header_line(session.state))
            typer.echo(board_text(session.state))
            continue

        raw = typer.prompt(
            f"{state.current_player.value}'s move (1–9, r=reset, q=quit)",
            default="",
            show_default=False,
        ).strip()
        lowered = raw.lower()
        if lowered in {"q", "quit", "exit"}:
            raise typer.Exit(0)
        if lowered == "r":
            session.reset()
            typer.echo(header_line(session.state))
            typer.echo(board_text(session.state))
            continue
        if raw == "":
            typer.echo(
                "Type a cell number 1–9 to move, r to reset the game, or q to quit."
            )
            continue
        try:
            n = int(raw)
        except ValueError:
            typer.echo(
                "That is not a number. Use 1–9 for a cell, r to reset, or q to quit."
            )
            continue
        if not 1 <= n <= 9:
            typer.echo(
                f"Cell must be between 1 and 9 (you entered {n}). "
                "Numbers map to the board left→right, top→bottom."
            )
            continue
        # UI cells are 1-9; internal indices are 0-8.
        idx = cell_index(n - 1)
        try:
            session.place(idx)
        except GameError as exc:
            typer.echo(str(exc))
            continue
        typer.echo(header_line(session.state))
        typer.echo(board_text(session.state))

        # AI response (plays as the next player, optimally).
        if strategy is not None and not session.is_over:
            ai_cell = strategy.choose_move(session.state)
            if ai_cell is not None:
                session.place(ai_cell)
                typer.echo(f"AI plays: {int(ai_cell) + 1}")
                typer.echo(header_line(session.state))
                typer.echo(board_text(session.state))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
