#
class Piece():
    def __init__(self, color, type):
        self.type = type
        self.color = color



# Constants to represent piece (and pawn) values in a human readable way
WHITE = 0
BLACK = 1

ROOK = 0
KNIGHT = 1
BISHOP = 2
QUEEN = 3
KING = 4

PAWN = 5
EMPTY = 0


CH_TO_PIECE = {"p": Piece(BLACK, PAWN), "r": Piece(BLACK, ROOK), "n": Piece(BLACK, KNIGHT), "b": Piece(BLACK, BISHOP), "k": Piece(BLACK, KING), "q": Piece(
    BLACK, QUEEN), "P": Piece(WHITE, PAWN), "R": Piece(WHITE, ROOK), "N": Piece(WHITE, KNIGHT),  "B": Piece(WHITE, BISHOP),  "K": Piece(WHITE, KING), "Q": Piece(WHITE, QUEEN)}
CH_TO_COLOR = {"w": WHITE, "b": BLACK}
