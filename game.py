EMPTY = " "
PLAYERS = ("X", "O")

WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


class Board:
    def __init__(self):
        self.cells = [EMPTY] * 9
        self.current_player = "X"

    def make_move(self, index):
        if not 0 <= index < 9:
            raise ValueError(f"Cell index {index} is out of range (0-8).")
        if self.cells[index] != EMPTY:
            raise ValueError(f"Cell {index} is already taken.")
        self.cells[index] = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"

    def available_moves(self):
        return [i for i, cell in enumerate(self.cells) if cell == EMPTY]

    def winner(self):
        for a, b, c in WINNING_LINES:
            if self.cells[a] != EMPTY and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def is_draw(self):
        return self.winner() is None and EMPTY not in self.cells

    def is_game_over(self):
        return self.winner() is not None or EMPTY not in self.cells

    def reset(self):
        self.cells = [EMPTY] * 9
        self.current_player = "X"

    def copy(self):
        new_board = Board()
        new_board.cells = list(self.cells)
        new_board.current_player = self.current_player
        return new_board
