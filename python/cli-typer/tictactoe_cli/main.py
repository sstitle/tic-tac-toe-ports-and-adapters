"""Typer-based terminal UI: talks to :class:`~tictactoe.application.GameSession` (the port implementation)."""

from __future__ import annotations

import typer

from tictactoe.application import GameSession
from tictactoe.reducer import describe_outcome
from tictactoe.types import Outcome, cell_index
from tictactoe.presentation import board_text, header_line, intro_line

app = typer.Typer(help="Tic-tac-toe: ports & application + Typer CLI.")


@app.command()
def play() -> None:
    """Play an interactive game (cells 1–9, q to quit, r to reset)."""
    session = GameSession()
    typer.echo(header_line(session.state))
    typer.echo(intro_line())
    typer.echo(board_text(session.state))
    while True:
        state = session.state
        if state.outcome is not Outcome.IN_PROGRESS:
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
        idx = cell_index(n - 1)
        err = session.place(idx)
        if err is not None:
            typer.echo(err)
            continue
        typer.echo(header_line(session.state))
        typer.echo(board_text(session.state))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
