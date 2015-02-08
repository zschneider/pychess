from pieces import Piece

class Board:
    """Represents a standard 8x8 chess board."""
    def __init__(self):
        self.board = []
        for x in range(0, 64):
            self.board += None,

    def xy_to_num(self, xy):
        """Converts an xy coordinate to the space in array."""
        return xy[0] + xy[1]*8

    def fails_bounds_check(self, position):
        if position[0] > 7 or position[0] < 0:
            return True
        if position[1] > 7 or position[1] < 0:
            return True

    def check_if_empty(self, position):
        if self.fails_bounds_check(position):
            return False
        if self.board[self.xy_to_num(position)] == None:
            return True
        else:
            return False

    def check_if_opponent(self, position, owner):
        p = self.get_piece_at_position(position)
        if p:
            return p.owner != owner
        return False

    def add_to_board(self, piece):
        pos = piece.position
        if self.check_if_empty(pos):
            self.board[self.xy_to_num(pos)] = piece

    def get_piece_at_position(self, position):
        if self.fails_bounds_check(position):
            return False
        return self.board[self.xy_to_num(position)]

    def is_check(self):
        """Checks if a player is in check."""
        

    def __repr__(self):
        rep =  "   _     _     _     _     _     _     _     _  \n"
        for y in range(0, 8):
            rep += "| "
            for row in range(0, 8):
                space = self.board[y*8 + row]
                if space:
                    rep += " " + str(space) + " | "
                else:
                    rep += "    | "
            rep += "\n"
            rep += "|  _  |  _  |  _  |  _  |  _  |  _  |  _  |  _  |\n"
        return rep


        



