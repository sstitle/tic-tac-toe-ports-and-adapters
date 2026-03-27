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
from tictactoe.errors import GameError
from tictactoe.minimax import MinimaxStrategy
from tictactoe.ports import MoveStrategyPort
from tictactoe.presentation import header_line
from tictactoe.types import Outcome, cell_index


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
        self._status.setText(header_line(self.session.state))
        for i, btn in enumerate(self._buttons):
            cell = self.session.state.board[i]
            btn.setText(cell.value if cell else "·")

    def _on_ai_toggled(self, checked: bool) -> None:
        self.strategy = MinimaxStrategy() if checked else None

    def _on_cell(self, i: int) -> None:
        try:
            self.session.place(cell_index(i))
        except GameError as exc:
            QMessageBox.warning(self, "Invalid move", str(exc))
            return
        # AI response after a valid human move.
        if self.strategy is not None and self.session.state.outcome is Outcome.IN_PROGRESS:
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
