"""Minimax solver and its bundled MoveStrategyPort adapter.

The solver (``_minimax``, ``best_move``) is pure domain logic: no I/O, no
framework dependencies.  ``MinimaxStrategy`` is a thin adapter that satisfies
``MoveStrategyPort`` using that solver.  It ships here in ``core`` because the
algorithm has no external dependencies; adapters that want a different strategy
(random, LLM-backed, difficulty-limited) can implement ``MoveStrategyPort``
independently without touching this module.
"""

from __future__ import annotations

from functools import lru_cache

from tictactoe.reducer import GameState, PlaceMark, reduce
from tictactoe.types import CellIndex, Outcome, Player, cell_index


@lru_cache(maxsize=None)
def _minimax(state: GameState) -> int:
    """Score the position from X's perspective (positive = good for X).

    Uses remaining empty cells as a proxy for depth so the result is
    state-intrinsic and can be safely cached across transpositions.
    Faster wins score higher; faster losses score lower.
    """
    empty = sum(1 for c in state.board if c is None)
    if state.outcome is Outcome.WIN_X:
        return empty + 1
    if state.outcome is Outcome.WIN_O:
        return -(empty + 1)
    if state.outcome is Outcome.DRAW:
        return 0

    maximizing = state.current_player is Player.X
    best = -100 if maximizing else 100
    for i in range(9):
        if state.board[i] is None:
            child = reduce(state, PlaceMark(cell=cell_index(i)))
            score = _minimax(child)
            if maximizing:
                best = max(best, score)
            else:
                best = min(best, score)
    return best


class MinimaxStrategy:
    """``MoveStrategyPort`` implementation backed by the minimax solver."""

    def choose_move(self, state: GameState) -> CellIndex | None:
        return best_move(state)


def best_move(state: GameState) -> CellIndex | None:
    """Return the optimal cell for the current player, or None if the game is over."""
    if state.outcome is not Outcome.IN_PROGRESS:
        return None

    maximizing = state.current_player is Player.X
    best: tuple[int, CellIndex] | None = None
    for i in range(9):
        if state.board[i] is None:
            child = reduce(state, PlaceMark(cell=cell_index(i)))
            score = _minimax(child)
            if best is None:
                best = (score, cell_index(i))
            elif maximizing and score > best[0]:
                best = (score, cell_index(i))
            elif not maximizing and score < best[0]:
                best = (score, cell_index(i))
    return best[1] if best is not None else None
