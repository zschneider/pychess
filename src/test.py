"""Chess engine/AI testing framework using python unittests."""
# stdlib
import unittest

# local
from engine import Color, Board, Player, Pawn, Knight, Rook, Bishop, Knight, Queen, King, xy_to_num, fails_bounds_check

# ------------ Utility Functions ------------


def create_board_and_players():
    """One line function used to create an empty board and players."""
    return Board(), Player(Color.W), Player(Color.B)

# ------------ Test Suites ------------


class TestEngineUtilityMethods(unittest.TestCase):
    """Tests additional utility functions."""

    def test_xy_conv(self):
        """Tests for conversion from xy arrray positions to board indices."""
        pos1 = [0, 0]  # a8
        pos2 = [7, 7]  # h1
        pos3 = [4, 5]  # e3
        pos_inv1 = [64, 0]
        pos_inv2 = [0, 9]

        self.assertEqual(xy_to_num(pos1), 0)
        self.assertEqual(xy_to_num(pos2), 63)
        self.assertEqual(xy_to_num(pos3), 44)
        self.assertFalse(xy_to_num(pos_inv1))
        self.assertFalse(xy_to_num(pos_inv2))

    def test_bounds_check(self):
        """Tests the bounds_check method correctly returns False on incorrect
        positions and True on correct positions."""
        pos1 = [0, 0]  # a8
        pos2 = [7, 7]  # h1
        pos3 = [4, 5]  # e3
        pos_inv1 = [64, 0]
        pos_inv2 = [-3, 5]
        pos_inv3 = [0, 9]

        # fails_bounds_check tests
        self.assertFalse(fails_bounds_check(pos1))
        self.assertFalse(fails_bounds_check(pos2))
        self.assertFalse(fails_bounds_check(pos3))
        self.assertTrue(fails_bounds_check(pos_inv1))
        self.assertTrue(fails_bounds_check(pos_inv2))
        self.assertTrue(fails_bounds_check(pos_inv3))


class TestBoardMethods(unittest.TestCase):
    """Test suite for Board class."""

    def test_add_to_board(self):
        """Add a piece, verify the square is taken and that the board's
        pieces list has the piece in it."""
        board, white = Board(), Player(Color.W)
        pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pos_white)

        board.add_to_board(pawn_white)

        # fetch the piece using xy_conversion
        self.assertTrue(board.board[xy_to_num(pos_white)] is pawn_white)

        # assure that the piece is in the board's pieces list.
        self.assertTrue(pawn_white in board.pieces)

    def test_check_if_empty(self):
        """Make sure check_if_empty returns True at first,
        and then False when we add a piece."""
        board, white = Board(), Player(Color.W)
        pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pos_white)

        self.assertTrue(board.check_if_empty(pos_white))
        board.add_to_board(pawn_white)
        self.assertFalse(board.check_if_empty(pos_white))

    def test_get_piece_at_position(self):
        """Fetch a piece we add to the board, fetch an empty square
        and make sure we get None."""
        board, white = Board(), Player(Color.W)
        pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pos_white)
        board.add_to_board(pawn_white)
        self.assertTrue(board.get_piece_at_position(pos_white) is pawn_white)
        self.assertTrue(board.get_piece_at_position([1, 1]) is None)

    def test_check_if_opponent(self):
        """Add one piece from each player to the board, verify booleans
        are correct."""
        board, white, black = create_board_and_players()
        pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pos_white)

        pos_black = [4, 1]
        pawn_black = Pawn(black, pos_black)

        board.add_to_board(pawn_white)
        board.add_to_board(pawn_black)

        self.assertFalse(board.check_if_opponent(pos_white, white))
        self.assertFalse(board.check_if_opponent(pos_black, black))
        self.assertTrue(board.check_if_opponent(pos_black, white))
        self.assertTrue(board.check_if_opponent(pos_white, black))

    def test_remove_a_piece(self):
        """Add a piece, then remove it, and verify space is empty"""
        board, white = Board(), Player(Color.W)
        pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pos_white)
        board.add_to_board(pawn_white)

        # emptySpace
        self.assertFalse(board.check_if_empty(pos_white))
        board.remove_from_board(pos_white)
        self.assertTrue(board.check_if_empty(pos_white))

    def test_determine_check(self):
        """Creates two check situations and verifies that is_in_check returns
        True in both situations."""
        # Check 1:
        board, white, black = create_board_and_players()

        pos_rook_black = [4, 0]  # e8
        rook_black = Rook(black, pos_rook_black)

        pos_king_white = [4, 7]  # e1
        king_white = King(white, pos_king_white)

        board.add_to_board(rook_black)
        board.add_to_board(king_white)

        self.assertTrue(board.is_in_check(white))

        # Add a separation pawn, should no longer be in check

        pos_pawn_black = [4, 3]  # e5
        pawn_black = Pawn(black, pos_pawn_black)
        board.add_to_board(pawn_black)
        self.assertFalse(board.is_in_check(white))

        # Check 2:
        board, white, black = create_board_and_players()

        pos_bishop_black = [1, 0]  # b8
        bishop_black = Bishop(black, pos_bishop_black)

        pos_king_white = [5, 4]  # f4
        king_white = King(white, pos_king_white)

        board.add_to_board(bishop_black)
        board.add_to_board(king_white)

        self.assertTrue(board.is_in_check(white))

        # Add a separation pawn, should no longer be in check

        pos_pawn_black = [3, 2]  # d6
        pawn_black = Pawn(black, pos_pawn_black)
        board.add_to_board(pawn_black)
        self.assertFalse(board.is_in_check(white))

    def test_is_attacked(self):
        """Assure that all positions attacked by an enemy piece return True."""
        board, white, black = create_board_and_players()
        pos_white = [4, 6]  # e2
        rook_white = Rook(white, pos_white)

        board.add_to_board(rook_white)
        self.assertTrue(board.is_attacked([3, 6], black))
        self.assertTrue(board.is_attacked([4, 7], black))
        self.assertFalse(board.is_attacked([5, 5], black))
        self.assertFalse(board.is_attacked([4, 7], white))

    def test_get_all_legal_moves_simple(self):
        """Simply verify that getting the legal moves of two pieces
        sum to the returned value of get_all_legal_moves."""
        board, white = Board(), Player(Color.W)
        pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pos_white)
        board.add_to_board(pawn_white)

        pos_white2 = [3, 3]  # d5
        rook_white = Rook(white, pos_white2)
        board.add_to_board(rook_white)

        combined_positions = {}
        combined_positions[pawn_white] = pawn_white.get_legal_moves(board, True)
        combined_positions[rook_white] = rook_white.get_legal_moves(board, True)

        self.assertEqual(board.get_all_legal_moves(white), combined_positions)

    def test_get_all_legal_moves_check(self):
        """Assures that get_all_legal_moves won't return a move that puts
        the owner in check."""
        board, white, black = create_board_and_players()
        pawn_pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pawn_pos_white)
        board.add_to_board(pawn_white)

        king_pos_white = [5, 6]
        king_white = King(white, king_pos_white)
        board.add_to_board(king_white)
        self.assertFalse(board.get_all_legal_moves(white)[pawn_white] == [])

        rook_pos_black = [1, 6]
        rook_black = Rook(black, rook_pos_black)
        board.add_to_board(rook_black)

        self.assertTrue(board.get_all_legal_moves(white)[pawn_white] == [])

    def test_get_all_legal_moves_cm(self):
        """Assures that get_all_legal_moves returns no moves if the player
        is in checkmate."""
        board, white, black = create_board_and_players()
        pawn_pos_white = [4, 6]  # e2
        pawn_white = Pawn(white, pawn_pos_white)
        board.add_to_board(pawn_white)

        king_pos_white = [7, 6]
        king_white = King(white, king_pos_white)
        board.add_to_board(king_white)

        rook_pos_black1 = [7, 0]
        rook_black1 = Rook(black, rook_pos_black1)
        board.add_to_board(rook_black1)

        rook_pos_black2 = [6, 0]
        rook_black2 = Rook(black, rook_pos_black2)
        board.add_to_board(rook_black2)

        for moves in board.get_all_legal_moves(white).values():
            self.assertTrue(moves == [])

    def test_board_with_passed_in_board(self):
        """Tests the creation of a board using a previous
        board's array. Each peice should have a copy created."""
        board, white = Board(), Player(Color.W)
        pawn_white = Pawn(white, [3, 2])  # d6
        board.add_to_board(pawn_white)

        new_board = Board(board.board)
        self.assertEqual(len(new_board.pieces), 1)
        self.assertFalse(new_board.check_if_empty([3, 2]))
        self.assertFalse(new_board.get_piece_at_position([3, 2]) is
                         pawn_white)

    def test_make_move_simple(self):
        """Makes a simple move, verifies values are appropriately updated."""
        board, white = Board(), Player(Color.W)
        rook_white = Rook(white, [3, 2])  # d6
        board.add_to_board(rook_white)

        board.make_move(rook_white, [5, 2])  # f6
        # ensure make_move updated piece position
        self.assertTrue(rook_white.position == [5, 2])
        # ensure make_move updated board position
        self.assertTrue(board.get_piece_at_position([5, 2]) is rook_white)
        self.assertTrue(board.get_piece_at_position([3, 2]) is None)

    def test_make_move_pawn_simple(self):
        """Makes a simple pawn move, verifies values are appropriately
         updated."""
        board, white = Board(), Player(Color.W)
        pawn_white = Pawn(white, [3, 6])  # d2
        board.add_to_board(pawn_white)

        board.make_move(pawn_white, [3, 4])  # d4
        # ensure make_move updated piece position
        self.assertTrue(pawn_white.position == [3, 4])
        # ensure make_move updated board position
        self.assertTrue(board.get_piece_at_position([3, 4]) is pawn_white)
        self.assertTrue(board.get_piece_at_position([3, 6]) is None)

    def test_make_move_pawn_promotion(self):
        """Verifies that making promition moves work appropriately."""
        board, white = Board(), Player(Color.W)
        pawn_white = Pawn(white, [3, 1])  # d7
        board.add_to_board(pawn_white)

        board.make_move(pawn_white, [3, 'Q'])  # promotion at d8 square
        # ensure the new piece is a queen.
        self.assertTrue(isinstance(board.get_piece_at_position([3, 0]), Queen))

    def test_make_move_pawn_en_passant(self):
        """Verifies that taking a pawn en passant removes enemy pawn."""
        board, white, black = create_board_and_players()
        pawn_pos_white = [5, 3]  # f5
        pawn_white = Pawn(white, pawn_pos_white)
        board.add_to_board(pawn_white)

        pawn_pos_black = [4, 3]  # e5
        pawn_black = Pawn(black, pawn_pos_black)
        board.add_to_board(pawn_black)
        # simulate having made its first move.
        board.en_passant = pawn_black

        board.make_move(pawn_white, [4, 2])  # e6
        self.assertTrue(board.get_piece_at_position([4, 2]) is pawn_white)
        self.assertTrue(board.get_piece_at_position([4, 3]) is None)

    def test_make_move_pawn_double_jump(self):
        """Verifies that making a double jump opens up the piece for
         en passant."""
        board, white = Board(), Player(Color.W)
        pawn_pos_white = [5, 6]  # f2
        pawn_white = Pawn(white, pawn_pos_white)
        board.add_to_board(pawn_white)

        board.make_move(pawn_white, [5, 4])
        self.assertTrue(board.en_passant is pawn_white)

    """
    # rules of castling:
    # 1. king cant be in check
    # 2. king cannot travel through or land in attacked square
    # 3. neither the king or castling rook can have moved
    # 4. there must not be any pieces in between the king and rook
    """

    def test_make_move_castle_kingside(self):
        """Ensures kingside castling moving works correctly."""
        board, white = Board(), Player(Color.W)
        king_pos_white = [4, 7]  # e1
        rook_pos_white = [7, 7]  # h1
        king_white = King(white, king_pos_white)
        rook_white = Rook(white, rook_pos_white)
        board.add_to_board(king_white)
        board.add_to_board(rook_white)

        board.make_move(king_white, [6, 7])  # castle to g1
        self.assertTrue(board.get_piece_at_position([6, 7]) is king_white)
        self.assertTrue(board.get_piece_at_position([5, 7]) is rook_white)
        self.assertTrue(board.get_piece_at_position([4, 7]) is None)
        self.assertTrue(board.get_piece_at_position([7, 7]) is None)

    def test_make_move_castle_queenside(self):
        """Ensures queenside castling moving works correctly."""
        board, white = Board(), Player(Color.W)
        king_pos_white = [4, 7]  # e1
        rook_pos_white = [0, 7]  # a1
        king_white = King(white, king_pos_white)
        rook_white = Rook(white, rook_pos_white)
        board.add_to_board(king_white)
        board.add_to_board(rook_white)

        board.make_move(king_white, [2, 7])  # castle to c1
        self.assertTrue(board.get_piece_at_position([2, 7]) is king_white)
        self.assertTrue(board.get_piece_at_position([3, 7]) is rook_white)
        self.assertTrue(board.get_piece_at_position([4, 7]) is None)
        self.assertTrue(board.get_piece_at_position([0, 7]) is None)
        self.assertTrue(board.get_piece_at_position([1, 7]) is None)


class TestPieceMethods(unittest.TestCase):
    """Test suite for Piece class."""

    def test_filter_checks(self):
        """Assure that all moves that lead to check for the player are
        appropriately filtered out of the move list."""
        board, white, black = create_board_and_players()
        pawn_pos_white = [5, 3]  # f5
        pawn_white = Pawn(white, pawn_pos_white)
        pawn_white.first_move = False
        board.add_to_board(pawn_white)

        king_pos_white = [7, 3]  # h5
        king_white = King(white, king_pos_white)
        board.add_to_board(king_white)

        pawn_moves = pawn_white.get_legal_moves(board, False)
        filtered_pawn_moves = pawn_white.filter_checks(pawn_moves, board)
        self.assertEqual(pawn_moves, filtered_pawn_moves)

        rook_pos_black = [1, 3]  # a1
        rook_black = Rook(black, rook_pos_black)
        board.add_to_board(rook_black)

        pawn_moves = pawn_white.get_legal_moves(board, False)
        filtered_pawn_moves = pawn_white.filter_checks(pawn_moves, board)
        self.assertEqual(len(filtered_pawn_moves), 0)


class TestPawnMethods(unittest.TestCase):
    """Test suite for Pawn class."""

    def test_pawn_white_simple(self):
        pass

    def test_pawn_white_path_impeded(self):
        pass

    def test_pawn_white_first_move(self):
        pass

    def test_pawn_white_promotion(self):
        pass

    def test_pawn_white_capture(self):
        pass

    def test_pawn_white_en_passant(self):
        pass

    def test_pawn_black_capture_promo(self):
        pass

    def test_pawn_black_simple(self):
        pass

    def test_pawn_black_path_impeded(self):
        pass

    def test_pawn_black_first_move(self):
        pass

    def test_pawn_black_promotion(self):
        pass

    def test_pawn_black_capture(self):
        pass

    def test_pawn_black_en_passant(self):
        pass

    def test_pawn_black_capture_promo(self):
        pass

class TestRookMethods(unittest.TestCase):
    """Test suite for rook class."""

    def test_simple(self):
        pass

    def test_capture(self):
        pass

    def test_path_impeded(self):
        pass


class TestBishopMethods(unittest.TestCase):
    """Test suite for bishop class."""

    def test_simple(self):
        pass

    def test_capture(self):
        pass

    def test_path_impeded(self):
        pass


class TestKnightMethods(unittest.TestCase):
    """Test suite for knight class."""

    def test_simple(self):
        pass

    def test_capture(self):
        pass

    def test_path_impeded(self):
        pass


class TestQueenMethods(unittest.TestCase):
    """Test suite for queen class."""

    def test_simple(self):
        pass

    def test_capture(self):
        pass

    def test_path_impeded(self):
        pass


class TestKingMethods(unittest.TestCase):
    """Test suite for king class."""

    def test_simple(self):
        pass

    def test_capture(self):
        pass

    def test_path_impeded(self):
        pass

    def test_castling(self):
        pass







if __name__ == '__main__':
    unittest.main()
