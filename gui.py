import tkinter as tk
from tkinter import ttk

from game import Board
from ai import best_move
from stats import StatsTracker

MODE_HVH = "Human vs Human"
MODE_HVC = "Human vs Computer"
MODE_CVC = "Computer vs Computer"
MODES = (MODE_HVH, MODE_HVC, MODE_CVC)

AI_DELAY_MS = 350


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        self.board = Board()
        self.mode_var = tk.StringVar(value=MODE_HVH)
        self.human_side_var = tk.StringVar(value="X")
        self.difficulty_var = tk.StringVar(value="Hard")
        self.status_var = tk.StringVar(value="X's turn")
        self._pending_after = None
        self._stats = StatsTracker()
        self._stats.load()
        self._result_recorded = False

        self._build_controls()
        self._build_board()
        self._build_stats()
        self._build_status()
        self._refresh()

    def _build_controls(self):
        controls = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        controls.grid(row=0, column=0, sticky="ew")

        ttk.Label(controls, text="Mode:").grid(row=0, column=0, sticky="w")
        mode_menu = ttk.OptionMenu(
            controls, self.mode_var, MODE_HVH, *MODES, command=lambda _=None: self._on_mode_change()
        )
        mode_menu.grid(row=0, column=1, padx=(4, 12), sticky="w")

        ttk.Label(controls, text="Human plays:").grid(row=0, column=2, sticky="w")
        self.side_menu = ttk.OptionMenu(
            controls, self.human_side_var, "X", "X", "O", command=lambda _=None: self._new_game()
        )
        self.side_menu.grid(row=0, column=3, padx=(4, 12), sticky="w")

        ttk.Label(controls, text="Difficulty:").grid(row=0, column=4, sticky="w")
        self.difficulty_menu = ttk.OptionMenu(
            controls, self.difficulty_var, "Hard", "Easy", "Hard",
            command=lambda _=None: self._new_game()
        )
        self.difficulty_menu.grid(row=0, column=5, padx=(4, 12), sticky="w")
        self.difficulty_menu.configure(state="disabled")

        ttk.Button(controls, text="New Game", command=self._new_game).grid(row=0, column=6, sticky="e")

    def _build_board(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=1, column=0)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                frame,
                text=" ",
                width=4,
                height=2,
                font=("Helvetica", 28, "bold"),
                command=lambda idx=i: self._on_cell_click(idx),
            )
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)

    def _build_stats(self):
        frame = ttk.Frame(self.root, padding=(10, 0))
        frame.grid(row=2, column=0, sticky="ew")
        self._stats_var = tk.StringVar()
        ttk.Label(frame, textvariable=self._stats_var).pack(side="left")
        ttk.Button(frame, text="Reset Stats", command=self._reset_stats).pack(side="right")

    def _build_status(self):
        status = ttk.Label(self.root, textvariable=self.status_var, padding=(10, 0, 10, 10))
        status.grid(row=3, column=0, sticky="ew")

    def _on_mode_change(self):
        if self.mode_var.get() == MODE_HVC:
            self.side_menu.configure(state="normal")
            self.difficulty_menu.configure(state="normal")
        else:
            self.side_menu.configure(state="disabled")
            self.difficulty_menu.configure(state="disabled")
        self._new_game()

    def _reset_stats(self):
        self._result_recorded = False
        self._stats.reset()
        self._refresh_stats()

    def _new_game(self):
        self._result_recorded = False
        if self._pending_after is not None:
            self.root.after_cancel(self._pending_after)
            self._pending_after = None
        self.board.reset()
        self._refresh()
        self._maybe_schedule_ai()

    def _on_cell_click(self, index):
        if self.board.is_game_over():
            return
        if self._is_ai_turn():
            return
        if self.board.cells[index] != " ":
            return
        self.board.make_move(index)
        self._refresh()
        self._maybe_schedule_ai()

    def _is_ai_turn(self):
        mode = self.mode_var.get()
        if mode == MODE_HVH:
            return False
        if mode == MODE_CVC:
            return True
        return self.board.current_player != self.human_side_var.get()

    def _maybe_schedule_ai(self):
        if self.board.is_game_over():
            return
        if self._is_ai_turn():
            self._pending_after = self.root.after(AI_DELAY_MS, self._play_ai_turn)

    def _play_ai_turn(self):
        self._pending_after = None
        if self.board.is_game_over():
            return
        if not self._is_ai_turn():
            return
        difficulty = (
            self.difficulty_var.get().lower()
            if self.mode_var.get() == MODE_HVC
            else "hard"
        )
        move = best_move(self.board, self.board.current_player, difficulty)
        self.board.make_move(move)
        self._refresh()
        self._maybe_schedule_ai()

    def _refresh_stats(self):
        s = self._stats
        self._stats_var.set(f"X wins: {s.x_wins}   O wins: {s.o_wins}   Draws: {s.draws}")

    def _refresh(self):
        for i, btn in enumerate(self.buttons):
            btn.configure(text=self.board.cells[i])
        winner = self.board.winner()
        if winner is not None:
            self.status_var.set(f"{winner} wins!")
        elif self.board.is_draw():
            self.status_var.set("Draw")
        else:
            self.status_var.set(f"{self.board.current_player}'s turn")
        if self.board.is_game_over() and not self._result_recorded:
            self._stats.record(winner if winner else "draw")
            self._result_recorded = True
        self._refresh_stats()
