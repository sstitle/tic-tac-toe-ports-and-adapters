"""Flask app: one ``GameSession`` per browser session (signed cookie id); pure HTML buttons."""

from __future__ import annotations

import os
import secrets
import threading
from typing import Final

from flask import Flask, flash, redirect, render_template_string, request, session, url_for

from tictactoe.application import GameSession
from tictactoe.presentation import header_line
from tictactoe.types import Outcome, cell_index

_LOCK = threading.Lock()
_GAMES: dict[str, GameSession] = {}

_PAGE: Final[str] = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Tic-tac-toe</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 28rem; margin: 2rem auto; padding: 0 1rem; }
    h1 { font-size: 1.1rem; font-weight: 600; }
    .flash { color: #b45309; margin: 0.75rem 0; }
    .grid { display: grid; grid-template-columns: repeat(3, minmax(4rem, 1fr)); gap: 0.5rem; margin: 1rem 0; }
    .grid button { min-height: 3.5rem; font-size: 1.35rem; cursor: pointer; }
    .grid button:disabled { cursor: not-allowed; opacity: 0.75; }
    .actions { margin-top: 1rem; }
    .actions button { font-size: 1rem; padding: 0.35rem 0.75rem; cursor: pointer; }
    .hint { font-size: 0.85rem; color: #444; margin-top: 1.5rem; }
  </style>
</head>
<body>
  <h1>{{ status }}</h1>
  {% for msg in get_flashed_messages() %}
  <p class="flash">{{ msg }}</p>
  {% endfor %}
  <form method="post" action="{{ url_for('move') }}">
    <div class="grid">
      {% for i in range(9) %}
      <button
        type="submit"
        name="cell"
        value="{{ i }}"
        {% if cell_disabled[i] %}disabled{% endif %}
        aria-label="Cell {{ i + 1 }}"
      >{{ cell_label[i] }}</button>
      {% endfor %}
    </div>
  </form>
  <form class="actions" method="post" action="{{ url_for('reset') }}">
    <button type="submit">New game</button>
  </form>
  <p class="hint">Empty squares show ·. Cells are numbered 1–9 left to right, top to bottom.</p>
</body>
</html>
"""


def _browser_id() -> str:
    sid = session.get("sid")
    if not sid:
        sid = secrets.token_hex(16)
        session["sid"] = sid
    return sid


def _game() -> GameSession:
    bid = _browser_id()
    with _LOCK:
        if bid not in _GAMES:
            _GAMES[bid] = GameSession()
        return _GAMES[bid]


def _cell_labels_and_disabled(st) -> tuple[list[str], list[bool]]:
    labels: list[str] = []
    disabled: list[bool] = []
    for i in range(9):
        mark = st.board[i]
        labels.append(mark.value if mark is not None else "·")
        fin = st.outcome is not Outcome.IN_PROGRESS
        disabled.append(fin or mark is not None)
    return labels, disabled


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-change-me")

    @app.get("/")
    def index() -> str:
        g = _game()
        st = g.state
        labels, cell_disabled = _cell_labels_and_disabled(st)
        return render_template_string(
            _PAGE,
            status=header_line(st),
            cell_label=labels,
            cell_disabled=cell_disabled,
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
        err = _game().place(idx)
        if err is not None:
            flash(err)
        return redirect(url_for("index"))

    @app.post("/reset")
    def reset() -> str:
        _game().reset()
        return redirect(url_for("index"))

    return app


def main() -> None:
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    create_app().run(host=host, port=port, debug=os.environ.get("FLASK_DEBUG") == "1")


if __name__ == "__main__":
    main()
