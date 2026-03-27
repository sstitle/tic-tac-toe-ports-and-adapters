"""Application service: orchestrates the reducer; no UI or framework imports."""

from __future__ import annotations

from tictactoe.errors import GameOverError
from tictactoe.reducer import GameState, PlaceMark, ResetGame, initial_state, reduce
from tictactoe.types import CellIndex, Outcome


class GameSession:
    """Concrete implementation of :class:`~tictactoe.ports.GameSessionPort`."""

    __slots__ = ("_state",)

    def __init__(self) -> None:
        self._state = initial_state()

    @property
    def state(self) -> GameState:
        return self._state

    def place(self, cell: CellIndex) -> None:
        if self._state.outcome is not Outcome.IN_PROGRESS:
            raise GameOverError(self._state.outcome)
        self._state = reduce(self._state, PlaceMark(cell=cell))

    def reset(self) -> None:
        self._state = reduce(self._state, ResetGame())
