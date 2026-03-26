"""Text-oriented view helpers for the in-core CLI (no UI framework deps)."""

from __future__ import annotations

from tictactoe.reducer import GameState, describe_outcome

_EMPTY = "·"


def empty_cell_glyph() -> str:
    return _EMPTY


def header_line(state: GameState) -> str:
    oc = describe_outcome(state)
    if oc:
        return oc
    return f"Turn: {state.current_player.value}"


def intro_line() -> str:
    return (
        f"Positions 1–9 are left→right, top→bottom "
        f"(empty cells show as {_EMPTY})."
    )


def board_lines(state: GameState) -> list[str]:
    b = state.board
    lines: list[str] = []
    for r in range(3):
        row_cells: list[str] = []
        for c in range(3):
            i = r * 3 + c
            mark = b[i]
            row_cells.append(mark if mark is not None else _EMPTY)
        lines.append(" " + " | ".join(row_cells) + " ")
        if r < 2:
            lines.append("---+---+---")
    return lines


def board_text(state: GameState) -> str:
    return "\n".join(board_lines(state))
