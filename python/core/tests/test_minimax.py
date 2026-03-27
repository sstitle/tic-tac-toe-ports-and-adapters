"""Tests for the minimax solver."""

from __future__ import annotations

from tictactoe.minimax import best_move
from tictactoe.reducer import GameState, PlaceMark, initial_state, reduce
from tictactoe.types import Outcome, Player, cell_index


def _play(*cells: int) -> GameState:
    state = initial_state()
    for c in cells:
        state = reduce(state, PlaceMark(cell=cell_index(c)))
    return state


class TestBestMoveTerminalStates:
    def test_returns_none_on_win(self) -> None:
        state = _play(0, 3, 1, 4, 2)  # X wins
        assert best_move(state) is None

    def test_returns_none_on_draw(self) -> None:
        state = _play(0, 1, 2, 3, 5, 4, 6, 8, 7)
        assert best_move(state) is None


class TestBestMoveBlocksWin:
    def test_blocks_immediate_x_win(self) -> None:
        # X has 0,1 — O must block cell 2 to prevent X winning top row.
        state = _play(0, 4, 1)  # X:0,1  O:4
        move = best_move(state)  # O's turn
        assert move == cell_index(2)

    def test_blocks_immediate_o_win(self) -> None:
        # X:0,6  O:3,4 — O is one move from winning middle row at cell 5.
        # X has no immediate win so must block at 5.
        state = _play(0, 3, 6, 4)  # X:0,6  O:3,4
        move = best_move(state)  # X's turn
        assert move == cell_index(5)


class TestBestMoveTakesWin:
    def test_takes_winning_move_for_x(self) -> None:
        # X has 0,1 — should complete top row at cell 2.
        state = _play(0, 3, 1, 6)  # X:0,1  O:3,6
        move = best_move(state)  # X's turn
        assert move == cell_index(2)

    def test_takes_winning_move_for_o(self) -> None:
        # O has 3,4 — should complete middle row at cell 5.
        state = _play(0, 3, 2, 4, 8)  # X:0,2,8  O:3,4
        move = best_move(state)  # O's turn
        assert move == cell_index(5)


class TestBestMoveReturnsCellIndex:
    def test_returns_valid_cell_on_empty_board(self) -> None:
        move = best_move(initial_state())
        assert move is not None
        assert 0 <= int(move) <= 8

    def test_returned_cell_is_empty(self) -> None:
        state = _play(0, 1, 2, 3)
        move = best_move(state)
        assert move is not None
        assert state.board[int(move)] is None

    def test_perfect_play_never_loses(self) -> None:
        """AI vs AI always draws when both play optimally."""

        def play_to_end(state: GameState) -> Outcome:
            while state.outcome is Outcome.IN_PROGRESS:
                cell = best_move(state)
                assert cell is not None
                state = reduce(state, PlaceMark(cell=cell))
            return state.outcome

        result = play_to_end(initial_state())
        assert result is Outcome.DRAW
