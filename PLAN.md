# Tic Tac Toe (Python + Tkinter) — Development Plan

## Context
Build a tic-tac-toe game from scratch in `/Users/davidkolet-tassara/Desktop/tic_tac_toe` (currently empty). The game uses a Tkinter GUI, supports three modes (two-player local, human vs computer, computer vs computer), ships with an unbeatable minimax AI, and includes unit tests using the standard-library `unittest`.

The architecture separates **pure game logic** (board state, win/draw detection, move validation, AI) from the **UI layer** (Tkinter). This keeps the logic testable without spinning up a window and makes it easy to swap or extend the front-end later.

## File layout

```
tic_tac_toe/
├── main.py          # Entry point — launches the Tkinter GUI
├── game.py          # Board class: state, moves, win/draw detection (no UI)
├── ai.py            # Minimax AI (no UI, no Board mutation)
├── gui.py           # Tkinter window, mode selection, board rendering
└── tests/
    ├── __init__.py
    ├── test_game.py # Tests for Board: moves, wins, draws, validation
    └── test_ai.py   # Tests for AI: blocks wins, takes wins, never loses
```

## Module designs

### `game.py` — `Board`
- 3×3 grid stored as a flat list of 9 cells, each `'X'`, `'O'`, or `' '`.
- `current_player` attribute, starts as `'X'`.
- `make_move(index)` — places the current player's mark at `index`, switches turn. Raises on invalid moves (occupied or out of range).
- `available_moves()` → list of empty indices.
- `winner()` → `'X'`, `'O'`, or `None`. Checks 8 lines (3 rows, 3 cols, 2 diagonals).
- `is_draw()` → `True` if no winner and no empty cells.
- `is_game_over()` → convenience: winner exists or draw.
- `reset()` — clears board, resets `current_player` to `'X'`.
- `copy()` — returns a deep copy (used by AI for lookahead without mutating real state).

### `ai.py` — minimax
- `best_move(board, player)` → index of optimal move for `player`.
- `minimax(board, player, maximizing_player)` → score (+1 win for maximizing player, -1 loss, 0 draw). Recurses over `available_moves()` on a copy of the board.
- For 3×3 the search tree is tiny (<9!), so no need for alpha-beta pruning or memoization — keep it simple.

### `gui.py` — Tkinter UI
- A startup screen (or top control bar) lets the user pick mode: **Human vs Human**, **Human vs Computer**, **Computer vs Computer**, plus which side X/O the human plays in HvC.
- 3×3 grid of `tk.Button` widgets, one per cell. Clicking a cell calls `Board.make_move()` then re-renders.
- Status label below the grid: "X's turn", "O wins!", "Draw", etc.
- "New Game" button to reset.
- For computer turns: schedule the AI move via `root.after(300, ...)` so the UI updates between moves and the human can see what's happening.
- In Computer vs Computer, both turns are scheduled with `after()` so the game animates rather than resolving instantly.

### `main.py`
- Just instantiates the Tk root and the GUI app, then calls `mainloop()`.

## Tests (`unittest`)

### `test_game.py`
- New board is empty, X goes first.
- `make_move` places mark and toggles turn.
- `make_move` on occupied / out-of-range cell raises.
- `winner()` detects each row, each column, both diagonals.
- `is_draw()` returns True for a full board with no winner, False otherwise.
- `copy()` is independent — mutating the copy doesn't affect the original.

### `test_ai.py`
- AI takes an immediate winning move when one exists.
- AI blocks the opponent's immediate winning move.
- AI vs AI from an empty board always ends in a draw (sanity check that minimax is correct).
- AI never loses across a sweep of every legal opening move played by the opponent.

## Verification
1. `cd /Users/davidkolet-tassara/Desktop/tic_tac_toe`
2. Run tests: `python -m unittest discover tests` — all pass.
3. Launch the game: `python main.py`.
4. Manual smoke checks in the GUI:
   - Two-player mode: play a row-win, a column-win, a diagonal-win, and a draw.
   - Human vs Computer: try to beat the AI — should be impossible; best case is a draw.
   - Computer vs Computer: every game ends in a draw.
   - "New Game" resets the board and status label.

## Dependencies
- Python 3.x with `tkinter` (ships with the standard CPython installer on macOS).
- No third-party packages.

## Out of scope
- Score tracking across multiple games.
- Variable board sizes (NxN).
- Network play.
- Persisting games to disk.

---

## Version History

### v1 — Initial implementation
Core game with Tkinter GUI, minimax AI, three game modes (Human vs Human, Human vs Computer, Computer vs Computer), and 16 unit tests covering board logic and AI behavior.
(See original plan above.)

### v2 — Persistent statistics
**Added:** Per-player win/draw tracking that persists across app restarts. Stats are displayed in the GUI at all times and can be reset by the user.

New files:
- `stats.py` — `StatsTracker` class: JSON persistence with atomic writes (write-then-rename), silent fallback to zeros on missing/corrupt file, `record()` / `reset()` / `load()` / `save()` API.
- `tests/test_stats.py` — 10 unit tests for `StatsTracker` (using `tempfile`, no real `stats.json` touched).
- `stats.json` — auto-created at runtime in the project directory; git-ignored.

Changed files:
- `gui.py` — stats bar (row 2) added between the board and status label; Reset Stats button; `_result_recorded` guard prevents double-counting when `_refresh()` is called multiple times on a finished board; status label shifted to row 3.
- `.gitignore` — excludes `stats.json` so user data is not committed.
