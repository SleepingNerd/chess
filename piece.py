# Constants to represent piece (and pawn) values in a human readable way
WHITE = 0
BLACK = 1

ROOK = 0
HORSE = 1
BISHOP = 2
QUEEN = 3
KING = 4

PAWN = 5

#
class Piece():
    def __init__(self, color, type):
        self.type = type
        self.color = color
