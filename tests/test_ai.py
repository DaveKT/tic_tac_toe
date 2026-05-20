import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game import Board, EMPTY
from ai import best_move


def play_full_game(first_mover, second_mover):
    """Play a full game where each side is a callable (board) -> move index."""
    board = Board()
    movers = {"X": first_mover, "O": second_mover}
    while not board.is_game_over():
        move = movers[board.current_player](board)
        board.make_move(move)
    return board


class TestAI(unittest.TestCase):
    def test_takes_immediate_win(self):
        board = Board()
        board.cells = ["X", "X", EMPTY,
                       "O", "O", EMPTY,
                       EMPTY, EMPTY, EMPTY]
        board.current_player = "X"
        self.assertEqual(best_move(board, "X"), 2)

    def test_blocks_opponent_win(self):
        board = Board()
        board.cells = ["X", "X", EMPTY,
                       EMPTY, "O", EMPTY,
                       EMPTY, EMPTY, EMPTY]
        board.current_player = "O"
        self.assertEqual(best_move(board, "O"), 2)

    def test_ai_vs_ai_is_always_a_draw(self):
        result = play_full_game(
            lambda b: best_move(b, "X"),
            lambda b: best_move(b, "O"),
        )
        self.assertTrue(result.is_draw())

    def test_ai_never_loses_against_every_opening(self):
        """For each possible first move by X, the perfect-play O must not lose."""
        for opening in range(9):
            board = Board()
            board.make_move(opening)

            def x_strategy(b, _opening=opening):
                # X plays optimally for the rest of the game.
                return best_move(b, "X")

            def o_strategy(b):
                return best_move(b, "O")

            movers = {"X": x_strategy, "O": o_strategy}
            while not board.is_game_over():
                move = movers[board.current_player](board)
                board.make_move(move)
            self.assertNotEqual(
                board.winner(), "X",
                f"AI O lost when X opened at cell {opening}",
            )

    def test_ai_never_loses_against_every_opening_as_x(self):
        """X with perfect play should never lose to any first response by O."""
        # X opens, then for each O response we let both sides play optimally.
        for x_open in range(9):
            for o_response in range(9):
                if o_response == x_open:
                    continue
                board = Board()
                board.make_move(x_open)
                board.make_move(o_response)
                while not board.is_game_over():
                    mover = "X" if board.current_player == "X" else "O"
                    board.make_move(best_move(board, mover))
                self.assertNotEqual(
                    board.winner(), "O",
                    f"AI X lost after opening {x_open}, O replied {o_response}",
                )


class TestAIDifficulty(unittest.TestCase):
    def test_easy_takes_immediate_win(self):
        board = Board()
        board.cells = ["X", "X", EMPTY,
                       "O", "O", EMPTY,
                       EMPTY, EMPTY, EMPTY]
        board.current_player = "X"
        self.assertEqual(best_move(board, "X", difficulty="easy"), 2)

    def test_easy_blocks_immediate_loss(self):
        board = Board()
        board.cells = ["X", "X", EMPTY,
                       EMPTY, "O", EMPTY,
                       EMPTY, EMPTY, EMPTY]
        board.current_player = "O"
        self.assertEqual(best_move(board, "O", difficulty="easy"), 2)

    def test_hard_difficulty_identical_to_default(self):
        positions = [
            (["X", EMPTY, EMPTY, EMPTY, "O", EMPTY, EMPTY, EMPTY, EMPTY], "X"),
            (["X", "O", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY], "X"),
            ([EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY], "X"),
        ]
        for cells, player in positions:
            board_default = Board()
            board_default.cells = list(cells)
            board_default.current_player = player
            board_hard = Board()
            board_hard.cells = list(cells)
            board_hard.current_player = player
            self.assertEqual(
                best_move(board_default, player),
                best_move(board_hard, player, difficulty="hard"),
            )

    def test_easy_difficulty_is_beatable(self):
        wins_by_x = 0
        for x_open in range(9):
            board = Board()
            board.make_move(x_open)
            while not board.is_game_over():
                if board.current_player == "X":
                    board.make_move(best_move(board, "X"))
                else:
                    board.make_move(best_move(board, "O", difficulty="easy"))
            if board.winner() == "X":
                wins_by_x += 1
        self.assertGreater(wins_by_x, 0, "Easy O should be beatable by optimal X")

    def test_hard_difficulty_never_loses(self):
        for x_open in range(9):
            board = Board()
            board.make_move(x_open)
            while not board.is_game_over():
                if board.current_player == "X":
                    board.make_move(best_move(board, "X"))
                else:
                    board.make_move(best_move(board, "O", difficulty="hard"))
            self.assertNotEqual(
                board.winner(), "X",
                f"Hard O should not lose when X opens at cell {x_open}",
            )


if __name__ == "__main__":
    unittest.main()
