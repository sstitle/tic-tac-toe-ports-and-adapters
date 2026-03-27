"""Property-based tests using Hypothesis."""

from __future__ import annotations

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from tictactoe.errors import CellOccupiedError
from tictactoe.minimax import best_move
from tictactoe.reducer import PlaceMark, initial_state, reduce
from tictactoe.types import Outcome, Player, cell_index

# Generate valid game sequences: a random-length prefix of a random permutation
# of all 9 cells. This guarantees no repeated cells and produces reachable states.
_valid_move_sequence_st = st.integers(min_value=0, max_value=9).flatmap(
    lambda n: st.permutations(list(range(9))).map(lambda p: p[:n])
)


def _play(*cells: int):
    state = initial_state()
    for c in cells:
        if state.outcome is not Outcome.IN_PROGRESS:
            break
        state = reduce(state, PlaceMark(cell=cell_index(c)))
    return state


class TestMarkCountInvariant:
    @given(_valid_move_sequence_st)
    def test_x_count_leads_or_ties_o(self, cells: list[int]) -> None:
        state = _play(*cells)
        x_count = sum(1 for c in state.board if c is Player.X)
        o_count = sum(1 for c in state.board if c is Player.O)
        assert x_count == o_count or x_count == o_count + 1


class TestMoveCountMatchesBoard:
    @given(_valid_move_sequence_st)
    def test_move_count_equals_occupied_cells(self, cells: list[int]) -> None:
        state = _play(*cells)
        occupied = sum(1 for c in state.board if c is not None)
        assert state.move_count == occupied


class TestOutcomeConsistency:
    @given(_valid_move_sequence_st)
    def test_outcome_consistent_with_board(self, cells: list[int]) -> None:
        state = _play(*cells)
        if state.outcome is Outcome.WIN_X:
            assert state.winning_line is not None
            a, b, c = state.winning_line
            assert state.board[int(a)] is state.board[int(b)] is state.board[int(c)] is Player.X
        elif state.outcome is Outcome.WIN_O:
            assert state.winning_line is not None
            a, b, c = state.winning_line
            assert state.board[int(a)] is state.board[int(b)] is state.board[int(c)] is Player.O
        elif state.outcome is Outcome.DRAW:
            assert all(c is not None for c in state.board)
            assert state.winning_line is None
        else:
            assert state.winning_line is None


class TestReducerDeterminism:
    @given(_valid_move_sequence_st)
    def test_same_sequence_same_state(self, cells: list[int]) -> None:
        assert _play(*cells) == _play(*cells)


class TestMinimaxProperties:
    @given(_valid_move_sequence_st)
    @settings(max_examples=50)
    def test_minimax_never_picks_occupied_cell(self, cells: list[int]) -> None:
        state = _play(*cells)
        assume(state.outcome is Outcome.IN_PROGRESS)
        move = best_move(state)
        assert move is not None
        assert state.board[int(move)] is None

    @given(st.integers(min_value=0, max_value=8))
    @settings(max_examples=50)
    def test_ai_never_loses_from_any_human_opening(self, opening: int) -> None:
        # Human plays X first; AI plays O optimally for the rest.
        state = _play(opening)
        while state.outcome is Outcome.IN_PROGRESS:
            move = best_move(state)
            assert move is not None
            state = reduce(state, PlaceMark(cell=move))
        assert state.outcome is not Outcome.WIN_X


class TestReducerOccupiedCell:
    @given(_valid_move_sequence_st)
    def test_reducer_raises_on_occupied_cell(self, cells: list[int]) -> None:
        state = _play(*cells)
        occupied = [i for i in range(9) if state.board[i] is not None]
        assume(len(occupied) > 0)
        with pytest.raises(CellOccupiedError):
            reduce(state, PlaceMark(cell=cell_index(occupied[0])))
