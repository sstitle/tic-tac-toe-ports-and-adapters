"""Primary ports: contracts that outer drivers (CLI in core, separate TUI/GUI packages) implement against.

The **domain** (`types`, `reducer`) stays free of I/O and UI frameworks.

The **application** (`GameSession`) implements the use case and is exposed here as
`GameSessionPort` so any shell can depend on a stable interface. Separate packages
may provide Textual or Qt front-ends that call this port and render ``GameState``.
"""

from __future__ import annotations

from typing import Protocol

from tictactoe.reducer import GameState
from tictactoe.types import CellIndex


class GameSessionPort(Protocol):
    """Driving port: everything a user interface needs to drive one game."""

    @property
    def state(self) -> GameState:
        """Current immutable snapshot (same object identity may update between moves)."""
        ...

    def place(self, cell: CellIndex) -> None:
        """Apply a move for the current player.

        Raises:
            CellOccupiedError: if the target cell is already taken.
            GameOverError: if the game has already ended.
        """
        ...

    def reset(self) -> None:
        """Start a fresh game (same as domain ``ResetGame``)."""
        ...
