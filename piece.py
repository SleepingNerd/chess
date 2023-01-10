from math import  inf

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
# 0 For queenside- 1 for kingside
CH_TO_CASTLES = {"Q":[WHITE, 0],"K":[WHITE, 1], "q":[BLACK, 0], "k":[BLACK, 1]}

CH_TO_COLOR = {"w": WHITE, "b": BLACK}

CH_TO_INDEX = {"a":0 , "b": 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h": 7}

CASTLE_ROW = {WHITE: 0, BLACK: 7}
# Q FIRST A
CASTLES_SQUARE = {0: [0, 1] ,1:[6, 7]}
ROOK_X_TO_CASTLES = {0: 0, 7:1}
KING_X_AFTER_CASTLES = {0: 2, 1:6}

# Y IS ALWAYS FIRST
PIECE_TO_MOVEMENT = {ROOK: [[1, 0]], KNIGHT: [[1,2]], BISHOP: [[1,1]], QUEEN:[[1, 0], [1,1]], KING: [[1, 0], [1,1]]}
LINEAR_MOVERS = [ROOK, BISHOP, QUEEN]
SINGULAR_MOVERS = [KING, KNIGHT]
PAWN_MOVEMENT = {WHITE: [1, 0], BLACK:[-1, 0]}
PAWN_DOUBLEHOP_MOVEMENT = {WHITE: [2, 1], BLACK: [-2, 1]}
PAWN_DOUBLEHOP_POS = {WHITE: 1, BLACK: 6}
PAWN_PROMOTE_POS = {WHITE: 7, BLACK: 0}

# COLOR TO T
ACTIVE_TO_INACTIVE = {BLACK: WHITE, WHITE: BLACK}

# Bot stuff
PIECE_TO_CLASSICAL_VALUE = {ROOK: 5, QUEEN: 10, PAWN:1, BISHOP: 3, KNIGHT:3, KING: 100}

# 



#  CONSTANTS TO REPRESENT function returns i guess
NOTHING = 0
EN_PASSANT = 1
CAPTURE = 2
BLOCKED = 3


# Borders idk
ZERO_BORDER = 100
