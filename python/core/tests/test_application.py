"""Tests for GameSession (application service)."""

from __future__ import annotations

import pytest

from tictactoe.application import GameOverError, GameSession
from tictactoe.reducer import CellOccupiedError
from tictactoe.types import Outcome, Player, cell_index


def test_initial_state() -> None:
    gs = GameSession()
    assert gs.state.outcome is Outcome.IN_PROGRESS
    assert gs.state.current_player is Player.X


def test_valid_move_returns_none() -> None:
    gs = GameSession()
    assert gs.place(cell_index(0)) is None


def test_valid_move_updates_state() -> None:
    gs = GameSession()
    gs.place(cell_index(0))
    assert gs.state.board[0] is Player.X


def test_occupied_cell_raises_cell_occupied_error() -> None:
    gs = GameSession()
    gs.place(cell_index(0))
    with pytest.raises(CellOccupiedError) as exc_info:
        gs.place(cell_index(0))
    assert exc_info.value.cell == cell_index(0)


def test_occupied_cell_error_message_mentions_cell_number() -> None:
    gs = GameSession()
    gs.place(cell_index(0))
    with pytest.raises(CellOccupiedError) as exc_info:
        gs.place(cell_index(0))
    # cell_index(0) is UI cell 1
    assert "1" in str(exc_info.value)


def test_occupied_cell_does_not_change_state() -> None:
    gs = GameSession()
    gs.place(cell_index(0))
    state_before = gs.state
    with pytest.raises(CellOccupiedError):
        gs.place(cell_index(0))
    assert gs.state is state_before


def test_move_after_game_finished_raises_game_over_error() -> None:
    gs = GameSession()
    for cell in (0, 3, 1, 4, 2):  # X wins top row
        gs.place(cell_index(cell))
    with pytest.raises(GameOverError) as exc_info:
        gs.place(cell_index(5))
    assert exc_info.value.outcome is Outcome.WIN_X


def test_game_over_error_message_mentions_outcome() -> None:
    gs = GameSession()
    for cell in (0, 3, 1, 4, 2):
        gs.place(cell_index(cell))
    with pytest.raises(GameOverError) as exc_info:
        gs.place(cell_index(5))
    assert "win_x" in str(exc_info.value).lower()


def test_reset_restarts_game() -> None:
    gs = GameSession()
    for cell in (0, 3, 1, 4, 2):
        gs.place(cell_index(cell))
    gs.reset()
    assert gs.state.outcome is Outcome.IN_PROGRESS
    assert gs.state.move_count == 0
    assert all(c is None for c in gs.state.board)


def test_move_after_reset_is_valid() -> None:
    gs = GameSession()
    for cell in (0, 3, 1, 4, 2):
        gs.place(cell_index(cell))
    gs.reset()
    assert gs.place(cell_index(0)) is None
