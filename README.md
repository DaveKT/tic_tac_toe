# Tic Tac Toe

A small Python tic-tac-toe game with a Tkinter GUI, three game modes, and an unbeatable minimax AI.

## Features

- **Three modes:** Human vs Human, Human vs Computer, Computer vs Computer
- **Unbeatable AI** using the classic minimax algorithm — the best you can do is draw
- **Pick your side** (X or O) when playing against the computer
- **Pure-logic core** separated from the UI, so it's easy to test and extend
- **Zero third-party dependencies** — just Python's standard library

## Project layout

```
tic_tac_toe/
├── main.py          # Entry point — launches the Tkinter GUI
├── game.py          # Board: state, moves, win/draw detection
├── ai.py            # Minimax AI
├── gui.py           # Tkinter window, mode selection, board rendering
├── tests/
│   ├── test_game.py # Board logic tests
│   └── test_ai.py   # AI behavior tests
├── PLAN.md          # Original development plan
└── README.md
```

## Running the game

The game uses `tkinter`, which ships with the standard CPython installer. The
easiest way to launch it is with [`uv`](https://github.com/astral-sh/uv), which
will fetch a managed Python build automatically:

```bash
uv run --python 3.13 main.py
```

Or, if you have a Python 3 install on your system that includes Tk (e.g. macOS
system Python at `/usr/bin/python3`, or python.org installers):

```bash
python3 main.py
```

> **Note:** Homebrew's default `python@3.14` is built without `_tkinter`. If
> `import tkinter` fails, either use `uv` as shown above, install the
> `python-tk` companion formula, or use a different Python.

## Running the tests

16 unit tests cover board logic and AI behavior (including a sweep proving the
AI never loses against any legal opening). Tests don't need Tk:

```bash
uv run --python 3.13 -m unittest discover tests -v
# or
python3 -m unittest discover tests -v
```

## How to play

1. Launch the game.
2. Pick a mode from the dropdown:
   - **Human vs Human** — hot-seat play on the same machine
   - **Human vs Computer** — choose whether you play X or O
   - **Computer vs Computer** — watch two perfect players draw forever
3. Click any empty cell to place your mark.
4. Hit **New Game** to reset.

## Architecture notes

- `Board` is a plain class with no UI dependencies, making it trivial to test
  and reuse. The GUI is a thin layer that calls into it.
- `ai.minimax` recurses on copies of the board (`Board.copy()`), so it never
  mutates real game state.
- The 3×3 search tree is small enough that no alpha-beta pruning or
  memoization is needed — the implementation is intentionally simple.
- Computer moves are scheduled with `root.after()` so the UI repaints between
  turns and Computer-vs-Computer games animate rather than resolving instantly.
