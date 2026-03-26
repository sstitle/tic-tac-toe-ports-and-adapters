"""Qt GUI: wires ``GameSession`` (port) to widgets."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from tictactoe.application import GameSession
from tictactoe.presentation import header_line
from tictactoe.types import cell_index


class BoardWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.session = GameSession()
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
        outer = QVBoxLayout()
        outer.addWidget(self._status)
        outer.addLayout(grid)
        outer.addWidget(reset)
        self.setLayout(outer)
        self._refresh()

    def _refresh(self) -> None:
        self._status.setText(header_line(self.session.state))
        for i, btn in enumerate(self._buttons):
            cell = self.session.state.board[i]
            btn.setText(cell.value if cell else "·")

    def _on_cell(self, i: int) -> None:
        err = self.session.place(cell_index(i))
        if err:
            QMessageBox.warning(self, "Invalid move", err)
        self._refresh()

    def _on_reset(self) -> None:
        self.session.reset()
        self._refresh()


def main() -> None:
    app = QApplication([])
    w = BoardWidget()
    w.setWindowTitle("Tic-tac-toe")
    w.resize(320, 380)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
