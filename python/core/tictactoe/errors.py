"""Domain-level exceptions raised by the application service."""

from __future__ import annotations

from tictactoe.types import CellIndex, Outcome


class GameError(Exception):
    """Base class for all game rule violations."""


class CellOccupiedError(GameError):
    """Raised when a player attempts to place on an already-occupied cell."""

    def __init__(self, cell: CellIndex) -> None:
        super().__init__(
            f"Cell {int(cell) + 1} is already occupied. Choose an empty cell."
        )
        self.cell = cell


class GameOverError(GameError):
    """Raised when a move is attempted after the game has finished."""

    def __init__(self, outcome: Outcome) -> None:
        super().__init__(
            f"The game is already finished ({outcome}). Start a new game or reset."
        )
        self.outcome = outcome
