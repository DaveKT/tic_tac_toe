import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game import Board, EMPTY


class TestBoard(unittest.TestCase):
    def test_new_board_is_empty_and_x_starts(self):
        board = Board()
        self.assertEqual(board.cells, [EMPTY] * 9)
        self.assertEqual(board.current_player, "X")
        self.assertEqual(board.available_moves(), list(range(9)))
        self.assertIsNone(board.winner())
        self.assertFalse(board.is_draw())
        self.assertFalse(board.is_game_over())

    def test_make_move_places_mark_and_toggles_turn(self):
        board = Board()
        board.make_move(0)
        self.assertEqual(board.cells[0], "X")
        self.assertEqual(board.current_player, "O")
        board.make_move(4)
        self.assertEqual(board.cells[4], "O")
        self.assertEqual(board.current_player, "X")

    def test_make_move_on_occupied_cell_raises(self):
        board = Board()
        board.make_move(0)
        with self.assertRaises(ValueError):
            board.make_move(0)

    def test_make_move_out_of_range_raises(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.make_move(-1)
        with self.assertRaises(ValueError):
            board.make_move(9)

    def test_winner_detects_rows(self):
        for row in (0, 3, 6):
            board = Board()
            board.cells = [EMPTY] * 9
            for offset in range(3):
                board.cells[row + offset] = "X"
            self.assertEqual(board.winner(), "X")

    def test_winner_detects_columns(self):
        for col in (0, 1, 2):
            board = Board()
            for r in range(3):
                board.cells[col + r * 3] = "O"
            self.assertEqual(board.winner(), "O")

    def test_winner_detects_diagonals(self):
        b1 = Board()
        for i in (0, 4, 8):
            b1.cells[i] = "X"
        self.assertEqual(b1.winner(), "X")

        b2 = Board()
        for i in (2, 4, 6):
            b2.cells[i] = "O"
        self.assertEqual(b2.winner(), "O")

    def test_is_draw_only_when_full_and_no_winner(self):
        board = Board()
        board.cells = ["X", "O", "X",
                       "X", "O", "O",
                       "O", "X", "X"]
        self.assertIsNone(board.winner())
        self.assertTrue(board.is_draw())
        self.assertTrue(board.is_game_over())

    def test_is_draw_false_with_winner(self):
        board = Board()
        board.cells = ["X", "X", "X",
                       "O", "O", EMPTY,
                       EMPTY, EMPTY, EMPTY]
        self.assertEqual(board.winner(), "X")
        self.assertFalse(board.is_draw())
        self.assertTrue(board.is_game_over())

    def test_reset_clears_state(self):
        board = Board()
        board.make_move(0)
        board.make_move(1)
        board.reset()
        self.assertEqual(board.cells, [EMPTY] * 9)
        self.assertEqual(board.current_player, "X")

    def test_copy_is_independent(self):
        board = Board()
        board.make_move(4)
        clone = board.copy()
        clone.make_move(0)
        self.assertEqual(board.cells[0], EMPTY)
        self.assertEqual(board.current_player, "O")
        self.assertEqual(clone.cells[0], "O")
        self.assertEqual(clone.current_player, "X")


if __name__ == "__main__":
    unittest.main()
