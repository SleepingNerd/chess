import piece
from engine import BoardData, Coordinate, get_linear_moves, get_singular_moves, is_piece, is_color, is_capture, in_check, keep_applying
from engine import Move, DoubleHop, Capture, EnPassant, Promotion, QueenSideCastles, KingSideCastles
import piece

# NOTE: [y, x] when representing a movement_pattern

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

# Y for each color on wich the pawns should start 
PAWN_DOUBLEHOP_Y = {WHITE: 1, BLACK: 6}

# Double hop movement for each color
PAWN_DOUBLEHOP_MOVEMENT = {WHITE: [2, 1], BLACK: [-2, 1]}

class Piece():
    def __init__(self, color):
        self.color = color

class LinearPiece(Piece):
    movement_patterns = []
    def get_moves(self, board_data: BoardData, origin: Coordinate):
        return get_linear_moves(board_data, origin, self.movement_patterns)
    
class SingularPiece(Piece):
    movement_patterns = []
    def get_moves(self, board_data: BoardData, origin: Coordinate):
        return get_singular_moves(board_data, origin, self.movement_patterns)
#
class ExceptionPiece(Piece):
    """
    Is meant to be TOTALLY overwritten ->
    """
    def get_moves(self, board_data: BoardData, origin: Coordinate):
        pass
    
class Empty(Piece):
    movement_patterns = []
    type =  EMPTY
    
class Queen(LinearPiece):
    movement_patterns = [[1, 0], [1,1]]
    type = QUEEN
    
class Rook(LinearPiece):
    movement_patterns = [[1,0]]
    type = ROOK

class Bishop(LinearPiece):
    movement_patterns = [[1,1]]
    type = BISHOP
     
class Knight(SingularPiece):
    movement_patterns = [[2,1]]
    type = KNIGHT
    
class King(ExceptionPiece):
    type = KING
    
    
    def get_moves(self, board_data: BoardData, origin: Coordinate):
        moves = get_linear_moves(board_data, origin, self.movement_patterns)
        if in_check(board_data, origin, False) == False:
                    # QUEENSIDE
                    if board_data.castles[board_data.active][0] and not in_check(board_data, Coordinate(origin.y, origin.x-1), False):
                        # If it's not blocked   and the left square isn't in check
                        if  len(keep_applying(board_data, origin, [0,-1], [0, 8])) == 3:
                            moves.append(QueenSideCastles(origin, Coordinate(origin.y, 1)))
                            

                    if board_data.castles[board_data.active][1] and not in_check(board_data, Coordinate(.y, origin.x+1), False):
                        # If no pieces block
                        if  len(keep_applying(board_data, origin, [0,1], [0, 8])) == 2:
                            moves.append(KingSideCastles(origin, Coordinate(origin.y, 6)))
                            
class Pawn(ExceptionPiece):
    movement_patterns = {WHITE: [1, 0], BLACK:[-1, 0]}
    type = piece.PAWN
    def __init__(self, color, type):
        super().__init__(color)
    def get_moves(self, board_data: BoardData, origin: Coordinate):
        target_y = origin.y + self.movement_patterns[board_data.active][0]    
        moves = []
           
        # If he can move forward by 1
        if is_piece(board_data.board, Coordinate(target_y,  origin.x), piece.EMPTY):
            moves.append(Move(origin, Coordinate(target_y, origin.x)))
            
            # If he's on start position
            if origin.y == piece.PAWN_DOUBLEHOP_POS[board_data.active]:
                double_hop_target = Coordinate(origin.y+piece.PAWN_DOUBLEHOP_MOVEMENT[board_data.active][0], origin.x)
                if is_piece(board_data.board, Coordinate(target_y,  origin.x), piece.EMPTY):
                    moves.append(DoubleHop(origin, double_hop_target))
                    
            
        # If he can capture left and en passant
        target_x = origin.x+1

        # If the target isn't off screen 
        if target_x < 8:
            state = is_capture(board_data, Coordinate(target_y, origin.x+1))
            
            if state == piece.CAPTURE:
                moves.append(Capture(origin, Coordinate(target_y, target_x)))
                
            elif state == piece.EN_PASSANT:
                moves.append(EnPassant(origin, Coordinate(target_y, target_x), Coordinate(origin.y, target_x)))
                
                
        # Capture right and en passant
        target_x = origin.x-1
        # If the target isn't off screen 
        if not target_x < 0:
            state = is_capture(board_data, Coordinate(target_y, origin.x+1))
            
            if state == piece.CAPTURE:
                moves.append(Capture(origin, Coordinate(target_y, target_x)))
                
            elif state == piece.EN_PASSANT:
                moves.append(EnPassant(origin, Coordinate(target_y, target_x), Coordinate(origin.y, target_x)))

        # If pawn has reached promotion square
        if target_y == piece.PAWN_PROMOTE_POS[board_data.active]:
            promotion_moves = []
            for move in moves:
                for i in (piece.ROOK, piece.BISHOP, piece.KNIGHT, piece.QUEEN):
                    promotion_moves.append(Promotion(move.origin, move.dest, i)) 
            return promotion_moves
        return moves