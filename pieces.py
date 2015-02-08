import board
from players import Player

class Piece:
    """Parent class for chess pieces. Neccesary?"""

    def __repr__(self):
        return "A blank space."
    
class Pawn(Piece):
    """The pawn piece."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position
        self.first_move = True

    def get_position(self):
        return self.position
    
    def get_legal_moves(self, board):
        moves = []
        # If first move, can move two spaces ahead
        if (self.first_move and 
            board.check_if_empty([self.position[0], self.position[1] + 2])):
            moves += [self.position[0], self.position[1] + 2],
        # Can move one space ahead if empty
        if (board.check_if_empty([self.position[0], self.position[1] + 1])):
            moves += [self.position[0], self.position[1] + 1],
        # Can capture to the forward diagonals
        if (board.check_if_opponent([self.position[0] + 1, self.position[1] + 1],self.owner)):
            moves += [self.position[0] + 1, self.position[1] + 1],
        if (board.check_if_opponent([self.position[0] - 1, self.position[1] + 1],self.owner)):
            moves += [self.position[0] - 1, self.position[1] + 1],
        # En Passant
        # Promotion
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"P"

class Rook(Piece):
    """The rook piece."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position

    def get_position(self):
        return self.position

    def get_legal_moves(self, board):
        # Can move all spaces until blocked
        moves = []
        for x in range(self.position[0]+1, 8):
            if (board.check_if_empty([x, self.position[1]])):
                moves += [x, self.position[1]],
            elif (board.check_if_opponent([x, self.position[1]],self.owner)):
                moves += [x, self.position[1]],
                break
            else:
                #Your own piece or wall
                break
        for x in range(self.position[0]-1, -1, -1):
            if (board.check_if_empty([x, self.position[1]])):
                moves += [x, self.position[1]],
            elif (board.check_if_opponent([x, self.position[1]],self.owner)):
                moves += [x, self.position[1]],
                break
            else:
                #Your own piece or wall
                break
        for y in range(self.position[1]+1, 8):
            if (board.check_if_empty([self.position[0], y])):
                moves += [self.position[0], y],
            elif (board.check_if_opponent([self.position[0], y],self.owner)):
                moves += [self.position[0], y],
                break
            else:
                #Your own piece or wall
                break
        for y in range(self.position[1]-1, -1, -1):
            if (board.check_if_empty([self.position[0], y])):
                moves += [self.position[0], y],
            elif (board.check_if_opponent([self.position[0], y],self.owner)):
                moves += [self.position[0], y],
                break
            else:
                #Your own piece or wall
                break
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"R"

class Bishop(Piece):
    """The bishop piece, which moves diagonally."""
    def __init__(self,owner,position):
        self.owner = owner
        self.position = position

    def get_position(self):
        return self.position

    def get_legal_moves(self, board):
        moves = []
        # Towards top right
        helper = 0
        for x in range(self.position[1]-1,-1,-1):
            helper += 1
            if (board.check_if_empty([self.position[0]+helper,x])):
                moves += [self.position[0]+helper,x],
            elif (board.check_if_opponent([self.position[0]+helper,x],self.owner)):
                moves += [self.position[0]+helper,x],
                break
            else:
                break
        # Toward top left
        helper = 0
        for x in range(self.position[1]-1,-1,-1):
            helper += 1
            if (board.check_if_empty([self.position[0]-helper,x])):
                moves += [self.position[0]-helper,x],
            elif (board.check_if_opponent([self.position[0]-helper,x],self.owner)):
                moves += [self.position[0]-helper,x],
                break
            else:
                break
        # Toward bottom left
        helper = 0
        for x in range(self.position[0]-1,-1,-1):
            helper += 1
            if (board.check_if_empty([x,self.position[0]+helper])):
                moves += [x,self.position[0]+helper],
            elif (board.check_if_opponent([x,self.position[0]+helper],self.owner)):
                moves += [x,self.position[0]+helper],
                break
            else:
                break
        # Toward bottom right
        helper = 0
        for x in range(self.position[0]+1,8):
            helper += 1
            if (board.check_if_empty([x,self.position[0]+helper])):
                moves += [x,self.position[0]+helper],
            elif (board.check_if_opponent([x,self.position[0]+helper],self.owner)):
                moves += [x,self.position[0]+helper],
                break
            else:
                break
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"B"

class Knight(Piece):
    """The knight piece, which moves in an L shape."""
    def __init__(self,owner,position):
        self.owner = owner
        self.position = position

    def get_position(self):
        return self.position

    def get_legal_moves(self, board):
        moves = []
        if (board.check_if_empty([self.position[0]+1,self.position[1]+2]) or
            board.check_if_opponent([self.position[0]+1,self.position[1]+2])):
            moves += [self.position[0]+1,self.position[1]+2],

        if (board.check_if_empty([self.position[0]-1,self.position[1]+2]) or
            board.check_if_opponent([self.position[0]-1,self.position[1]+2])):
            moves += [self.position[0]-1,self.position[1]+2],

        if (board.check_if_empty([self.position[0]+2,self.position[1]+1]) or
            board.check_if_opponent([self.position[0]+2,self.position[1]+1])):
            moves += [self.position[0]+2,self.position[1]+1],

        if (board.check_if_empty([self.position[0]+2,self.position[1]-1]) or
            board.check_if_opponent([self.position[0]+2,self.position[1]-1])):
            moves += [self.position[0]+2,self.position[1]-1],

        if (board.check_if_empty([self.position[0]+1,self.position[1]-2]) or
            board.check_if_opponent([self.position[0]+1,self.position[1]-2])):
            moves += [self.position[0]+1,self.position[1]-2],

        if (board.check_if_empty([self.position[0]-1,self.position[1]-2]) or
            board.check_if_opponent([self.position[0]-1,self.position[1]-2])):
            moves += [self.position[0]-1,self.position[1]-2],

        if (board.check_if_empty([self.position[0]-2,self.position[1]+1]) or
            board.check_if_opponent([self.position[0]-2,self.position[1]+1])):
            moves += [self.position[0]-2,self.position[1]+1],

        if (board.check_if_empty([self.position[0]-2,self.position[1]-1]) or
            board.check_if_opponent([self.position[0]-2,self.position[1]-1])):
            moves += [self.position[0]-2,self.position[1]-1],

        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"K"

class Queen(Piece):
    """The queen piece, which moves in horizontal and diagonal directions."""
    def __init__(self,owner,position):
        self.owner = owner
        self.position = position

    def get_position(self):
        return self.position

    def get_legal_moves(self, board):
        moves = []
        for x in range(self.position[0]+1, 8):
            if (board.check_if_empty([x, self.position[1]])):
                moves += [x, self.position[1]],
            elif (board.check_if_opponent([x, self.position[1]],self.owner)):
                moves += [x, self.position[1]],
                break
            else:
                #Your own piece or wall
                break
        for x in range(self.position[0]-1, -1, -1):
            if (board.check_if_empty([x, self.position[1]])):
                moves += [x, self.position[1]],
            elif (board.check_if_opponent([x, self.position[1]],self.owner)):
                moves += [x, self.position[1]],
                break
            else:
                #Your own piece or wall
                break
        for y in range(self.position[1]+1, 8):
            if (board.check_if_empty([self.position[0], y])):
                moves += [self.position[0], y],
            elif (board.check_if_opponent([self.position[0], y],self.owner)):
                moves += [self.position[0], y],
                break
            else:
                #Your own piece or wall
                break
        for y in range(self.position[1]-1, -1, -1):
            if (board.check_if_empty([self.position[0], y])):
                moves += [self.position[0], y],
            elif (board.check_if_opponent([self.position[0], y],self.owner)):
                moves += [self.position[0], y],
                break
            else:
                #Your own piece or wall
                break
        helper = 0
        for x in range(self.position[1]-1,-1,-1):
            helper += 1
            if (board.check_if_empty([self.position[0]+helper,x])):
                moves += [self.position[0]+helper,x],
            elif (board.check_if_opponent([self.position[0]+helper,x],self.owner)):
                moves += [self.position[0]+helper,x],
                break
            else:
                break
        # Toward top left
        helper = 0
        for x in range(self.position[1]-1,-1,-1):
            helper += 1
            if (board.check_if_empty([self.position[0]-helper,x])):
                moves += [self.position[0]-helper,x],
            elif (board.check_if_opponent([self.position[0]-helper,x],self.owner)):
                moves += [self.position[0]-helper,x],
                break
            else:
                break
        # Toward bottom left
        helper = 0
        for x in range(self.position[0]-1,-1,-1):
            helper += 1
            if (board.check_if_empty([x,self.position[0]+helper])):
                moves += [x,self.position[0]+helper],
            elif (board.check_if_opponent([x,self.position[0]+helper],self.owner)):
                moves += [x,self.position[0]+helper],
                break
            else:
                break
        # Toward bottom right
        helper = 0
        for x in range(self.position[0]+1,8):
            helper += 1
            if (board.check_if_empty([x,self.position[0]+helper])):
                moves += [x,self.position[0]+helper],
            elif (board.check_if_opponent([x,self.position[0]+helper],self.owner)):
                moves += [x,self.position[0]+helper],
                break
            else:
                break
        self.owner.filter_checks(self.position, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"Q"

class King(Piece):
    """The king piece."""
    def __init__(self, owner, position):
        self.owner = owner
        self.position = position

    def get_position(self):
        return self.position
    
    def get_legal_moves(self, board):
        moves = []
        if (board.check_if_empty([self.position[0],self.position[1]+1]) or
            board.check_if_opponent([self.position[0],self.position[1]+1])):
            moves += [self.position[0],self.position[1]+1],

        if (board.check_if_empty([self.position[0]+1,self.position[1]+1]) or
            board.check_if_opponent([self.position[0]+1,self.position[1]+1])):
            moves += [self.position[0]+1,self.position[1]+1],

        if (board.check_if_empty([self.position[0]+1,self.position[1]]) or
            board.check_if_opponent([self.position[0]+1,self.position[1]])):
            moves += [self.position[0]+1,self.position[1]],

        if (board.check_if_empty([self.position[0]+1,self.position[1]-1]) or
            board.check_if_opponent([self.position[0]+1,self.position[1]-1])):
            moves += [self.position[0]+1,self.position[1]-1],

        if (board.check_if_empty([self.position[0],self.position[1]-1]) or
            board.check_if_opponent([self.position[0],self.position[1]-1])):
            moves += [self.position[0],self.position[1]-1],

        if (board.check_if_empty([self.position[0]-1,self.position[1]-1]) or
            board.check_if_opponent([self.position[0]-1,self.position[1]-1])):
            moves += [self.position[0]-1,self.position[1]-1],

        if (board.check_if_empty([self.position[0]-1,self.position[1]]) or
            board.check_if_opponent([self.position[0]-1,self.position[1]])):
            moves += [self.position[0]-1,self.position[1]],

        if (board.check_if_empty([self.position[0]-1,self.position[1]+1]) or
            board.check_if_opponent([self.position[0]-1,self.position[1]+1])):
            moves += [self.position[0]-1,self.position[1]+1],

        self.owner.filter_checks(self.posiiton, moves)
        return moves

    def __repr__(self):
        return self.owner.color.name+"P"


