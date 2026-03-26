"""Application service: orchestrates the reducer; no UI or framework imports."""

from __future__ import annotations

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

    def place(self, cell: CellIndex) -> str | None:
        if self._state.outcome is not Outcome.IN_PROGRESS:
            return "The game is already finished. Start a new game or reset."
        if self._state.board[int(cell)] is not None:
            return (
                "That cell is already occupied. Choose an empty cell "
                "(shown as · in text UIs)."
            )
        prev = self._state
        self._state = reduce(self._state, PlaceMark(cell=cell))
        if self._state.board == prev.board and self._state.outcome == prev.outcome:
            return "That move could not be applied."
        return None

    def reset(self) -> None:
        self._state = reduce(self._state, ResetGame())
