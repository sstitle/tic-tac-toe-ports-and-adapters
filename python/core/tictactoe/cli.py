"""Typer CLI: drives the reducer in an interactive session."""

from __future__ import annotations

import typer

from tictactoe.reducer import GameState, PlaceMark, ResetGame, describe_outcome, initial_state, reduce
from tictactoe.types import Outcome, cell_index

app = typer.Typer(help="Tic-tac-toe: typed domain + reducer + Typer CLI.")

_EMPTY_CELL = "·"


def _render_board(state: GameState) -> str:
    b = state.board
    lines: list[str] = []
    for r in range(3):
        row_cells: list[str] = []
        for c in range(3):
            i = r * 3 + c
            mark = b[i]
            row_cells.append(mark if mark is not None else _EMPTY_CELL)
        lines.append(" " + " | ".join(row_cells) + " ")
        if r < 2:
            lines.append("---+---+---")
    return "\n".join(lines)


@app.command()
def play() -> None:
    """Play an interactive game (cells 1–9, q to quit, r to reset)."""
    state = initial_state()
    typer.echo(_header(state))
    typer.echo(
        f"Positions 1–9 are left→right, top→bottom "
        f"(empty cells show as {_EMPTY_CELL})."
    )
    typer.echo(_render_board(state))
    while True:
        if state.outcome is not Outcome.IN_PROGRESS:
            msg = describe_outcome(state)
            if msg:
                typer.echo(msg)
            again = typer.confirm("New game?", default=True)
            if not again:
                raise typer.Exit(0)
            state = reduce(state, ResetGame())
            typer.echo(_header(state))
            typer.echo(_render_board(state))
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
            state = reduce(state, ResetGame())
            typer.echo(_header(state))
            typer.echo(_render_board(state))
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
        if state.board[int(idx)] is not None:
            typer.echo(
                f"That cell is already occupied. Choose a cell that shows {_EMPTY_CELL} (empty)."
            )
            continue
        prev = state
        state = reduce(state, PlaceMark(cell=idx))
        if state.board == prev.board and state.outcome == prev.outcome:
            typer.echo(
                "That move could not be applied (game may already be finished)."
            )
            continue
        typer.echo(_header(state))
        typer.echo(_render_board(state))


def _header(state: GameState) -> str:
    oc = describe_outcome(state)
    if oc:
        return oc
    return f"Turn: {state.current_player.value}"


def main() -> None:
    app()


if __name__ == "__main__":
    main()
