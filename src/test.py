"""Chess engine/AI testing framework using python unittests."""
# stdlib
import unittest

# local
from engine import Color, Board, Player, Pawn, Knight, Bishop, Knight, Queen, King


class TestBoardMethods(unittest.TestCase):
    """Test suite for Board class."""

    def test_xy_conversions_and_bounds_checking(self):
        """Tests for xy_to_num and fails_bounds_check"""
        board = Board()
        pos1 = [0, 0]  # a1
        pos2 = [7, 7]  # g8
        pos3 = [4, 5]  # e6
        pos_inv1 = [64, 0]
        pos_inv2 = [-3, 5]
        pos_inv3 = [0, 9]
        # xy_to_num tests (we dont test inv2 since 
        # it will return a valid square)
        self.assertEqual(board.xy_to_num(pos1), 0)
        self.assertEqual(board.xy_to_num(pos2), 63)
        self.assertEqual(board.xy_to_num(pos3), 44)
        self.assertFalse(board.xy_to_num(pos_inv1))
        self.assertFalse(board.xy_to_num(pos_inv3))
        # fails_bounds_check tests
        self.assertFalse(board.fails_bounds_check(pos1))
        self.assertFalse(board.fails_bounds_check(pos2))
        self.assertFalse(board.fails_bounds_check(pos3))
        self.assertTrue(board.fails_bounds_check(pos_inv1))
        self.assertTrue(board.fails_bounds_check(pos_inv2))
        self.assertTrue(board.fails_bounds_check(pos_inv3))

    def test_add_a_piece(self):
        board = Board()
        white = Player(Color.W)
        pos = [4, 5]  # e6
        pawn = Pawn(white, pos)
        board.add_to_board(pawn)
        self.assertFalse(board.check_if_empty(pos))
        self.assertTrue(isinstance(board.get_piece_at_position(pos), Pawn))
        self.assertFalse(board.check_if_opponent(pos, white))




if __name__ == '__main__':
    unittest.main()