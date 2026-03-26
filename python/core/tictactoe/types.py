"""Domain primitives: NewTypes and small constructors for tic-tac-toe."""

from __future__ import annotations

from enum import StrEnum
from typing import NewType

# --- NewTypes (domain identity) ---

CellIndex = NewType("CellIndex", int)
RowIndex = NewType("RowIndex", int)
ColIndex = NewType("ColIndex", int)
MoveCount = NewType("MoveCount", int)
WinLineIndex = NewType("WinLineIndex", int)


class Player(StrEnum):
    X = "X"
    O = "O"


class Outcome(StrEnum):
    IN_PROGRESS = "in_progress"
    WIN_X = "win_x"
    WIN_O = "win_o"
    DRAW = "draw"


def cell_index(value: int) -> CellIndex:
    if not 0 <= value < 9:
        msg = f"cell index must be 0..8, got {value}"
        raise ValueError(msg)
    return CellIndex(value)


def row_index(value: int) -> RowIndex:
    if not 0 <= value < 3:
        msg = f"row index must be 0..2, got {value}"
        raise ValueError(msg)
    return RowIndex(value)


def col_index(value: int) -> ColIndex:
    if not 0 <= value < 3:
        msg = f"col index must be 0..2, got {value}"
        raise ValueError(msg)
    return ColIndex(value)


def win_line_index(value: int) -> WinLineIndex:
    if not 0 <= value < 8:
        msg = f"win line index must be 0..7, got {value}"
        raise ValueError(msg)
    return WinLineIndex(value)


def cell_from_row_col(row: RowIndex, col: ColIndex) -> CellIndex:
    return cell_index(int(row) * 3 + int(col))


def row_col_from_cell(index: CellIndex) -> tuple[RowIndex, ColIndex]:
    v = int(index)
    return row_index(v // 3), col_index(v % 3)


Board = NewType("Board", tuple[Player | None, ...])


def empty_board() -> Board:
    return Board((None,) * 9)


WIN_LINES: tuple[tuple[CellIndex, CellIndex, CellIndex], ...] = (
    (cell_index(0), cell_index(1), cell_index(2)),
    (cell_index(3), cell_index(4), cell_index(5)),
    (cell_index(6), cell_index(7), cell_index(8)),
    (cell_index(0), cell_index(3), cell_index(6)),
    (cell_index(1), cell_index(4), cell_index(7)),
    (cell_index(2), cell_index(5), cell_index(8)),
    (cell_index(0), cell_index(4), cell_index(8)),
    (cell_index(2), cell_index(4), cell_index(6)),
)
