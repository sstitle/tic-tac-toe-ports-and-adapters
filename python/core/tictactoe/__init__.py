"""Tic-tac-toe core: NewTyped domain, reducer, CLI entry in `tictactoe.cli`."""

from tictactoe.reducer import Action, GameState, PlaceMark, ResetGame, initial_state, reduce
from tictactoe.types import (
    Board,
    CellIndex,
    ColIndex,
    MoveCount,
    Outcome,
    Player,
    RowIndex,
    WinLineIndex,
    cell_from_row_col,
    cell_index,
    col_index,
    empty_board,
    row_col_from_cell,
    row_index,
    win_line_index,
)

__all__ = [
    "Action",
    "Board",
    "CellIndex",
    "ColIndex",
    "GameState",
    "MoveCount",
    "Outcome",
    "PlaceMark",
    "Player",
    "ResetGame",
    "RowIndex",
    "WinLineIndex",
    "cell_from_row_col",
    "cell_index",
    "col_index",
    "empty_board",
    "initial_state",
    "reduce",
    "row_col_from_cell",
    "row_index",
    "win_line_index",
]
