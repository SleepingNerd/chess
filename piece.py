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

# Constants to represent 


COLOR_TO_WORD = ["White", "Black"]
CH_TO_CASTLES = {"Q":[WHITE, 0],"K":[WHITE, 1], "q":[BLACK, 0], "k":[BLACK, 1]}
CH_TO_PIECE = {"p": Piece(BLACK, PAWN), "r": Piece(BLACK, ROOK), "n": Piece(BLACK, KNIGHT), "b": Piece(BLACK, BISHOP), "k": Piece(BLACK, KING), "q": Piece(
    BLACK, QUEEN), "P": Piece(WHITE, PAWN), "R": Piece(WHITE, ROOK), "N": Piece(WHITE, KNIGHT),  "B": Piece(WHITE, BISHOP),  "K": Piece(WHITE, KING), "Q": Piece(WHITE, QUEEN)}
CH_TO_COLOR = {"w": WHITE, "b": BLACK}

CH_TO_INDEX = {"a":0 , "b": 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h": 7}

PIECE_TO_MOVEMENT = {}
LINEAR_MOVERS = 
SINGULAR MOVERS = 
