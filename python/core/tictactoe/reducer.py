"""Immutable game state and pure reducer over actions."""

from __future__ import annotations

from dataclasses import dataclass

from tictactoe.types import (
    Board,
    CellIndex,
    MoveCount,
    Outcome,
    Player,
    WIN_LINES,
    empty_board,
)


@dataclass(frozen=True)
class GameState:
    board: Board
    current_player: Player
    outcome: Outcome
    move_count: MoveCount
    winning_line: tuple[CellIndex, CellIndex, CellIndex] | None = None


def initial_state() -> GameState:
    return GameState(
        board=empty_board(),
        current_player=Player.X,
        outcome=Outcome.IN_PROGRESS,
        move_count=MoveCount(0),
    )


@dataclass(frozen=True)
class PlaceMark:
    cell: CellIndex


@dataclass(frozen=True)
class ResetGame:
    pass


Action = PlaceMark | ResetGame


def _winner_for_line(
    board: Board, a: CellIndex, b: CellIndex, c: CellIndex
) -> Player | None:
    x, y, z = board[int(a)], board[int(b)], board[int(c)]
    if x is not None and x == y == z:
        return x
    return None


def _outcome_after_move(
    board: Board,
) -> tuple[Outcome, tuple[CellIndex, CellIndex, CellIndex] | None]:
    for a, b, c in WIN_LINES:
        w = _winner_for_line(board, a, b, c)
        if w is not None:
            outcome = Outcome.WIN_X if w is Player.X else Outcome.WIN_O
            return outcome, (a, b, c)
    if all(cell is not None for cell in board):
        return Outcome.DRAW, None
    return Outcome.IN_PROGRESS, None


def _other(p: Player) -> Player:
    return Player.O if p is Player.X else Player.X


def reduce(state: GameState, action: Action) -> GameState:
    match action:
        case ResetGame():
            return initial_state()
        case PlaceMark(cell=idx):
            b = state.board
            cells = list(b)
            p = state.current_player
            cells[int(idx)] = p
            new_board = Board(tuple(cells))
            new_moves = MoveCount(int(state.move_count) + 1)
            oc, wline = _outcome_after_move(new_board)
            next_player = _other(p) if oc is Outcome.IN_PROGRESS else p
            return GameState(
                board=new_board,
                current_player=next_player,
                outcome=oc,
                move_count=new_moves,
                winning_line=wline,
            )
        case _:
            raise TypeError(f"Unknown action type: {type(action)!r}")


def describe_outcome(state: GameState) -> str | None:
    match state.outcome:
        case Outcome.IN_PROGRESS:
            return None
        case Outcome.WIN_X:
            return "X wins."
        case Outcome.WIN_O:
            return "O wins."
        case Outcome.DRAW:
            return "Draw."
