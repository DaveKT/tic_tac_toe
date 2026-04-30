# Tic Tac Toe

A small Python tic-tac-toe game with a Tkinter GUI, three game modes, an unbeatable minimax AI, and persistent per-player statistics.

## Features

- **Three modes:** Human vs Human, Human vs Computer, Computer vs Computer
- **Unbeatable AI** using the classic minimax algorithm — the best you can do is draw
- **Pick your side** (X or O) when playing against the computer
- **Persistent statistics** — X wins, O wins, and draws are tracked across sessions and saved to `stats.json`; click **Reset Stats** to clear them
- **Pure-logic core** separated from the UI, so it's easy to test and extend
- **Zero third-party dependencies** — just Python's standard library

## Project layout

```
tic_tac_toe/
├── main.py          # Entry point — launches the Tkinter GUI
├── game.py          # Board: state, moves, win/draw detection
├── ai.py            # Minimax AI
├── gui.py           # Tkinter window, mode selection, board rendering
├── stats.py         # StatsTracker: persistent JSON statistics
├── stats.json       # Auto-created at runtime; git-ignored
├── tests/
│   ├── test_game.py # Board logic tests
│   ├── test_ai.py   # AI behavior tests
│   └── test_stats.py # StatsTracker tests
├── PLAN.md          # Development plan (versioned)
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

26 unit tests cover board logic, AI behavior (including a sweep proving the
AI never loses against any legal opening), and statistics persistence. Tests don't need Tk:

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
5. Running totals for X wins, O wins, and draws are shown below the board and persist between sessions. Click **Reset Stats** to clear them.

## Architecture notes

- `Board` is a plain class with no UI dependencies, making it trivial to test
  and reuse. The GUI is a thin layer that calls into it.
- `ai.minimax` recurses on copies of the board (`Board.copy()`), so it never
  mutates real game state.
- The 3×3 search tree is small enough that no alpha-beta pruning or
  memoization is needed — the implementation is intentionally simple.
- Computer moves are scheduled with `root.after()` so the UI repaints between
  turns and Computer-vs-Computer games animate rather than resolving instantly.
- `StatsTracker` writes `stats.json` atomically (write to a `.tmp` file, then
  rename) so a crash mid-save cannot corrupt the persisted data.

## Version history

| Version | What changed |
|---------|-------------|
| v1 | Initial release: Tkinter GUI, minimax AI, three game modes, 16 unit tests |
| v2 | Persistent statistics: X wins / O wins / draws saved to `stats.json`, Reset Stats button, 10 new unit tests |
