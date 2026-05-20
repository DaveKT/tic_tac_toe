# Project Timeline

## 2026-04-29 — v1: Initial Release
**Commit:** `1496aac` — Initial commit: Tic Tac Toe (Tkinter + minimax)
**Commit:** `065d8a5` — Add README

- Built Tkinter GUI with a 3x3 board rendered as button widgets
- Implemented three game modes: Human vs Human, Human vs Computer, Computer vs Computer
- Implemented unbeatable minimax AI (`ai.py`)
- Pure-logic `Board` class (`game.py`) separated from the UI layer
- Computer moves scheduled with `root.after()` so the UI animates between turns
- Entry point in `main.py`
- 16 unit tests covering board logic and AI behavior (`test_game.py`, `test_ai.py`)
- Zero third-party dependencies

---

## 2026-04-30 — v2: Persistent Statistics
**Commit:** `d3dab27` — Added score keeping

- Added `stats.py` with a `StatsTracker` class that tracks X wins, O wins, and draws
- Stats saved to `stats.json` using atomic writes (write-then-rename) to prevent corruption
- Stats displayed in the GUI at all times; survive app restarts
- Added **Reset Stats** button to clear persisted data
- Added `.gitignore` entry to exclude `stats.json` from version control
- Added `tests/test_stats.py` with 10 new unit tests for `StatsTracker`

---

## 2026-05-20 — v3: Difficulty Levels (Beatable Computer)
**Commit:** `58bcc63` — Added new levels feature
**Commit:** `7ca4822` — Updated the readme for difficulty levels.

- Added **Easy** difficulty: depth-limited minimax (`max_depth=2`) that takes immediate wins and blocks immediate losses, but misses forks and multi-move combinations — beatable with good play
- **Hard** difficulty retains the original unbeatable minimax
- Difficulty dropdown added to the control bar, enabled only in Human vs Computer mode
- Computer vs Computer always plays at full strength regardless of difficulty setting
- `ai.py`: `minimax()` gains optional `max_depth` parameter; `best_move()` gains a `difficulty` parameter
- Added 5 new unit tests to `test_ai.py` (easy takes wins, easy blocks losses, easy is beatable, hard is never beaten)
- README updated with difficulty level documentation

---

## 2026-05-20 — Documentation & Planning Updates
**Commit:** `aac96fc` — Added feature ideas for training sessions with developers.
**Commit:** `0a8fca4` — Updated feature ideas with completed feature.

- Added `FEATURE_IDEAS.md` with planned improvements:
  - Sync stats to play mode (reset stats on mode change)
  - Add classic hash-grid lines to the UI
  - ~~Beatable computer option~~ (completed in v3, struck through)
