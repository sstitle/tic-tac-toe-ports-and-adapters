# tictactoe-web

Flask server that serves a single page of `<button>` cells. Each browser gets its own `GameSession` from `core` (keyed by a signed session id).

From the repo root (after `uv sync --extra web`):

```bash
uv run tictactoe-web
```

Open `http://127.0.0.1:5000` (override with `FLASK_HOST` / `FLASK_PORT`). Set `FLASK_SECRET_KEY` for anything beyond local demo use.
