"""Tests for the pure reducer and GameState."""

from __future__ import annotations

import pytest

from tictactoe.reducer import (
    GameState,
    PlaceMark,
    ResetGame,
    describe_outcome,
    initial_state,
    reduce,
)
from tictactoe.types import Outcome, Player, cell_index


def place(state: GameState, cell: int) -> GameState:
    return reduce(state, PlaceMark(cell=cell_index(cell)))


def play(*cells: int) -> GameState:
    """Apply a sequence of moves to an initial state."""
    state = initial_state()
    for c in cells:
        state = place(state, c)
    return state


class TestInitialState:
    def test_board_empty(self) -> None:
        state = initial_state()
        assert all(cell is None for cell in state.board)

    def test_x_goes_first(self) -> None:
        assert initial_state().current_player is Player.X

    def test_outcome_in_progress(self) -> None:
        assert initial_state().outcome is Outcome.IN_PROGRESS

    def test_move_count_zero(self) -> None:
        assert initial_state().move_count == 0


class TestPlaceMark:
    def test_places_mark_on_board(self) -> None:
        state = play(0)
        assert state.board[0] is Player.X

    def test_alternates_players(self) -> None:
        state = play(0)
        assert state.current_player is Player.O
        state = play(0, 1)
        assert state.current_player is Player.X

    def test_increments_move_count(self) -> None:
        assert play(0).move_count == 1
        assert play(0, 1).move_count == 2

    def test_occupied_cell_overwritten_by_reducer(self) -> None:
        # The reducer no longer guards against occupied cells — that's GameSession's job.
        # Placing on an occupied cell simply overwrites it.
        state = play(0)
        state2 = place(state, 0)
        assert state2 is not state

    def test_state_is_immutable(self) -> None:
        s1 = initial_state()
        s2 = place(s1, 0)
        assert s1.board[0] is None  # original unchanged
        assert s2.board[0] is Player.X


class TestWinDetection:
    @pytest.mark.parametrize("a,b,c,o1,o2", [
        # rows
        (0, 1, 2, 3, 4),
        (3, 4, 5, 0, 1),
        (6, 7, 8, 0, 1),
        # columns
        (0, 3, 6, 1, 2),
        (1, 4, 7, 0, 2),
        (2, 5, 8, 0, 1),
        # diagonals
        (0, 4, 8, 1, 2),
        (2, 4, 6, 0, 1),
    ])
    def test_x_wins_all_lines(self, a: int, b: int, c: int, o1: int, o2: int) -> None:
        state = play(a, o1, b, o2, c)
        assert state.outcome is Outcome.WIN_X

    def test_o_wins(self) -> None:
        # O wins: X on 0,1,6 O on 3,4,5
        state = play(0, 3, 1, 4, 6, 5)
        assert state.outcome is Outcome.WIN_O

    def test_current_player_frozen_after_win(self) -> None:
        state = play(0, 3, 1, 4, 2)  # X wins
        assert state.current_player is Player.X  # stays on winner


class TestWinningLine:
    def test_winning_line_set_on_win(self) -> None:
        state = play(0, 3, 1, 4, 2)  # X wins top row
        assert state.winning_line == (0, 1, 2)

    def test_winning_line_none_in_progress(self) -> None:
        assert initial_state().winning_line is None

    def test_winning_line_none_on_draw(self) -> None:
        state = play(0, 1, 2, 3, 5, 4, 6, 8, 7)
        assert state.winning_line is None

    def test_winning_line_diagonal(self) -> None:
        state = play(0, 1, 4, 2, 8)  # X wins main diagonal
        assert state.winning_line == (0, 4, 8)


class TestDrawDetection:
    def test_draw(self) -> None:
        # X: 0,2,5,6,7  O: 1,3,4,8  — no winner
        state = play(0, 1, 2, 3, 5, 4, 6, 8, 7)
        assert state.outcome is Outcome.DRAW

    def test_draw_move_count(self) -> None:
        state = play(0, 1, 2, 3, 5, 4, 6, 8, 7)
        assert state.move_count == 9


class TestResetGame:
    def test_reset_returns_initial(self) -> None:
        state = play(0, 1, 2)
        reset = reduce(state, ResetGame())
        assert reset == initial_state()


class TestUnknownAction:
    def test_unknown_action_raises(self) -> None:
        import pytest
        with pytest.raises(TypeError, match="Unknown action type"):
            reduce(initial_state(), object())  # type: ignore[arg-type]


class TestDescribeOutcome:
    def test_in_progress_is_none(self) -> None:
        assert describe_outcome(initial_state()) is None

    def test_win_x(self) -> None:
        state = play(0, 3, 1, 4, 2)
        assert describe_outcome(state) == "X wins."

    def test_win_o(self) -> None:
        state = play(0, 3, 1, 4, 6, 5)
        assert describe_outcome(state) == "O wins."

    def test_draw(self) -> None:
        state = play(0, 1, 2, 3, 5, 4, 6, 8, 7)
        assert describe_outcome(state) == "Draw."
