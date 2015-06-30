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

        combined_positions = []
        for move in pawn_white.get_legal_moves(board, True):
            combined_positions += [pawn_white, move],
        for move in rook_white.get_legal_moves(board, True):
            combined_positions += [rook_white, move],

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

        found_a_move = False
        for move in board.get_all_legal_moves(white):
            if move[0] == pawn_white:
                found_a_move = True
        self.assertTrue(found_a_move)

        rook_pos_black = [1, 6]
        rook_black = Rook(black, rook_pos_black)
        board.add_to_board(rook_black)

        found_a_move = False
        for move in board.get_all_legal_moves(white):
            if move[0] == pawn_white:
                found_a_move = True
        self.assertFalse(found_a_move)

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

        self.assertTrue(board.get_all_legal_moves(white) == [])

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
        """Tests that a simple forward move is in the pawn's move list."""
        board, white = Board(), Player(Color.W)
        pawn_white = Pawn(white, [3, 4])  # d4
        pawn_white.first_move = False
        board.add_to_board(pawn_white)

        correct_move = [3, 3]  # d5

        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 1)
        self.assertTrue(correct_move in returned_moves)

    def test_pawn_white_path_impeded(self):
        """Tests that no moves are returned if the pawn's path is impeded."""
        board, white, black = create_board_and_players()
        pawn_white = Pawn(white, [3, 6])  # d2
        board.add_to_board(pawn_white)
        pawn_black = Pawn(black, [3, 5])  # d3
        board.add_to_board(pawn_black)
        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 0)

    def test_pawn_white_first_move(self):
        """Tests that two moves are available to a new unimpeded pawn."""
        board, white = Board(), Player(Color.W)
        pawn_white = Pawn(white, [3, 6])  # d2
        board.add_to_board(pawn_white)

        correct_move1 = [3, 5]  # d3
        correct_move2 = [3, 4]  # d4

        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 2)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)

    def test_pawn_white_promotion(self):
        """Tests that the four promotion moves are available to a promoting
         pawn."""
        board, white = Board(), Player(Color.W)
        pawn_white = Pawn(white, [3, 1])  # d7
        board.add_to_board(pawn_white)

        correct_move1 = [3, "Q"]  # d8
        correct_move2 = [3, "N"]  # d8
        correct_move3 = [3, "B"]  # d8
        correct_move4 = [3, "R"]  # d8

        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 4)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)
        self.assertTrue(correct_move4 in returned_moves)

    def test_pawn_white_capture(self):
        """Tests that pawn capture moves are returned correctly."""
        board, white, black = create_board_and_players()
        pawn_white = Pawn(white, [3, 4])  # d4
        pawn_white.first_move = False
        board.add_to_board(pawn_white)
        pawn_black1 = Pawn(black, [2, 3])  # c5
        board.add_to_board(pawn_black1)
        pawn_black2 = Pawn(black, [4, 3])  # e5
        board.add_to_board(pawn_black2)

        correct_move1 = [3, 3]  # d5
        correct_move2 = [2, 3]  # c5
        correct_move3 = [4, 3]  # e5

        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 3)

        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)

    def test_pawn_white_en_passant(self):
        """Tests that en passant opportunities are returned correctly."""
        board, white, black = create_board_and_players()
        pawn_white = Pawn(white, [3, 3])  # d5
        pawn_white.first_move = False
        board.add_to_board(pawn_white)
        pawn_black = Pawn(black, [2, 1])  # c7
        board.add_to_board(pawn_black)

        # simulate a move to c5, creating en passant opportunity.
        board.make_move(pawn_black, [2, 3])

        correct_move1 = [3, 2]  # d6
        correct_move2 = [2, 2]  # c6, en passant capture

        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 2)

        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)

    def test_pawn_white_capture_promo(self):
        """Tests that a pawn that is about to promote can do so via capture."""
        board, white, black = create_board_and_players()
        pawn_white = Pawn(white, [3, 1])  # d7
        board.add_to_board(pawn_white)
        rook_black1 = Rook(black, [2, 0])  # c8
        board.add_to_board(rook_black1)
        rook_black2 = Rook(black, [4, 0])  # e8
        board.add_to_board(rook_black2)
        king_black = King(black, [3, 0])  # d8
        board.add_to_board(king_black)

        correct_move1 = [2, "Q"]  # c8
        correct_move2 = [2, "N"]  # c8
        correct_move3 = [2, "B"]  # c8
        correct_move4 = [2, "R"]  # c8
        correct_move5 = [4, "Q"]  # e8
        correct_move6 = [4, "N"]  # e8
        correct_move7 = [4, "B"]  # e8
        correct_move8 = [4, "R"]  # e8

        returned_moves = pawn_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 8)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)
        self.assertTrue(correct_move4 in returned_moves)
        self.assertTrue(correct_move5 in returned_moves)
        self.assertTrue(correct_move6 in returned_moves)
        self.assertTrue(correct_move7 in returned_moves)
        self.assertTrue(correct_move8 in returned_moves)

    def test_pawn_black_simple(self):
        """Tests that a simple forward move is in the pawn's move list."""
        board, black = Board(), Player(Color.B)
        pawn_black = Pawn(black, [3, 4])  # d4
        pawn_black.first_move = False
        board.add_to_board(pawn_black)

        correct_move = [3, 5]  # d3

        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 1)
        self.assertTrue(correct_move in returned_moves)

    def test_pawn_black_path_impeded(self):
        """Tests that no moves are returned if the pawn's path is impeded."""
        board, white, black = create_board_and_players()
        pawn_white = Pawn(white, [3, 6])  # d2
        board.add_to_board(pawn_white)
        pawn_black = Pawn(black, [3, 5])  # d3
        board.add_to_board(pawn_black)
        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 0)  

    def test_pawn_black_first_move(self):
        """Tests that two moves are available to a new unimpeded pawn."""
        board, black = Board(), Player(Color.B)
        pawn_black = Pawn(black, [3, 1])  # d7
        board.add_to_board(pawn_black)

        correct_move1 = [3, 2]  # d6
        correct_move2 = [3, 3]  # d5

        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 2)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)

    def test_pawn_black_promotion(self):
        """Tests that the four promotion moves are available to a promoting
         pawn."""
        board, black = Board(), Player(Color.B)
        pawn_black = Pawn(black, [3, 6])  # d2
        board.add_to_board(pawn_black)

        correct_move1 = [3, "Q"]  # d1
        correct_move2 = [3, "N"]  # d1
        correct_move3 = [3, "B"]  # d1
        correct_move4 = [3, "R"]  # d1

        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 4)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)
        self.assertTrue(correct_move4 in returned_moves)

    def test_pawn_black_capture(self):
        """Tests that pawn capture moves are returned correctly."""
        board, white, black = create_board_and_players()
        pawn_black = Pawn(black, [3, 4])  # d4
        pawn_black.first_move = False
        board.add_to_board(pawn_black)
        pawn_white1 = Pawn(white, [2, 5])  # c3
        board.add_to_board(pawn_white1)
        pawn_white2 = Pawn(white, [4, 5])  # e3
        board.add_to_board(pawn_white2)

        correct_move1 = [3, 5]  # d3
        correct_move2 = [2, 5]  # c3
        correct_move3 = [4, 5]  # e3

        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 3)

        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)

    def test_pawn_black_en_passant(self):
        """Tests that en passant opportunities are returned correctly."""
        board, white, black = create_board_and_players()
        pawn_black = Pawn(black, [3, 4])  # d4
        pawn_black.first_move = False
        board.add_to_board(pawn_black)
        pawn_white = Pawn(white, [2, 6])  # c2
        board.add_to_board(pawn_white)

        # simulate a move to c4, creating en passant opportunity.
        board.make_move(pawn_white, [2, 4])

        correct_move1 = [3, 5]  # d3
        correct_move2 = [2, 5]  # c3, en passant capture

        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 2)

        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)

    def test_pawn_black_capture_promo(self):
        """Tests that a pawn that is about to promote can do so via capture."""
        board, white, black = create_board_and_players()
        pawn_black = Pawn(black, [3, 6])  # d2
        board.add_to_board(pawn_black)
        rook_white1 = Rook(white, [2, 7])  # c1
        board.add_to_board(rook_white1)
        rook_white2 = Rook(white, [4, 7])  # e1
        board.add_to_board(rook_white2)
        king_white = King(white, [3, 7])  # d1
        board.add_to_board(king_white)

        correct_move1 = [2, "Q"]  # c8
        correct_move2 = [2, "N"]  # c8
        correct_move3 = [2, "B"]  # c8
        correct_move4 = [2, "R"]  # c8
        correct_move5 = [4, "Q"]  # e8
        correct_move6 = [4, "N"]  # e8
        correct_move7 = [4, "B"]  # e8
        correct_move8 = [4, "R"]  # e8

        returned_moves = pawn_black.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 8)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)
        self.assertTrue(correct_move4 in returned_moves)
        self.assertTrue(correct_move5 in returned_moves)
        self.assertTrue(correct_move6 in returned_moves)
        self.assertTrue(correct_move7 in returned_moves)
        self.assertTrue(correct_move8 in returned_moves)


class TestRookMethods(unittest.TestCase):
    """Test suite for rook class."""

    def test_simple(self):
        """Verifies that a rook's returned move list has the correct
        number of moves and that the boundaries of it's movelist is correct."""
        board, white = Board(), Player(Color.W)
        rook_white = Rook(white, [3, 4])  # d4
        board.add_to_board(rook_white)

        correct_move1 = [0, 4]  # a4
        correct_move2 = [7, 4]  # h4
        correct_move3 = [3, 0]  # d8
        correct_move4 = [3, 7]  # d1

        returned_moves = rook_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 14)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)
        self.assertTrue(correct_move4 in returned_moves)

    def test_capture(self):
        """Verifies that a rook's returned move list correctly includes
        a capture opportunity."""
        board, white, black = create_board_and_players()
        rook_white = Rook(white, [3, 4])  # d4
        board.add_to_board(rook_white)

        pawn_black = Pawn(black, [2, 4])  # c4
        board.add_to_board(pawn_black)

        correct_move1 = [2, 4]  # c4

        returned_moves = rook_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 12)
        self.assertTrue(correct_move1 in returned_moves)

    def test_path_impeded(self):
        """Verifies that a rook's returned moves stops when encountering
        another of the rook's owner's pieces."""
        board, white = Board(), Player(Color.W)
        rook_white = Rook(white, [3, 4])  # d4
        board.add_to_board(rook_white)

        pawn_white = Pawn(white, [2, 4])  # c4
        board.add_to_board(pawn_white)

        incorrect_move1 = [2, 4]  # c4

        returned_moves = rook_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 11)
        self.assertTrue(incorrect_move1 not in returned_moves)


class TestBishopMethods(unittest.TestCase):
    """Test suite for bishop class."""

    def test_simple(self):
        """Verifies that a bishops's returned movelist has the correct
        number of moves and that the boundaries of it's movelist is correct."""
        board, white = Board(), Player(Color.W)
        bishop_white = Bishop(white, [3, 4])  # d4
        board.add_to_board(bishop_white)

        correct_move1 = [7, 0]  # h8
        correct_move2 = [6, 7]  # g1
        correct_move3 = [0, 1]  # a7
        correct_move4 = [0, 7]  # a1

        returned_moves = bishop_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 13)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)
        self.assertTrue(correct_move3 in returned_moves)
        self.assertTrue(correct_move4 in returned_moves)

    def test_capture(self):
        """Verifies that a bishop's returned move list correctly includes
        a capture opportunity."""
        board, white, black = create_board_and_players()
        bishop_white = Bishop(white, [3, 4])  # d4
        board.add_to_board(bishop_white)

        pawn_black = Pawn(black, [2, 5])  # c3
        board.add_to_board(pawn_black)

        correct_move1 = [2, 5]  # c3

        returned_moves = bishop_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 11)
        self.assertTrue(correct_move1 in returned_moves)

    def test_path_impeded(self):
        """Verifies that a bishop's returned moves stops when encountering
        another of the bishop's owner's pieces."""
        board, white = Board(), Player(Color.W)
        bishop_white = Bishop(white, [3, 4])  # d4
        board.add_to_board(bishop_white)

        pawn_white = Pawn(white, [2, 5])  # c3
        board.add_to_board(pawn_white)

        incorrect_move1 = [2, 4]  # c3

        returned_moves = bishop_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 10)
        self.assertTrue(incorrect_move1 not in returned_moves)


class TestKnightMethods(unittest.TestCase):
    """Test suite for knight class."""

    def test_simple(self):
        """Verifies that a knight's returned movelist has the correct
        number of moves and that the boundaries of it's movelist is correct."""
        board, white = Board(), Player(Color.W)
        knight_white = Knight(white, [3, 4])  # d4
        board.add_to_board(knight_white)
        # c6, e6, f5, f3, e2, c2, b3, b5
        correct_move_list = [[2, 2], [4, 2], [5, 3], [5, 5],
                             [4, 6], [2, 6], [1, 5], [1, 3]]

        returned_moves = knight_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 8)
        for move in correct_move_list:
            self.assertTrue(move in returned_moves)

    def test_capture(self):
        """Verifies that a knights's returned movelist correctly includes
        a capture opportunity."""
        board, white, black = create_board_and_players()
        knight_white = Knight(white, [3, 4])  # d4
        board.add_to_board(knight_white)

        pawn_black = Pawn(black, [2, 2])  # c6
        board.add_to_board(pawn_black)

        correct_move1 = [2, 2]  # c6

        returned_moves = knight_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 8)
        self.assertTrue(correct_move1 in returned_moves)


class TestQueenMethods(unittest.TestCase):
    """Test suite for queen class."""

    def test_simple(self):
        """Verifies that a queen's returned movelist has the correct
        number of moves and that the boundaries of it's movelist is correct."""
        board, white = Board(), Player(Color.W)
        queen_white = Queen(white, [3, 4])  # d4
        board.add_to_board(queen_white)

        correct_move_list = [[7, 0]]  # h8
        correct_move_list += [6, 7],  # g1
        correct_move_list += [0, 1],  # a7
        correct_move_list += [0, 7],  # a1
        correct_move_list += [0, 4],  # a4
        correct_move_list += [7, 4],  # h4
        correct_move_list += [3, 0],  # d8
        correct_move_list += [3, 7],  # d1

        returned_moves = queen_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 27)
        for move in correct_move_list:
            self.assertTrue(move in returned_moves)

    def test_capture(self):
        """Verifies that a queen's returned movelist correctly includes
        a capture opportunity."""
        board, white, black = create_board_and_players()
        queen_white = Queen(white, [3, 4])  # d4
        board.add_to_board(queen_white)

        pawn_black = Pawn(black, [2, 3])  # c5
        board.add_to_board(pawn_black)

        correct_move1 = [2, 5]  # c6

        pawn_black = Pawn(black, [2, 4])  # c4
        board.add_to_board(pawn_black)

        correct_move2 = [2, 4]  # c4

        returned_moves = queen_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 23)
        self.assertTrue(correct_move1 in returned_moves)
        self.assertTrue(correct_move2 in returned_moves)

    def test_path_impeded(self):
        """Verifies that a bishop's returned moves stops when encountering
        another of the bishop's owner's pieces."""
        board, white = Board(), Player(Color.W)
        queen_white = Queen(white, [3, 4])  # d4
        board.add_to_board(queen_white)

        pawn_white1 = Pawn(white, [2, 3])  # c5
        board.add_to_board(pawn_white1)

        incorrect_move1 = [2, 3]  # c6

        pawn_white2 = Pawn(white, [2, 4])  # c4
        board.add_to_board(pawn_white2)

        incorrect_move2 = [2, 4]  # c4

        returned_moves = queen_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 21)
        self.assertTrue(incorrect_move1 not in returned_moves)
        self.assertTrue(incorrect_move2 not in returned_moves)


class TestKingMethods(unittest.TestCase):
    """Test suite for king class."""

    def test_simple(self):
        """Verifies that a king's returned movelist has the correct
        number of moves and that the boundaries of it's movelist is correct."""
        board, white = Board(), Player(Color.W)
        king_white = King(white, [3, 4])  # d4
        board.add_to_board(king_white)

        correct_move_list = [[3, 5]]  # d3
        correct_move_list += [2, 5],  # c3
        correct_move_list += [4, 5],  # e3
        correct_move_list += [4, 4],  # e4
        correct_move_list += [2, 4],  # c4
        correct_move_list += [4, 3],  # e5
        correct_move_list += [3, 3],  # d5
        correct_move_list += [2, 3],  # c5

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 8)
        for move in correct_move_list:
            self.assertTrue(move in returned_moves)

    def test_capture(self):
        """Verifies that a king's returned movelist correctly includes
        a capture opportunity."""
        board, white, black = create_board_and_players()
        king_white = King(white, [3, 4])  # d4
        board.add_to_board(king_white)

        pawn_black = Pawn(black, [2, 3])  # c5
        board.add_to_board(pawn_black)

        correct_move_list = [[3, 5]]  # d3
        correct_move_list += [2, 5],  # c3
        correct_move_list += [4, 5],  # e3
        correct_move_list += [4, 4],  # e4
        correct_move_list += [2, 4],  # c4
        correct_move_list += [4, 3],  # e5
        correct_move_list += [3, 3],  # d5
        correct_move_list += [2, 3],  # c5

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 8)
        for move in correct_move_list:
            self.assertTrue(move in returned_moves)

    def test_path_impeded(self):
        """Verifies that a bishop's returned moves stops when encountering
        another of the bishop's owner's pieces."""
        board, white = Board(), Player(Color.W)
        king_white = King(white, [3, 4])  # d4
        board.add_to_board(king_white)

        pawn_white = Pawn(white, [2, 4])  # c4
        board.add_to_board(pawn_white)

        incorrect_move1 = [2, 4]  # c4

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(len(returned_moves) == 7)
        self.assertFalse(incorrect_move1 in returned_moves)

    def test_castling_normal(self):
        """Ensures that castling is properly returned in the King's moved
        list."""
        board, white = Board(), Player(Color.W)
        king_white = King(white, [4, 7])  # e1
        board.add_to_board(king_white)

        rook_white = Rook(white, [7, 7])  # h1
        board.add_to_board(rook_white)

        castle_move = [6, 7]  # g1

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(castle_move in returned_moves)

    def test_castling_in_check(self):
        """Ensures that castling is not returned in the King's moved
        list if the King is in check."""
        board, white, black = Board(), Player(Color.W), Player(Color.B)
        king_white = King(white, [4, 7])  # e1
        board.add_to_board(king_white)

        rook_white = Rook(white, [7, 7])  # h1
        board.add_to_board(rook_white)

        castle_move = [6, 7]  # g1

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(castle_move in returned_moves)

        rook_black = Rook(black, [4, 0])  # e7
        board.add_to_board(rook_black)
        returned_moves = king_white.get_legal_moves(board, True)
        self.assertFalse(castle_move in returned_moves)

    def test_castling_to_check(self):
        """Ensures that castling is not returned in the King's moved
        list if the King would be castling into check."""
        board, white, black = Board(), Player(Color.W), Player(Color.B)
        king_white = King(white, [4, 7])  # e1
        board.add_to_board(king_white)

        rook_white = Rook(white, [7, 7])  # h1
        board.add_to_board(rook_white)

        castle_move = [6, 7]  # g1

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(castle_move in returned_moves)

        rook_black = Rook(black, [6, 0])  # g7
        board.add_to_board(rook_black)
        returned_moves = king_white.get_legal_moves(board, True)
        self.assertFalse(castle_move in returned_moves)

    def test_castling_already_moved(self):
        """Ensures that castling is not returned in the King's moved
        list if the King has already moved."""
        board, white = Board(), Player(Color.W)
        king_white = King(white, [4, 7])  # e1
        king_white.first_move = False
        board.add_to_board(king_white)

        rook_white = Rook(white, [7, 7])  # h1
        board.add_to_board(rook_white)

        castle_move = [6, 7]  # g1

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertFalse(castle_move in returned_moves)

    def test_castling_through_attack(self):
        """Ensures that castling is not returned in the King's moved
        list if the King would be castling through an attacked square."""
        board, white, black = Board(), Player(Color.W), Player(Color.B)
        king_white = King(white, [4, 7])  # e1
        board.add_to_board(king_white)

        rook_white = Rook(white, [7, 7])  # h1
        board.add_to_board(rook_white)

        castle_move = [6, 7]  # g1

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertTrue(castle_move in returned_moves)

        rook_black = Rook(black, [5, 0])  # g7
        board.add_to_board(rook_black)
        returned_moves = king_white.get_legal_moves(board, True)
        self.assertFalse(castle_move in returned_moves)

    def test_castling_blocked_path(self):
        """Ensures that castling is not returned in the King's moved
        list if the King's path is blocked."""
        board, white = Board(), Player(Color.W)
        king_white = King(white, [4, 7])  # e1
        king_white.first_move = False
        board.add_to_board(king_white)

        rook_white = Rook(white, [7, 7])  # h1
        board.add_to_board(rook_white)

        pawn_white = Pawn(white, [6, 7])  # g1
        castle_move = [6, 7]  # g1

        returned_moves = king_white.get_legal_moves(board, True)
        self.assertFalse(castle_move in returned_moves)


if __name__ == '__main__':
    unittest.main()
