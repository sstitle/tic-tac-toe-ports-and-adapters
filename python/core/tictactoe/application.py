"""Application service: orchestrates the reducer; no UI or framework imports."""

from __future__ import annotations

from tictactoe.reducer import GameError, GameState, PlaceMark, ResetGame, initial_state, reduce
from tictactoe.types import CellIndex, Outcome


class GameOverError(GameError):
    """Raised when a move is attempted after the game has finished."""

    def __init__(self, outcome: Outcome) -> None:
        super().__init__(
            f"The game is already finished ({outcome}). Start a new game or reset."
        )
        self.outcome = outcome


class GameSession:
    """Concrete implementation of :class:`~tictactoe.ports.GameSessionPort`."""

    __slots__ = ("_state",)

    def __init__(self) -> None:
        self._state = initial_state()

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def is_over(self) -> bool:
        """True when the game has reached a terminal outcome."""
        return self._state.outcome is not Outcome.IN_PROGRESS

    def place(self, cell: CellIndex) -> None:
        if self.is_over:
            raise GameOverError(self._state.outcome)
        self._state = reduce(self._state, PlaceMark(cell=cell))

    def reset(self) -> None:
        self._state = reduce(self._state, ResetGame())
