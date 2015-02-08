import board
import pieces
from players import Player, Color

game = board.Board()
white = Player(Color.W, game)
black = Player(Color.B, game)
"""
pawn = pieces.Pawn(white,[1,1])
print "Adding a white pawn at B7"
game.add_to_board(pawn)
print game
print "Possible moves: " + str(pawn.get_legal_moves(game))
print "Adding a black pawn at C6"
pawn2 = pieces.Pawn(black,[2,2])
game.add_to_board(pawn2)
print game
print "Possible moves: " + str(pawn.get_legal_moves(game))
print "Adding a white rook!"
rook = pieces.Rook(white,[1,6])
game.add_to_board(rook)
print game
print "Possible moves: " + str(rook.get_legal_moves(game))
print "Adding a black pawn!"
pawn2 = pieces.Pawn(black,[1,3])
game.add_to_board(pawn2)
print game
print "Possible moves: " + str(rook.get_legal_moves(game))
"""
print "Adding a white bishop"
bishop = pieces.Bishop(white,[5,5])
game.add_to_board(bishop)
print game
print bishop.get_legal_moves(game)
