from enum import Enum

class Color(Enum):
	W = 0
	B = 1

class Player():
    def __init__(self,color, board):
        self.color = color
        self.board = board

    def filter_checks(self, position, moves):
        """Checks to see if moving this piece would cause a check."""
