"""Contains the logic for the game engine. Board,
pieces, player, and game classes."""
# stdlib imports
from enum import Enum
from copy import deepcopy
import random

# ------------ Utility Functions -------------


def fails_bounds_check(position):
    """Returns False if the position (a xy tuple) is within
    board bounds."""
    if position[0] > 7 or position[0] < 0:
        return True
    if isinstance(position[1], str) or position[1] > 7 or position[1] < 0:
        return True
    return False


def xy_to_num(xy_coords):
    """Converts an xy coordinate tuple to an array index."""
    if xy_coords[0] + xy_coords[1] * 8 > 63:
        return None
    return xy_coords[0] + xy_coords[1]*8


# ------------ Pieces -------------
# All pieces have at least position and owner (a Player) attributes.

class Piece():
    """Base class for all peices."""

    def __init__(self, owner, position):
        self.owner = owner
        self.position = position
        self.first_move = True

    def get_position(self):
        """Returns this piece's position"""
        return self.position

    def filter_checks(self, moves, board):
        """ Arguments:
            piece - a piece, has owner and position
            moves - a list of positions
            board - the current board.
            Returns a list without moves that would lead to check."""
        final = []
        for move in moves:
            new_board = Board(board.board, board.en_passant)
            new_piece = new_board.get_piece_at_position(self.position)
            new_board.make_move(new_piece, move)
            if not new_board.is_in_check(new_piece.owner):
                final += move,
        return final


class Pawn(Piece):
    """The pawn piece. Has special 'first_move' attribute."""

    def get_legal_moves(self, board, consider_checks):
        """Returns a list of all the legal moves for this piece
        on this board."""
        moves = []
        # If first move, can move two spaces ahead, if both spaces empty
        if self.owner.color == Color.B:
            if (self.first_move and
                    board.check_if_empty([self.position[0],
                                          self.position[1] + 1]) and
                    board.check_if_empty([self.position[0],
                                          self.position[1] + 2])):
                moves += [self.position[0], self.position[1] + 2],
            # Can move one space ahead if empty
            if board.check_if_empty([self.position[0], self.position[1] + 1]):
                # end of board, promotion
                if self.position[1] + 1 == 7:
                    moves += [self.position[0], "Q"],
                    moves += [self.position[0], "N"],
                    moves += [self.position[0], "R"],
                    moves += [self.position[0], "B"],
                else:
                    moves += [self.position[0], self.position[1] + 1],
            # Can capture to the forward diagonals
            if board.check_if_opponent([self.position[0] + 1,
                                        self.position[1] + 1], self.owner):
                if self.position[1] + 1 == 7:
                    moves += [self.position[0] + 1, "Q"],
                    moves += [self.position[0] + 1, "N"],
                    moves += [self.position[0] + 1, "R"],
                    moves += [self.position[0] + 1, "B"],
                else:
                    moves += [self.position[0] + 1, self.position[1] + 1],
            if (board.check_if_opponent([self.position[0] - 1,
                                         self.position[1] + 1], self.owner)):
                if self.position[1] + 1 == 7:
                    moves += [self.position[0] - 1, "Q"],
                    moves += [self.position[0] - 1, "N"],
                    moves += [self.position[0] - 1, "R"],
                    moves += [self.position[0] - 1, "B"],
                else:
                    moves += [self.position[0] - 1, self.position[1] + 1],
            # check if there is an en_passant opportunity
            if board.en_passant and self.owner != board.en_passant.owner:
                if board.en_passant.position == [self.position[0]+1,
                                                 self.position[1]]:
                    moves += [self.position[0]+1, self.position[1]+1],

                elif board.en_passant.position == [self.position[0]-1,
                                                   self.position[1]]:
                    moves += [self.position[0]-1, self.position[1]+1],

        if self.owner.color == Color.W:
            if (self.first_move and
                    board.check_if_empty([self.position[0],
                                          self.position[1] - 1]) and
                    board.check_if_empty([self.position[0],
                                          self.position[1] - 2])):
                moves += [self.position[0], self.position[1] - 2],
            # Can move one space ahead if empty
            if board.check_if_empty([self.position[0], self.position[1] - 1]):
                if self.position[1] - 1 == 0:
                    moves += [self.position[0], "Q"],
                    moves += [self.position[0], "N"],
                    moves += [self.position[0], "R"],
                    moves += [self.position[0], "B"],
                else:
                    moves += [self.position[0], self.position[1] - 1],
            # Can capture to the forward diagonals
            if board.check_if_opponent([self.position[0] + 1,
                                        self.position[1] - 1], self.owner):
                if self.position[1] - 1 == 0:
                    moves += [self.position[0] + 1, "Q"],
                    moves += [self.position[0] + 1, "N"],
                    moves += [self.position[0] + 1, "R"],
                    moves += [self.position[0] + 1, "B"],
                else:
                    moves += [self.position[0] + 1, self.position[1] - 1],
            if (board.check_if_opponent([self.position[0] - 1,
                                         self.position[1] - 1], self.owner)):
                if self.position[1] - 1 == 0:
                    moves += [self.position[0] - 1, "Q"],
                    moves += [self.position[0] - 1, "N"],
                    moves += [self.position[0] - 1, "R"],
                    moves += [self.position[0] - 1, "B"],
                else:
                    moves += [self.position[0] - 1, self.position[1] - 1],
            if board.en_passant and self.owner != board.en_passant.owner:
                if board.en_passant.position == [self.position[0]+1,
                                                 self.position[1]]:
                    moves += [self.position[0]+1, self.position[1]-1],

                if board.en_passant.position == [self.position[0]-1,
                                                 self.position[1]]:
                    moves += [self.position[0]-1, self.position[1]-1],

        if consider_checks:
            moves = self.filter_checks(moves, board)
        return moves

    def __repr__(self):
        return self.owner.color.name+"P"


class Rook(Piece):
    """The rook piece."""

    def get_legal_moves(self, board, consider_checks):
        """Returns a list of all the legal moves for this piece
        on this board."""
        # Can move all spaces until blocked
        moves = []
        for x_coord in range(self.position[0]+1, 8):
            if board.check_if_empty([x_coord, self.position[1]]):
                moves += [x_coord, self.position[1]],
            elif board.check_if_opponent([x_coord, self.position[1]],
                                         self.owner):
                moves += [x_coord, self.position[1]],
                break
            else:
                # Your own piece or wall
                break
        for x_coord in range(self.position[0]-1, -1, -1):
            if board.check_if_empty([x_coord, self.position[1]]):
                moves += [x_coord, self.position[1]],
            elif board.check_if_opponent([x_coord, self.position[1]],
                                         self.owner):
                moves += [x_coord, self.position[1]],
                break
            else:
                # Your own piece or wall
                break
        for y_coord in range(self.position[1]+1, 8):
            if board.check_if_empty([self.position[0], y_coord]):
                moves += [self.position[0], y_coord],
            elif board.check_if_opponent([self.position[0], y_coord],
                                         self.owner):
                moves += [self.position[0], y_coord],
                break
            else:
                # Your own piece or wall
                break
        for y_coord in range(self.position[1]-1, -1, -1):
            if board.check_if_empty([self.position[0], y_coord]):
                moves += [self.position[0], y_coord],
            elif board.check_if_opponent([self.position[0], y_coord],
                                         self.owner):
                moves += [self.position[0], y_coord],
                break
            else:
                # Your own piece or wall
                break
        if consider_checks:
            moves = self.filter_checks(moves, board)
        return moves

    def __repr__(self):
        return self.owner.color.name+"R"


class Bishop(Piece):
    """The bishop piece, which moves diagonally."""

    def get_legal_moves(self, board, consider_checks):
        """Returns this piece's legal moves."""
        moves = []
        # Towards top right
        helper = 0
        for pos in range(self.position[1]-1, -1, -1):
            helper += 1
            if board.check_if_empty([self.position[0]+helper, pos]):
                moves += [self.position[0]+helper, pos],
            elif (board.check_if_opponent([self.position[0]+helper, pos],
                                          self.owner)):
                moves += [self.position[0]+helper, pos],
                break
            else:
                break
        # Toward top left
        helper = 0
        for pos in range(self.position[1]-1, -1, -1):
            helper += 1
            if board.check_if_empty([self.position[0]-helper, pos]):
                moves += [self.position[0]-helper, pos],
            elif board.check_if_opponent([self.position[0]-helper, pos],
                                         self.owner):
                moves += [self.position[0]-helper, pos],
                break
            else:
                break
        # Toward bottom left
        helper = 0
        for pos in range(self.position[0]-1, -1, -1):
            helper += 1
            if board.check_if_empty([pos, self.position[1]+helper]):
                moves += [pos, self.position[1]+helper],
            elif (board.check_if_opponent([pos, self.position[1]+helper],
                                          self.owner)):
                moves += [pos, self.position[1]+helper],
                break
            else:
                break
        # Toward bottom right
        helper = 0
        for pos in range(self.position[0]+1, 8):
            helper += 1
            if board.check_if_empty([pos, self.position[1]+helper]):
                moves += [pos, self.position[1]+helper],
            elif (board.check_if_opponent([pos, self.position[1]+helper],
                                          self.owner)):
                moves += [pos, self.position[1]+helper],
                break
            else:
                break
        if consider_checks:
            moves = self.filter_checks(moves, board)
        return moves

    def __repr__(self):
        return self.owner.color.name+"B"


class Knight(Piece):
    """The knight piece, which moves in an L shape."""

    def get_legal_moves(self, board, consider_checks):
        """Returns the knight's legal moves."""
        moves = []
        if (board.check_if_empty([self.position[0]+1, self.position[1]+2]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]+2], self.owner)):
            moves += [self.position[0]+1, self.position[1]+2],

        if (board.check_if_empty([self.position[0]-1, self.position[1]+2]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]+2], self.owner)):
            moves += [self.position[0]-1, self.position[1]+2],

        if (board.check_if_empty([self.position[0]+2, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]+2,
                                         self.position[1]+1], self.owner)):
            moves += [self.position[0]+2, self.position[1]+1],

        if (board.check_if_empty([self.position[0]+2, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]+2,
                                         self.position[1]-1], self.owner)):
            moves += [self.position[0]+2, self.position[1]-1],

        if (board.check_if_empty([self.position[0]+1, self.position[1]-2]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]-2], self.owner)):
            moves += [self.position[0]+1, self.position[1]-2],

        if (board.check_if_empty([self.position[0]-1, self.position[1]-2]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]-2], self.owner)):
            moves += [self.position[0]-1, self.position[1]-2],

        if (board.check_if_empty([self.position[0]-2, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]-2,
                                         self.position[1]+1], self.owner)):
            moves += [self.position[0]-2, self.position[1]+1],

        if (board.check_if_empty([self.position[0]-2, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]-2,
                                         self.position[1]-1], self.owner)):
            moves += [self.position[0]-2, self.position[1]-1],

        if consider_checks:
            moves = self.filter_checks(moves, board)
        return moves

    def __repr__(self):
        return self.owner.color.name+"N"


class Queen(Piece):
    """The queen piece, which moves in horizontal and diagonal directions."""

    def get_legal_moves(self, board, consider_checks):
        """Returns a list of all legal moves for this piece."""
        moves = []
        for pos in range(self.position[0]+1, 8):
            if board.check_if_empty([pos, self.position[1]]):
                moves += [pos, self.position[1]],
            elif board.check_if_opponent([pos, self.position[1]], self.owner):
                moves += [pos, self.position[1]],
                break
            else:
                # Your own piece or wall
                break
        for pos in range(self.position[0]-1, -1, -1):
            if board.check_if_empty([pos, self.position[1]]):
                moves += [pos, self.position[1]],
            elif board.check_if_opponent([pos, self.position[1]], self.owner):
                moves += [pos, self.position[1]],
                break
            else:
                # Your own piece or wall
                break
        for pos in range(self.position[1]+1, 8):
            if board.check_if_empty([self.position[0], pos]):
                moves += [self.position[0], pos],
            elif board.check_if_opponent([self.position[0], pos], self.owner):
                moves += [self.position[0], pos],
                break
            else:
                # Your own piece or wall
                break
        for pos in range(self.position[1]-1, -1, -1):
            if board.check_if_empty([self.position[0], pos]):
                moves += [self.position[0], pos],
            elif board.check_if_opponent([self.position[0], pos], self.owner):
                moves += [self.position[0], pos],
                break
            else:
                # Your own piece or wall
                break
        helper = 0
        for pos in range(self.position[1]-1, -1, -1):
            helper += 1
            if board.check_if_empty([self.position[0]+helper, pos]):
                moves += [self.position[0]+helper, pos],
            elif board.check_if_opponent([self.position[0]+helper, pos],
                                         self.owner):
                moves += [self.position[0]+helper, pos],
                break
            else:
                break
        # Toward top left
        helper = 0
        for pos in range(self.position[1]-1, -1, -1):
            helper += 1
            if board.check_if_empty([self.position[0]-helper, pos]):
                moves += [self.position[0]-helper, pos],
            elif board.check_if_opponent([self.position[0]-helper, pos],
                                         self.owner):
                moves += [self.position[0]-helper, pos],
                break
            else:
                break
        # Toward bottom left
        helper = 0
        for pos in range(self.position[0]-1, -1, -1):
            helper += 1
            if board.check_if_empty([pos, self.position[1]+helper]):
                moves += [pos, self.position[1]+helper],
            elif board.check_if_opponent([pos, self.position[1]+helper],
                                         self.owner):
                moves += [pos, self.position[1]+helper],
                break
            else:
                break
        # Toward bottom right
        helper = 0
        for pos in range(self.position[0]+1, 8):
            helper += 1
            if board.check_if_empty([pos, self.position[1]+helper]):
                moves += [pos, self.position[1]+helper],
            elif board.check_if_opponent([pos, self.position[1]+helper],
                                         self.owner):
                moves += [pos, self.position[1]+helper],
                break
            else:
                break

        if consider_checks:
            moves = self.filter_checks(moves, board)
        return moves

    def __repr__(self):
        return self.owner.color.name+"Q"


class King(Piece):
    """The king piece."""

    def get_legal_moves(self, board, consider_checks):
        """Returns the kings legal moves."""
        moves = []
        if (board.check_if_empty([self.position[0], self.position[1]+1]) or
                board.check_if_opponent([self.position[0],
                                         self.position[1]+1], self.owner)):
            moves += [self.position[0], self.position[1]+1],

        if (board.check_if_empty([self.position[0]+1, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]+1], self.owner)):
            moves += [self.position[0]+1, self.position[1]+1],

        if (board.check_if_empty([self.position[0]+1, self.position[1]]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]], self.owner)):
            moves += [self.position[0]+1, self.position[1]],

        if (board.check_if_empty([self.position[0]+1, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]-1], self.owner)):
            moves += [self.position[0]+1, self.position[1]-1],

        if (board.check_if_empty([self.position[0], self.position[1]-1]) or
                board.check_if_opponent([self.position[0],
                                         self.position[1]-1], self.owner)):
            moves += [self.position[0], self.position[1]-1],

        if (board.check_if_empty([self.position[0]-1, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]-1], self.owner)):
            moves += [self.position[0]-1, self.position[1]-1],

        if (board.check_if_empty([self.position[0]-1, self.position[1]]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]], self.owner)):
            moves += [self.position[0]-1, self.position[1]],

        if (board.check_if_empty([self.position[0]-1, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]+1], self.owner)):
            moves += [self.position[0]-1, self.position[1]+1],

        """
        # rules of castling:
        # 1. king cant be in check
        # 2. king cannot travel through or land in attacked square
        # 3. neither the king or castling rook can have moved
        # 4. there must not be any pieces in between the king and rook
        """
        if consider_checks and self.first_move and not board.is_in_check(self.owner):
            kingsiderook = board.get_piece_at_position([self.position[0]+3, self.position[1]])
            if (kingsiderook and kingsiderook.owner == self.owner and kingsiderook.first_move and
                board.check_if_empty([self.position[0]+1, self.position[1]]) and
                    board.check_if_empty([self.position[0]+2, self.position[1]]) and
                    not board.is_attacked([self.position[0]+1, self.position[1]], self.owner)):
                # also need to make sure enemy pieces aren't attacking any square that king travels through.
                moves += [self.position[0]+2, self.position[1]],
            queensiderook = board.get_piece_at_position([self.position[0]-4, self.position[1]])
            if (queensiderook and queensiderook.owner == self.owner and queensiderook.first_move and
                board.check_if_empty([self.position[0]-1, self.position[1]]) and
                    board.check_if_empty([self.position[0]-2, self.position[1]]) and
                    board.check_if_empty([self.position[0]-3, self.position[1]]) and
                    not board.is_attacked([self.position[0]-1, self.position[1]], self.owner)):
                moves += [self.position[0]-2, self.position[1]],

        if consider_checks:
            moves = self.filter_checks(moves, board)
        return moves

    def __repr__(self):
        return self.owner.color.name+"K"

# ---------- Players -----------


class Color(Enum):
    """Simple enum that represents white and black as 0 and 1 respectively."""
    W = 0
    B = 1


class Player:
    """Represents a player, which has a color."""
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        if self.color == Color.W:
            return "White"
        else:
            return "Black"

# ---------- Board -----------


class Board:
    """Represents a standard 8x8 chess board."""
    def __init__(self, board=None, en_passant=None):
        # Passing in a board and pieces list.
        if board is not None:
            self.board = deepcopy(board)
            self.en_passant = deepcopy(en_passant)
            self.pieces = []
            for piece in self.board:
                if piece:
                    self.pieces += piece,
        # Fresh game.
        else:
            self.board = [None for x in range(0, 64)]
            self.pieces = []
            self.en_passant = None

    def check_if_empty(self, position):
        """Returns True if the position (xy format) is empty."""
        if fails_bounds_check(position):
            return False
        if self.board[xy_to_num(position)] == None:
            return True
        else:
            return False

    def get_piece_at_position(self, position):
        """Returns the piece at the position (xy format), or None
        if the position is empty or out of bounds."""
        if fails_bounds_check(position):
            return None
        return self.board[xy_to_num(position)]

    def check_if_opponent(self, position, owner):
        """Returns True if the piece at the position does not belong to
        the player. False if the position is empty or the piece
        belongs to the owner."""
        piece = self.get_piece_at_position(position)
        if piece:
            return piece.owner != owner
        return False

    def add_to_board(self, piece):
        """Adds the piece to the board using the piece's position.
        If there is already a piece there, do nothing."""
        pos = piece.position
        if self.check_if_empty(pos):
            self.board[xy_to_num(pos)] = piece
            self.pieces += piece,

    def undo_move(self):
        """Restores the board to one move prior. Returns None if no
        moves have been made yet."""
        piece = self.get_piece_at_position(self.last_move_new_position)
        self.remove_from_board(self.last_move_new_position)
        piece.position = self.last_move_prev_position
        self.add_to_board(piece)
        if self.last_move_captured_piece:
            self.add_to_board(self.last_move_captured_piece)

    def remove_from_board(self, position):
        """Removes the piece from the board, using the passed in position.
        Returns None if no piece was removed. Otherwise returns the piece."""
        piece = self.board[xy_to_num(position)]
        if piece is None:
            return None
        if piece in self.pieces:
            self.pieces.remove(piece)
            self.board[xy_to_num(position)] = None
            return piece

    def is_in_check(self, owner):
        """Returns true if the owner is in check (any of the opponent's pieces
            threaten the King.)"""
        for piece in self.pieces:
            # piece exists and belongs to opponent.
            if piece.owner != owner:
                # The False here specifies that we should get ALL moves, even
                # those that would leave the opponent King in check.
                moves = piece.get_legal_moves(self, False)
                for move in moves:
                    piece = self.get_piece_at_position(move)
                    if isinstance(piece, King) and piece.owner == owner:
                        return True
        return False

    def is_attacked(self, position, owner):
        """Returns true if the position is attacked by the opponent."""
        for piece in self.pieces:
            if piece.owner != owner:
                moves = piece.get_legal_moves(self, False)
                for move in moves:
                    if move == position:
                        return True
        return False

    def get_all_legal_moves(self, owner):
        """Gets the legal moves for all the player's pieces, and stores them
        in a list of [piece, move_position] format."""
        legal_moves = []
        for piece in self.pieces:
            if piece.owner.color is owner.color:
                for move in piece.get_legal_moves(self, True):
                    legal_moves += [piece, move],
        return legal_moves

    def make_move(self, piece, to_position):
        """Make a move. Handles captures. Checks for en_passant."""
        self.remove_from_board(piece.position)
        # Handle all pawn moves including en_passant and promotion
        if isinstance(piece, Pawn):
            self.make_pawn_move(piece, to_position)

        # castling
        elif (isinstance(piece, King) and
              (abs(piece.position[0] - to_position[0]) > 1)):
            self.make_castle_move(piece, to_position)

        else:
            piece.position = to_position

            self.en_passant = None
            self.remove_from_board(to_position)
            self.add_to_board(piece)

        piece.first_move = False

    def make_pawn_move(self, piece, to_position):
        """Only called by make_move. Aesthetic function to tidy up make_move"""
        if isinstance(to_position[1], str):
            if to_position[1] == "Q":
                piece = Queen(piece.owner, [to_position[0], -1])
            elif to_position[1] == "N":
                piece = Knight(piece.owner, [to_position[0], -1])
            elif to_position[1] == "B":
                piece = Bishop(piece.owner, [to_position[0], -1])
            elif to_position[1] == "R":
                piece = Rook(piece.owner, [to_position[0], -1])
            if piece.owner.color == Color.W:
                piece.position[1] = 0
            else:
                piece.position[1] = 7
            self.remove_from_board(piece.position)

            self.en_passant = None
            self.add_to_board(piece)

        elif (piece.position[1] + 2 == to_position[1] or
              piece.position[1] - 2 == to_position[1]):
            piece.position = to_position

            self.en_passant = piece  # en_passant is possible on next turn
            self.remove_from_board(to_position)
            self.add_to_board(piece)

        # en passant is being performed if we capturing an empty diagonal square with a pawn
        elif ((piece.position[1] + 1 == to_position[1] or
               piece.position[1] - 1 == to_position[1]) and
              ((piece.position[0] + 1 == to_position[0] and
                self.check_if_empty(to_position)) or
               (piece.position[0] - 1 == to_position[0] and
                self.check_if_empty(to_position)))):

            self.remove_from_board(self.en_passant.position)

            piece.position = to_position

            self.en_passant = None
            self.add_to_board(piece)

        else:
            piece.position = to_position

            self.en_passant = None
            self.remove_from_board(to_position)
            self.add_to_board(piece)

    def make_castle_move(self, piece, to_position):
        """Only called by make_move. Handles castling. Aesthetic."""
        # kingside
        if piece.position[0] - to_position[0] == -2:
            piece.position = to_position
            self.add_to_board(piece)
            rook = self.get_piece_at_position([to_position[0]+1, to_position[1]])
            self.remove_from_board(rook.position)
            rook.position = [rook.position[0] - 2, rook.position[1]]
            self.add_to_board(rook)
        # queenside
        elif piece.position[0] - to_position[0] == 2:
            piece.position = to_position
            self.add_to_board(piece)
            rook = self.get_piece_at_position([to_position[0]-2, to_position[1]])
            self.remove_from_board(rook.position)
            rook.position = [rook.position[0] + 3, rook.position[1]]
            self.add_to_board(rook)
        else:
            raise Exception

        self.en_passant = None

    def __repr__(self):
        rep = "     0     1     2     3     4     5     6     7  \n"
        rep += "     _     _     _     _     _     _     _     _  \n"
        for x in range(0, 8):
            rep += str(x+8-(2*x)) + " | "
            for row in range(0, 8):
                space = self.board[x*8 + row]
                if space:
                    rep += " " + str(space) + " | "
                else:
                    rep += "    | "
            rep += "  "+str(x)+"\n"
            rep += "  |  _  |  _  |  _  |  _  |  _  |  _  |  _  |  _  |\n"
        rep += "     a     b     c     d     e     f     g     h"
        return rep

# ---------- Game -----------


class Game():
    """Contains a game, players, and pieces."""
    def __init__(self, board=Board(),
                 white=Player(Color.W),
                 black=Player(Color.B)):
        self.board = board
        self.white = white
        self.black = black
        self.current_turn = self.white
        self.fifty_move_rule = 0

    def new_game(self):
        """Sets the board to a new game."""
        self.board.board = [None for x in range(0, 64)]
        self.board.pieces = []
        # Pawns
        for pawn_pos in range(0, 8):
            new_white_pawn = Pawn(self.white, [pawn_pos, 6])
            new_black_pawn = Pawn(self.black, [pawn_pos, 1])
            self.board.add_to_board(new_white_pawn)
            self.board.add_to_board(new_black_pawn)

        # Rooks
        white_rook_one = Rook(self.white, [0, 7])
        white_rook_two = Rook(self.white, [7, 7])
        self.board.add_to_board(white_rook_one)
        self.board.add_to_board(white_rook_two)

        black_rook_one = Rook(self.black, [0, 0])
        black_rook_two = Rook(self.black, [7, 0])
        self.board.add_to_board(black_rook_one)
        self.board.add_to_board(black_rook_two)

        # Knights
        white_knight_one = Knight(self.white, [1, 7])
        white_knight_two = Knight(self.white, [6, 7])
        self.board.add_to_board(white_knight_one)
        self.board.add_to_board(white_knight_two)

        black_knight_one = Knight(self.black, [1, 0])
        black_knight_two = Knight(self.black, [6, 0])
        self.board.add_to_board(black_knight_one)
        self.board.add_to_board(black_knight_two)

        # Bishops
        white_bishop_one = Bishop(self.white, [2, 7])
        white_bishop_two = Bishop(self.white, [5, 7])
        self.board.add_to_board(white_bishop_one)
        self.board.add_to_board(white_bishop_two)

        black_bishop_one = Bishop(self.black, [2, 0])
        black_bishop_two = Bishop(self.black, [5, 0])
        self.board.add_to_board(black_bishop_one)
        self.board.add_to_board(black_bishop_two)

        # Queen and King
        white_queen = Queen(self.white, [3, 7])
        white_king = King(self.white, [4, 7])
        self.board.add_to_board(white_queen)
        self.board.add_to_board(white_king)

        black_queen = Queen(self.black, [3, 0])
        black_king = King(self.black, [4, 0])
        self.board.add_to_board(black_queen)
        self.board.add_to_board(black_king)

    def change_turn(self):
        """Switches the turn."""
        if self.current_turn == self.white:
            self.current_turn = self.black
        else:
            self.current_turn = self.white

    def make_random_move(self):
        """Fetches the current players list of possible moves,
        and then chooses and executes one at random."""
        moves_list = self.board.get_all_legal_moves(self.current_turn)
        tup = random.choice(moves_list)
        self.make_move(tup[0], tup[1])

    def make_move(self, piece, to_position):
        """Make a move. Error if the piece does not belong to
        the owner of that piece. Handles captures."""
        if piece.owner != self.current_turn:
            raise Exception
        if (isinstance(piece, Pawn) or
                self.board.get_piece_at_position(to_position)):
            self.fifty_move_rule = 0
        else:
            self.fifty_move_rule += 1
        self.board.make_move(piece, to_position)
        self.change_turn()

    def checkmate(self):
        """Returns the winner if checkmate, None otherwise."""
        moves_list_black = self.board.get_all_legal_moves(self.black)
        if len(moves_list_black) == 0 and self.board.is_in_check(self.black):
            return self.white
        moves_list_white = self.board.get_all_legal_moves(self.white)
        if len(moves_list_white) == 0 and self.board.is_in_check(self.white):
            return self.black
        return None

    def stalemate(self):
        """Returns True if stalemate."""
        pieces = self.board.pieces

        if self.fifty_move_rule > 100:
            return True

        if len(pieces) == 2:
            for piece in pieces:
                if isinstance(piece, King):
                    return True

        if len(pieces) == 3:
            knight_count = 0
            bishop_count = 0
            for piece in pieces:
                if isinstance(piece, Bishop):
                    bishop_count += 1
                if isinstance(piece, Knight):
                    knight_count += 1
            if knight_count == 1 or bishop_count == 1:
                return True

        moves_list = self.board.get_all_legal_moves(self.current_turn)
        if (len(moves_list) == 0 and
                not self.board.is_in_check(self.current_turn)):
            return True

        return False
