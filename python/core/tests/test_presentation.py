"""Tests for tictactoe.presentation view helpers."""

from __future__ import annotations

from tictactoe.presentation import (
    board_lines,
    board_text,
    empty_cell_glyph,
    header_line,
    intro_line,
)
from tictactoe.reducer import initial_state, PlaceMark, reduce
from tictactoe.types import Outcome, Player, cell_index


def _play(*cells: int):
    state = initial_state()
    for c in cells:
        state = reduce(state, PlaceMark(cell=cell_index(c)))
    return state


class TestEmptyCellGlyph:
    def test_returns_string(self) -> None:
        assert isinstance(empty_cell_glyph(), str)

    def test_non_empty(self) -> None:
        assert len(empty_cell_glyph()) > 0


class TestHeaderLine:
    def test_in_progress_shows_current_player(self) -> None:
        state = initial_state()
        assert "X" in header_line(state)

    def test_after_one_move_shows_other_player(self) -> None:
        state = _play(0)
        assert "O" in header_line(state)

    def test_x_wins_shows_win_message(self) -> None:
        state = _play(0, 3, 1, 4, 2)  # X wins top row
        line = header_line(state)
        assert "X" in line
        assert "win" in line.lower()

    def test_o_wins_shows_win_message(self) -> None:
        state = _play(0, 3, 1, 4, 6, 5)  # O wins middle row
        line = header_line(state)
        assert "O" in line
        assert "win" in line.lower()

    def test_draw_shows_draw_message(self) -> None:
        state = _play(0, 1, 2, 3, 5, 4, 6, 8, 7)
        line = header_line(state)
        assert "draw" in line.lower()


class TestIntroLine:
    def test_returns_string(self) -> None:
        assert isinstance(intro_line(), str)

    def test_mentions_cell_range(self) -> None:
        line = intro_line()
        assert "1" in line and "9" in line


class TestBoardLines:
    def test_returns_five_lines(self) -> None:
        # 3 rows + 2 separators
        assert len(board_lines(initial_state())) == 5

    def test_empty_board_shows_glyphs(self) -> None:
        glyph = empty_cell_glyph()
        for line in board_lines(initial_state()):
            if "|" in line:
                assert glyph in line

    def test_placed_mark_appears_in_row(self) -> None:
        state = _play(0)  # X at top-left
        lines = board_lines(state)
        assert "X" in lines[0]

    def test_separators_between_rows(self) -> None:
        lines = board_lines(initial_state())
        assert "---" in lines[1]
        assert "---" in lines[3]

    def test_all_marks_reflected(self) -> None:
        state = _play(0, 4, 8)  # X at 0, 8; O at 4
        lines = board_lines(state)
        full = "\n".join(lines)
        assert full.count("X") == 2
        assert full.count("O") == 1


class TestBoardText:
    def test_newline_separated(self) -> None:
        text = board_text(initial_state())
        assert "\n" in text

    def test_consistent_with_board_lines(self) -> None:
        state = _play(0, 1, 2)
        assert board_text(state) == "\n".join(board_lines(state))
