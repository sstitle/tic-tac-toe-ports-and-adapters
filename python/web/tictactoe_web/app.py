"""Flask app: one ``GameSession`` per browser session (signed cookie id); pure HTML buttons."""

from __future__ import annotations

import os
import secrets
import threading
import time
from dataclasses import dataclass, field
from typing import Final

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

from tictactoe.application import GameSession
from tictactoe.minimax import MinimaxStrategy
from tictactoe.ports import MoveStrategyPort
from tictactoe.presentation import empty_cell_glyph, header_line
from tictactoe.reducer import GameError
from tictactoe.types import Outcome, cell_index

_LOCK = threading.Lock()
_SESSION_TTL: Final[float] = 12 * 3600  # 12 hours


@dataclass
class _WebGame:
    session: GameSession = field(default_factory=GameSession)
    last_active: float = field(default_factory=time.time)
    strategy: MoveStrategyPort | None = None


_GAMES: dict[str, _WebGame] = {}


def _browser_id() -> str:
    sid = session.get("sid")
    if not sid:
        sid = secrets.token_hex(16)
        session["sid"] = sid
    return sid


def _evict_stale(now: float) -> None:
    stale = [k for k, wg in _GAMES.items() if now - wg.last_active > _SESSION_TTL]
    for k in stale:
        del _GAMES[k]


def _web_game() -> _WebGame:
    wg: _WebGame | None = getattr(g, "_web_game", None)
    if wg is None:
        bid = _browser_id()
        now = time.time()
        with _LOCK:
            _evict_stale(now)
            wg = _GAMES.get(bid)
            if wg is None:
                wg = _WebGame()
                _GAMES[bid] = wg
            else:
                wg.last_active = now
        g._web_game = wg  # type: ignore[attr-defined]
    return wg


def _cell_labels_and_disabled(st) -> tuple[list[str], list[bool]]:
    labels: list[str] = []
    disabled: list[bool] = []
    fin = st.outcome is not Outcome.IN_PROGRESS
    for i in range(9):
        mark = st.board[i]
        labels.append(mark.value if mark is not None else empty_cell_glyph())
        disabled.append(fin or mark is not None)
    return labels, disabled


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-change-me")

    @app.get("/")
    def index() -> str:
        wg = _web_game()
        st = wg.session.state
        labels, cell_disabled = _cell_labels_and_disabled(st)
        return render_template(
            "board.html",
            status=header_line(st),
            cell_label=labels,
            cell_disabled=cell_disabled,
            vs_computer=wg.strategy is not None,
        )

    @app.post("/move")
    def move() -> str:
        raw = request.form.get("cell")
        if raw is None or raw == "":
            flash("No cell submitted.")
            return redirect(url_for("index"))
        try:
            idx_int = int(raw)
        except ValueError:
            flash("Invalid cell.")
            return redirect(url_for("index"))
        try:
            idx = cell_index(idx_int)
        except ValueError as e:
            flash(str(e))
            return redirect(url_for("index"))
        wg = _web_game()
        try:
            wg.session.place(idx)
        except GameError as exc:
            flash(str(exc))
            return redirect(url_for("index"))
        # AI response after a valid human move.
        if wg.strategy is not None and not wg.session.is_over:
            ai_cell = wg.strategy.choose_move(wg.session.state)
            if ai_cell is not None:
                wg.session.place(ai_cell)
        return redirect(url_for("index"))

    @app.post("/reset")
    def new_game() -> str:
        _web_game().session.reset()
        return redirect(url_for("index"))

    @app.post("/toggle-ai")
    def toggle_ai() -> str:
        wg = _web_game()
        wg.strategy = None if wg.strategy is not None else MinimaxStrategy()
        return redirect(url_for("index"))

    return app


def main() -> None:
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    create_app().run(host=host, port=port, debug=os.environ.get("FLASK_DEBUG") == "1")


if __name__ == "__main__":
    main()
