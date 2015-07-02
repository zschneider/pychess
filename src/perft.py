"""Perft test to verify move generation is correct."""
from copy import deepcopy
from time import time

from engine import Game, Color


class Perft:
    
    def __init__(self):
        self.game = Game()
        self.game.new_game()

    def perft(self, board, curr_player, depth):
        """Perft function that recursively checks nodes.
        Intended to be compared to predetermined values.
        ply 2 search time: .567
        ply 3 search time: 12.1
        ply 4 search time: 281.54"""
        nodes = 0

        if curr_player.color is Color.W:
            num_moves = board.get_all_legal_moves(self.game.white)
        else:
            num_moves = board.get_all_legal_moves(self.game.black)

        if depth == 1:
            return len(num_moves)

        for move in num_moves:
            new_board = deepcopy(board)
            new_piece = new_board.get_piece_at_position(move[0].position)
            new_board.make_move(new_piece, move[1])

            if curr_player == self.game.white:
                nodes += self.perft(new_board, self.game.black, depth-1)
            else:
                nodes += self.perft(new_board, self.game.white, depth-1)

        return nodes

    def run_perft(self, depth):
        """Perft wrapped in a timer."""
        start = time()
        done = self.perft(self.game.board, self.game.current_turn, depth)
        end = time()
        print("Elapsed time for depth " + str(depth) + ": ")
        print(str(end-start))
        return done
