"""Tests for domain primitives in tictactoe.types."""

from __future__ import annotations

import pytest

from tictactoe.types import (
    Board,
    cell_index,
    cell_from_row_col,
    col_index,
    empty_board,
    row_col_from_cell,
    row_index,
    win_line_index,
)


class TestBoard:
    def test_valid_board(self) -> None:
        b = empty_board()
        assert len(b) == 9

    def test_wrong_length_raises(self) -> None:
        with pytest.raises(ValueError, match="exactly 9 cells"):
            Board((None,) * 8)

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exactly 9 cells"):
            Board((None,) * 10)


class TestCellIndex:
    def test_valid_boundaries(self) -> None:
        assert cell_index(0) == 0
        assert cell_index(8) == 8

    def test_all_valid(self) -> None:
        for i in range(9):
            assert cell_index(i) == i

    def test_below_range(self) -> None:
        with pytest.raises(ValueError, match="0..8"):
            cell_index(-1)

    def test_above_range(self) -> None:
        with pytest.raises(ValueError, match="0..8"):
            cell_index(9)


class TestRowIndex:
    def test_valid_boundaries(self) -> None:
        assert row_index(0) == 0
        assert row_index(2) == 2

    def test_below_range(self) -> None:
        with pytest.raises(ValueError, match="0..2"):
            row_index(-1)

    def test_above_range(self) -> None:
        with pytest.raises(ValueError, match="0..2"):
            row_index(3)


class TestColIndex:
    def test_valid_boundaries(self) -> None:
        assert col_index(0) == 0
        assert col_index(2) == 2

    def test_below_range(self) -> None:
        with pytest.raises(ValueError, match="0..2"):
            col_index(-1)

    def test_above_range(self) -> None:
        with pytest.raises(ValueError, match="0..2"):
            col_index(3)


class TestWinLineIndex:
    def test_valid_boundaries(self) -> None:
        assert win_line_index(0) == 0
        assert win_line_index(7) == 7

    def test_below_range(self) -> None:
        with pytest.raises(ValueError):
            win_line_index(-1)

    def test_above_range(self) -> None:
        with pytest.raises(ValueError):
            win_line_index(8)


class TestCellRowColConversion:
    def test_cell_from_row_col_top_left(self) -> None:
        assert cell_from_row_col(row_index(0), col_index(0)) == 0

    def test_cell_from_row_col_bottom_right(self) -> None:
        assert cell_from_row_col(row_index(2), col_index(2)) == 8

    def test_cell_from_row_col_center(self) -> None:
        assert cell_from_row_col(row_index(1), col_index(1)) == 4

    def test_row_col_from_cell_top_left(self) -> None:
        assert row_col_from_cell(cell_index(0)) == (0, 0)

    def test_row_col_from_cell_bottom_right(self) -> None:
        assert row_col_from_cell(cell_index(8)) == (2, 2)

    def test_row_col_from_cell_center(self) -> None:
        assert row_col_from_cell(cell_index(4)) == (1, 1)

    def test_roundtrip_all_cells(self) -> None:
        for i in range(9):
            r, c = row_col_from_cell(cell_index(i))
            assert cell_from_row_col(r, c) == i
