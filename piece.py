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

# Y IS ALWAYS FIRST
PIECE_TO_MOVEMENT = {ROOK: [[1, 0]], KNIGHT: [[1,2]], BISHOP: [[1,1]], QUEEN:[[1, 0], [1,1]], KING: [[1, 0], [1,1]]}
LINEAR_MOVERS = [ROOK, BISHOP, QUEEN]
SINGULAR_MOVERS = [KING, KNIGHT]
PAWN_MOVEMENT = {WHITE: [1, 0], BLACK:[-1, 0]}
PAWN_DOUBLEHOP_MOVEMENT = {WHITE: [2, 1], BLACK: [-2, 1]}
PAWN_DOUBLEHOP_POS = {WHITE: 1, BLACK: 6}

# COLOR TO T
ACTIVE_TO_INACTIVE = {BLACK: WHITE, WHITE: BLACK}

#  CONSTANTS TO REPRESENT 
BLOCKED_BY_ACTIVE = 0
BLOCKED_BY_INACTIVE = 1
CAPTURE = 2
NOT_BLOCKED = 3
MOVING_PATTERN_MISTAKE = 4



