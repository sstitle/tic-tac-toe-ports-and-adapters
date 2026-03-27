# Maskfile

This is a [mask](https://github.com/jacobdeichert/mask) task runner file.

## cli

> Run the Typer terminal CLI

**OPTIONS**
* vs_computer
    * flags: -c, --vs-computer
    * type: bool
    * desc: Play against the minimax AI (you are X)

```bash
uv run --directory python/cli-typer tictactoe ${vs_computer:+--vs-computer}
```

## tui

> Run the Textual TUI

**OPTIONS**
* vs_computer
    * flags: -c, --vs-computer
    * type: bool
    * desc: Play against the minimax AI (you are X)

```bash
uv run --directory python/tui-textual tictactoe-tui ${vs_computer:+--vs-computer}
```

## qt

> Run the Qt GUI

**OPTIONS**
* vs_computer
    * flags: -c, --vs-computer
    * type: bool
    * desc: Play against the minimax AI (you are X)

```bash
uv run --directory python/gui-qt tictactoe-qt ${vs_computer:+--vs-computer}
```

## web

> Run the Flask web server

```bash
uv run --directory python/web tictactoe-web
```
