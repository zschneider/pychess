"""Contains the logic for the game engine. Board,
pieces, and player classes."""
# stdlib imports
from enum import Enum

# ------------ Pieces -------------
# All pieces have at least position and owner (a Player) attributes.


class Pawn():
    """The pawn piece. Has special 'first_move' attribute."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position
        self.first_move = True

    def get_position(self):
        """Returns this piece's position."""
        return self.position

    def get_legal_moves(self, board):
        """Returns a list of all the legal moves for this piece
        on this board."""
        moves = []
        # If first move, can move two spaces ahead
        if (self.first_move and board.check_if_empty([self.position[0],
                                                      self.position[1] + 2])):
            moves += [self.position[0], self.position[1] + 2],
        # Can move one space ahead if empty
        if board.check_if_empty([self.position[0], self.position[1] + 1]):
            moves += [self.position[0], self.position[1] + 1],
        # Can capture to the forward diagonals
        if board.check_if_opponent([self.position[0] + 1,
                                    self.position[1] + 1], self.owner):
            moves += [self.position[0] + 1, self.position[1] + 1],
        if (board.check_if_opponent([self.position[0] - 1,
                                     self.position[1] + 1], self.owner)):
            moves += [self.position[0] - 1, self.position[1] + 1],
        # TODO En Passant
        # TODO Promotion
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"P"


class Rook():
    """The rook piece."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position

    def get_position(self):
        """Returns this piece's xy position."""
        return self.position

    def get_legal_moves(self, board):
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
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"R"


class Bishop():
    """The bishop piece, which moves diagonally."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position

    def get_position(self):
        """Returns current position."""
        return self.position

    def get_legal_moves(self, board):
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
            if board.check_if_empty([pos, self.position[0]+helper]):
                moves += [pos, self.position[0]+helper],
            elif (board.check_if_opponent([pos, self.position[0]+helper],
                                          self.owner)):
                moves += [pos, self.position[0]+helper],
                break
            else:
                break
        # Toward bottom right
        helper = 0
        for pos in range(self.position[0]+1, 8):
            helper += 1
            if board.check_if_empty([pos, self.position[0]+helper]):
                moves += [pos, self.position[0]+helper],
            elif (board.check_if_opponent([pos, self.position[0]+helper],
                                          self.owner)):
                moves += [pos, self.position[0]+helper],
                break
            else:
                break
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"B"


class Knight:
    """The knight piece, which moves in an L shape."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position

    def get_position(self):
        """Returns this piece's position."""
        return self.position

    def get_legal_moves(self, board):
        """Returns the knight's legal moves."""
        moves = []
        if (board.check_if_empty([self.position[0]+1, self.position[1]+2]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]+2])):
            moves += [self.position[0]+1, self.position[1]+2],

        if (board.check_if_empty([self.position[0]-1, self.position[1]+2]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]+2])):
            moves += [self.position[0]-1, self.position[1]+2],

        if (board.check_if_empty([self.position[0]+2, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]+2,
                                         self.position[1]+1])):
            moves += [self.position[0]+2, self.position[1]+1],

        if (board.check_if_empty([self.position[0]+2, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]+2,
                                         self.position[1]-1])):
            moves += [self.position[0]+2, self.position[1]-1],

        if (board.check_if_empty([self.position[0]+1, self.position[1]-2]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]-2])):
            moves += [self.position[0]+1, self.position[1]-2],

        if (board.check_if_empty([self.position[0]-1, self.position[1]-2]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]-2])):
            moves += [self.position[0]-1, self.position[1]-2],

        if (board.check_if_empty([self.position[0]-2, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]-2,
                                         self.position[1]+1])):
            moves += [self.position[0]-2, self.position[1]+1],

        if (board.check_if_empty([self.position[0]-2, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]-2,
                                         self.position[1]-1])):
            moves += [self.position[0]-2, self.position[1]-1],

        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"K"


class Queen:
    """The queen piece, which moves in horizontal and diagonal directions."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position

    def get_position(self):
        """Returns this piece's position."""
        return self.position

    def get_legal_moves(self, board):
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
            if board.check_if_empty([pos, self.position[0]+helper]):
                moves += [pos, self.position[0]+helper],
            elif board.check_if_opponent([pos, self.position[0]+helper],
                                         self.owner):
                moves += [pos, self.position[0]+helper],
                break
            else:
                break
        # Toward bottom right
        helper = 0
        for pos in range(self.position[0]+1, 8):
            helper += 1
            if board.check_if_empty([pos, self.position[0]+helper]):
                moves += [pos, self.position[0]+helper],
            elif board.check_if_opponent([pos, self.position[0]+helper],
                                         self.owner):
                moves += [pos, self.position[0]+helper],
                break
            else:
                break
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"Q"


class King:
    """The king piece."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position
        self.first_move = True

    def get_position(self):
        """Returns the kings position."""
        return self.position

    def get_legal_moves(self, board):
        """Returns the kings legal moves."""
        moves = []
        if (board.check_if_empty([self.position[0], self.position[1]+1]) or
                board.check_if_opponent([self.position[0],
                                         self.position[1]+1])):
            moves += [self.position[0], self.position[1]+1],

        if (board.check_if_empty([self.position[0]+1, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]+1])):
            moves += [self.position[0]+1, self.position[1]+1],

        if (board.check_if_empty([self.position[0]+1, self.position[1]]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]])):
            moves += [self.position[0]+1, self.position[1]],

        if (board.check_if_empty([self.position[0]+1, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]+1,
                                         self.position[1]-1])):
            moves += [self.position[0]+1, self.position[1]-1],

        if (board.check_if_empty([self.position[0], self.position[1]-1]) or
                board.check_if_opponent([self.position[0],
                                         self.position[1]-1])):
            moves += [self.position[0], self.position[1]-1],

        if (board.check_if_empty([self.position[0]-1, self.position[1]-1]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]-1])):
            moves += [self.position[0]-1, self.position[1]-1],

        if (board.check_if_empty([self.position[0]-1, self.position[1]]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]])):
            moves += [self.position[0]-1, self.position[1]],

        if (board.check_if_empty([self.position[0]-1, self.position[1]+1]) or
                board.check_if_opponent([self.position[0]-1,
                                         self.position[1]+1])):
            moves += [self.position[0]-1, self.position[1]+1],

        # TODO Castle

        self.owner.filter_checks(self.position, moves)
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

# ---------- Board -----------


class Board:
    """Represents a standard 8x8 chess board."""
    def __init__(self):
        self.board = [None for x in range(0, 64)]

    def xy_to_num(self, xy_coords):
        """Converts an xy coordinate to the space in array."""
        if xy_coords[0] + xy_coords[1] * 8 > 63:
            return None
        return xy_coords[0] + xy_coords[1]*8

    def fails_bounds_check(self, position):
        """Returns False if the position (in xy format) is within
        board bounds."""
        if position[0] > 7 or position[0] < 0:
            return True
        if position[1] > 7 or position[1] < 0:
            return True
        return False

    def check_if_empty(self, position):
        """Returns True if the position (xy format) is empty."""
        if self.fails_bounds_check(position):
            return False
        if self.board[self.xy_to_num(position)] == None:
            return True
        else:
            return False

    def get_piece_at_position(self, position):
        """Returns the piece at the position (xy format), or None
        if the position is empty or out of bounds."""

        if self.fails_bounds_check(position):
            return None
        return self.board[self.xy_to_num(position)]

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
            self.board[self.xy_to_num(pos)] = piece

    def is_in_check(self, owner):
        """Returns true if the owner is in check (any of the opponent's pieces
            threaten the King.)"""
        # Iterate through the board, look for opponent pieces, check their legal moves,
        # see if one of the legal moves has the owner's King.
        for space in self.board:
            if space is not None and space.owner != owner:  # belongs to opponent.
                moves = space.get_legal_moves()  # gets all possible moves.
                for move in moves:
                    piece = self.get_piece_at_position(move)
                    if isinstance(piece, King) and piece.owner == owner:
                        return True

    def __repr__(self):
        rep = "   _     _     _     _     _     _     _     _  \n"
        for x in range(0, 8):
            rep += "| "
            for row in range(0, 8):
                space = self.board[x*8 + row]
                if space:
                    rep += " " + str(space) + " | "
                else:
                    rep += "    | "
            rep += "\n"
            rep += "|  _  |  _  |  _  |  _  |  _  |  _  |  _  |  _  |\n"
        return rep
