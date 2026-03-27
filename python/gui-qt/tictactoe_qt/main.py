"""Qt GUI: wires ``GameSession`` (port) to widgets."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tictactoe.application import GameSession
from tictactoe.minimax import MinimaxStrategy
from tictactoe.ports import MoveStrategyPort
from tictactoe.reducer import GameError, describe_outcome
from tictactoe.types import Player, cell_index

_EMPTY = "·"
_X_COLOR = "#0891b2"
_O_COLOR = "#c026d3"


def _status_html(state) -> str:
    oc = describe_outcome(state)
    if oc:
        return f"<b style='color: #16a34a'>{oc}</b>"
    color = _X_COLOR if state.current_player is Player.X else _O_COLOR
    return f"Turn: <b style='color: {color}'>{state.current_player.value}</b>"


class BoardWidget(QWidget):
    def __init__(self, vs_computer: bool = False) -> None:
        super().__init__()
        self.session = GameSession()
        self.strategy: MoveStrategyPort | None = MinimaxStrategy() if vs_computer else None
        self._status = QLabel()
        self._buttons: list[QPushButton] = []
        grid = QGridLayout()
        for i in range(9):
            btn = QPushButton()
            btn.setFixedSize(72, 72)
            btn.clicked.connect(lambda checked=False, idx=i: self._on_cell(idx))
            grid.addWidget(btn, i // 3, i % 3)
            self._buttons.append(btn)
        reset = QPushButton("New game")
        reset.clicked.connect(self._on_reset)
        self._ai_toggle = QCheckBox("Play vs computer (AI is O)")
        self._ai_toggle.setChecked(vs_computer)
        self._ai_toggle.toggled.connect(self._on_ai_toggled)
        outer = QVBoxLayout()
        outer.addWidget(self._status)
        outer.addLayout(grid)
        outer.addWidget(reset)
        outer.addWidget(self._ai_toggle)
        self.setLayout(outer)
        self._refresh()

    def _refresh(self) -> None:
        self._status.setText(_status_html(self.session.state))
        for i, btn in enumerate(self._buttons):
            cell = self.session.state.board[i]
            btn.setText(cell.value if cell else _EMPTY)
            if cell is Player.X:
                btn.setStyleSheet(
                    f"color: {_X_COLOR}; font-weight: bold; font-size: 20px;"
                )
            elif cell is Player.O:
                btn.setStyleSheet(
                    f"color: {_O_COLOR}; font-weight: bold; font-size: 20px;"
                )
            else:
                btn.setStyleSheet("font-size: 20px;")

    def _on_ai_toggled(self, checked: bool) -> None:
        self.strategy = MinimaxStrategy() if checked else None

    def _on_cell(self, i: int) -> None:
        try:
            self.session.place(cell_index(i))
        except GameError as exc:
            QMessageBox.warning(self, "Invalid move", str(exc))
            return
        # AI response after a valid human move.
        if self.strategy is not None and not self.session.is_over:
            ai_cell = self.strategy.choose_move(self.session.state)
            if ai_cell is not None:
                self.session.place(ai_cell)
        self._refresh()

    def _on_reset(self) -> None:
        self.session.reset()
        self._refresh()


def main() -> None:
    vs_computer = "--vs-computer" in sys.argv
    qt_app = QApplication(sys.argv)
    w = BoardWidget(vs_computer=vs_computer)
    w.setWindowTitle("Tic-tac-toe")
    w.resize(320, 420)
    w.show()
    qt_app.exec()


if __name__ == "__main__":
    main()
