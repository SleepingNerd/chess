import piece
import copy
from typing import Optional
import time
import numpy as np

class Piece():
    def __init__(self, color):
        self.color = color
    def get_moves():
        raise SyntaxError("get_moves from Piece is supposed to be overwritten, don't call it directly!")
    
class Void(Piece):
    movement_patterns = []
    type =  piece.EMPTY
    def get_moves():
        return []
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
    type =  piece.EMPTY
    
class Queen(LinearPiece):
    movement_patterns = [[1, 0], [1,1]]
    type = piece.QUEEN
    
class Rook(LinearPiece):
    movement_patterns = [[1,0]]
    type = piece.ROOK

class Bishop(LinearPiece):
    movement_patterns = [[1,1]]
    type = piece.BISHOP
     
class Knight(SingularPiece):
    movement_patterns = [[2,1]]
    type = piece.KNIGHT
    
class King(ExceptionPiece):
    type = piece.KING
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
    movement_patterns = {piece.WHITE: [1, 0], piece.piece.BLACK:[-1, 0]}
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
    
CH_TO_PIECE = {"p": Pawn(piece.BLACK), "r": Rook(piece.BLACK), "n": Knight(piece.BLACK), "b": Bishop(piece.BLACK), "k": King(piece.BLACK), "q": Queen(
    piece.BLACK), "P": Pawn(piece.WHITE), "R": Rook(piece.WHITE), "N": Knight(piece.WHITE),  "B": Bishop(piece.WHITE),  "K": King(piece.WHITE), "Q": Queen(piece.WHITE)}

def flatten(twodlist) -> list:
    result = []
    for lis in twodlist:
        # If "list" object can return an iterable
        if hasattr(lis, '__iter__'):
            for value in lis:
                result.append(value)
        else:
            result.append(lis)
    return result


def debug_time(func):
    def wrapper(*args, **kwargs):
        first = time.time()
        value = func(*args, **kwargs)
        print(first - time.time())
        return value
    return wrapper
    
class Coordinate():
    def __init__(self, y, x):
        self.y = y
        self.x = x

class Move():
    def __init__(self, origin: Coordinate, dest:Coordinate):
        self.origin = origin
        self.dest   = dest
class Capture(Move):
    pass
class DoubleHop(Move):
    pass
class Promotion(Move):
    def __init__(self, origin: Coordinate, dest:Coordinate, piece_type:int):
        super().__init__(origin, dest)
        self.type = piece_type
class EnPassant(Move):
    def __init__(self, origin: Coordinate, dest:Coordinate, captured_pawn:Coordinate):
        super().__init__(origin, dest)
        self.captured = captured_pawn
class Replace():
    def __init__(self, dest:Coordinate, dest_piece: piece.Piece):
        self.dest   = dest
        self.piece = dest_piece
        
class Castles():
    def __init__(self, origin: Coordinate,  dest:Coordinate):
        self.origin = origin
        self.dest   = dest
    
class QueenSideCastles(Castles):
    def __init__(self,  origin: Coordinate,  dest:Coordinate):
        super().__init__(origin, dest)

        
class KingSideCastles(Castles):
    def __init__(self,  origin: Coordinate,  dest:Coordinate):
        super().__init__(origin, dest)
        
class BoardData():
    """
    Represents all data of a chess board
    """
    def __init__(self):
        self.empty_board()

    def empty_board(self):
        self.board = np.zeros((8,8), dtype=Piece)
        # Empty board
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j] = Void(-1)

        # Reset other fields
        self.active  = piece.piece.WHITE
        # Q then K
        self.castles = [[False, False], [False, False]]
        self.reset_en_passant()
        self.halfmoves = 0
        
    def reset_en_passant(self):
        self.en_passant = Coordinate(-100, -100)
    def apply_move(self, move: Move):
        # If it's a double hop set en passant square
        if isinstance(move, DoubleHop):
            self.en_passant = Coordinate(move.origin.y + piece.PAWN_MOVEMENT[self.active][0], move.origin.x)
        else:
            if isinstance(move, EnPassant):
                self.board[move.captured.y][move.captured.x] = piece.EMPTY
            self.reset_en_passant()
            
        # Castles will become impossible if that rook is taken, that rook moves, or the king moves
        if self.board[move.origin.y][move.origin.x].type == piece.KING:
            self.castles[self.active] = [False, False]
        elif self.board[move.origin.y][move.origin.x].type == piece.ROOK:
            if move.origin.x in piece.ROOK_X_TO_CASTLES.keys() and move.origin.y == piece.CASTLE_ROW[self.active]:
                self.castles[self.active][piece.ROOK_X_TO_CASTLES[move.origin.x] ]= False
        if move.dest.y == piece.CASTLE_ROW[piece.ACTIVE_TO_INACTIVE[self.active]] and move.origin.x in piece.ROOK_X_TO_CASTLES.keys():
            self.castles[piece.ACTIVE_TO_INACTIVE[self.active]][piece.ROOK_X_TO_CASTLES[move.origin.x]] = False
        
        # Just apply the move
        if isinstance(move, Move):
            self.board[move.dest.y][move.dest.x] = self.board[move.origin.y][move.origin.x]
            self.board[move.origin.y][move.origin.x] = piece.EMPTY
            
        if isinstance(move, KingSideCastles):
            self.board[move.origin.y][6] = piece.Piece(self.active, piece.KING)
            self.board[move.origin.y][5] = piece.Piece(self.active, piece.ROOK)
            self.board[move.origin.y][move.origin.x] = piece.EMPTY
            self.board[move.origin.y][7] = piece.EMPTY
            self.castles[self.active][1] = True

        elif isinstance(move, QueenSideCastles):
            self.board[move.origin.y][2] = piece.Piece(self.active, piece.KING)
            self.board[move.origin.y][3] = piece.Piece(self.active, piece.ROOK)
            self.board[move.origin.y][move.origin.x] = piece.EMPTY
            self.board[move.origin.y][0] = piece.EMPTY
            self.castles[self.active][0] = True
                    
        #  If it could promote
        if isinstance(move, Promotion):
            self.board[move.dest.y][move.dest.x].type = move.type
            
        # Flip color
        self.active = piece.ACTIVE_TO_INACTIVE[self.active]


def readfen(fen: str) -> BoardData:
    """
    Returns a BoardData object out of a fen string
    """
    # BoardData object
    board_data = BoardData()

    # Split fen
    fen = fen.split(" ")
    # Split position into ranks
    fen[0] = fen[0].split("/")

    # Position
    for rank in range(0, len(fen[0])):
        file = 0
        for ch in fen[0][rank]:
            if file > 7:
                break
            elif ch in piece.CH_TO_PIECE:
                board_data.board[len(fen[0])- 1 -rank][file] = piece.Piece(piece.CH_TO_PIECE[ch].color, piece.CH_TO_PIECE[ch].type) 
                file += 1
            else:
                file += int(ch)

    # Active color
    board_data.active = piece.CH_TO_COLOR[fen[1]]

    # Castles right
    for ch in fen[2]:
        if ch != '-':
            i = piece.CH_TO_CASTLES[ch]
            board_data.castles[i[0]][i[1]] = True
            

    # If there's a possible en passant target
    if fen[3] != '-':
        board_data.en_passant = Coordinate(int(fen[3][1])-1, piece.CH_TO_INDEX[fen[3][0]])

    # Halfmove clock
    board_data.halfmoves = int(fen[4])

    #
    return board_data


def every_direction(func, *args):
    def wrapper(board_data: BoardData, origin: Coordinate, movement_patterns: list[tuple[int, int]]):
        
        combs = [[1, -1, 1, -1], [1, -1, -1, 1]]
        moves = []
        # For every movement pattern
        for pattern in movement_patterns:
            # Reversed
            for i in range(0,2):
                # For every combination of negative and positive
                
                start = 0
                if pattern[0] == 0 or pattern[1]  == 0:
                    start = 2
                    
                for j in range(start, 4):
                    
                    moves.append(func(board_data, origin, (pattern[0]*combs[0][j], pattern[1]*combs[1][j])))

                #
                if pattern[0] == pattern[1]:
                    break;
                # Reverse
                pattern = [pattern[1], pattern[0]]
                
        return flatten(moves)
    
    return wrapper

# For bishop, king (not castles tho), queen, rook
@every_direction
def get_linear_moves(board_data : BoardData, origin: Coordinate, movement_pattern: tuple[int, int]) -> list[Move]:
    return keep_applying(board_data, origin, movement_pattern)

#  Horse, king,
@every_direction
def get_singular_moves(board_data: BoardData, origin: Coordinate,movement_pattern: tuple[int, int]) -> list[Move]:
    dest = Coordinate(origin.y + movement_pattern[0], origin.x + movement_pattern[1])
    if dest.y < 8 and  dest.y > -1 and  dest.x < 8 and dest.x > -1:
        state = is_capture(board_data, dest)
        if  state == piece.BLOCKED:
            return []
        elif state == piece.CAPTURE:
            return [Capture(origin, dest)]
        else:
            return  [Move(origin, dest)]
    else:
        return []

# Checks if inactive color is in check
def in_check(board_data : BoardData, origin: Coordinate, check_inactive=True) -> bool:
    original_color = board_data.active
    if check_inactive:
        # Become color that just moved or might be in check
        board_data.active = piece.ACTIVE_TO_INACTIVE[board_data.active]

    # Collect rook moves from king
    rook_moves   =  flatten(get_linear_moves(board_data, origin, piece.PIECE_TO_MOVEMENT[piece.ROOK]))
  
    # If the dest of one of those moves is a rook or queen
    if is_dest(board_data, rook_moves, [piece.ROOK, piece.QUEEN]):
        return True

    bishop_moves =  get_linear_moves(board_data, origin, piece.PIECE_TO_MOVEMENT[piece.BISHOP])
    if is_dest(board_data, bishop_moves, [piece.BISHOP, piece.QUEEN]):
        return True

    knight_moves =  get_singular_moves(board_data, origin, piece.PIECE_TO_MOVEMENT[piece.KNIGHT])
    if is_dest(board_data, knight_moves, [piece.KNIGHT]):
        return True
    
    king_moves = get_singular_moves(board_data, origin, piece.PIECE_TO_MOVEMENT[piece.KING])
    if is_dest(board_data, king_moves, [piece.KING]):
            return True
    
    # Become color that just moved or might be in check
    opposing_color = piece.ACTIVE_TO_INACTIVE[board_data.active]
    board_data.active = original_color
    target_y = origin.y - piece.PAWN_MOVEMENT[opposing_color][0]
    
    if is_piece(board_data, Coordinate(target_y, origin.x + 1), piece.PAWN) and is_color(board_data, Coordinate(target_y, origin.x + 1), opposing_color):
        return True
    if is_piece(board_data, Coordinate(target_y, origin.x - 1), piece.PAWN) and is_color(board_data, Coordinate(target_y, origin.x - 1), opposing_color):
        return True
    return False

def has_no_moves(board_data : BoardData) -> bool:
    if get_moves(board_data) ==[]:
        return True
    return False
    

def in_mate(board_data : BoardData, origin: Coordinate, check_inactive=True) -> bool:
    if in_check(board_data, origin, check_inactive) and get_moves(board_data) == []:
        return True





def is_dest(board_data : BoardData, moves: list[Move], target: list[int]) -> bool:
    for move in moves:
        if board_data.board[move.dest.y][move.dest.x] != piece.EMPTY:
            if board_data.board[move.dest.y][move.dest.x].type in target:
                return True
    return False

def is_piece(board_data: BoardData, pos: Coordinate, piece: int):
    try:
        if board_data.board[pos.y][pos.x].type == piece:
            return True
    except:
        pass
    return False

def is_color(board_data: BoardData, pos: Coordinate, color: int):
    try:
        if board_data.board[pos.y][pos.x].color == color:
            return True
    except:
        pass
    return False

def  keep_applying_for_check(board_data: BoardData, start: Coordinate, movement_pattern: tuple[int, int], x_limits = [-1, 8], y_limits = [-1, 8]):
    y = start.y + movement_pattern[0]
    x = start.x  + movement_pattern[1]
    while y < y_limits[1] and y > y_limits[0] and x < x_limits[1] and x > x_limits[0]:
        if in_check(board_data, Coordinate(y, x)):
             return True
        x +=movement_pattern[1]
        y +=movement_pattern[0]
    return False

def  keep_applying(board_data: BoardData, start: Coordinate, movement_pattern: tuple[int, int], x_limits = [-1, 8], y_limits = [-1, 8]):

    moves = []
    y = start.y + movement_pattern[0]
    x = start.x  + movement_pattern[1]
    while y < y_limits[1] and y > y_limits[0] and x < x_limits[1] and x > x_limits[0]:
        state = is_capture(board_data, Coordinate(y,x))
        if state == piece.BLOCKED:
            return moves
        elif state == piece.CAPTURE:
            moves.append(Capture(start, Coordinate(y, x)))
            return moves
        else:
            moves.append(Move(start, Coordinate(y, x)))
        x +=movement_pattern[1]
        y +=movement_pattern[0]
    return moves

def on_board(x: int) -> bool:
    if x < 0 or x >7:
        return False
    return True

# Returns True if pos, is a piece not of active color
def is_capture(board_data: BoardData, pos: Coordinate):
    try:
        if board_data.board[pos.y][pos.x] != piece.EMPTY:
            if board_data.board[pos.y][pos.x].color != board_data.active:
                return piece.CAPTURE
            else:
                return piece.BLOCKED
        elif pos.y ==  board_data.en_passant.y and pos.x ==  board_data.en_passant.x:
            return piece.EN_PASSANT
    except IndexError:
        pass
    return piece.NOTHING

# Finds active king
def find_king(board_data: BoardData) -> Optional[Coordinate]:
    for i in range(0, 8):
        for j in range(0, 8):
            if board_data.board[i][j] != piece.EMPTY:
                if board_data.board[i][j].type == piece.KING and  board_data.board[i][j].color == board_data.active:
                    return Coordinate(i, j)
    return None
def contains_piece(board_data: BoardData, lis : list[Move], piece: int):
    for move in lis:
        if board_data[move.origin.y][move.origin.x] == piece:
            return True
    return False


            
        




def get_piece_moves(board_data: BoardData, pos: Coordinate) -> list[Coordinate]:
    moves = []
    p_type = board_data.board[pos.y][pos.x].type

    # If piece is of linear movement type, bishop, queen, rook
    if  p_type in piece.LINEAR_MOVERS:
        moves.append(get_linear_moves(board_data, pos, piece.PIECE_TO_MOVEMENT[p_type]))
    # If piece is of singular movement type, king horse
    elif p_type in piece.SINGULAR_MOVERS:
        moves.append(get_singular_moves(board_data, pos, piece.PIECE_TO_MOVEMENT[p_type]))

    # If piece is a pawn
    elif p_type == piece.PAWN:
        target_y = pos.y+piece.PAWN_MOVEMENT[board_data.active][0]    
        pawn_moves = []
           
        # If he can move forward
        if board_data.board[target_y][pos.x] == piece.EMPTY:
            pawn_moves.append(Move(pos, Coordinate(target_y, pos.x)))
            # If he can double hop
            if pos.y == piece.PAWN_DOUBLEHOP_POS[board_data.active]:
                target_cord = Coordinate(pos.y+piece.PAWN_DOUBLEHOP_MOVEMENT[board_data.active][0], pos.x)
                if board_data.board[target_cord.y][target_cord.x]== piece.EMPTY:
                    moves.append(DoubleHop(pos,target_cord))
            
        # If he can capture left and en passant
        x_dest = pos.x+1
        state=is_capture(board_data, Coordinate(target_y, pos.x+1))
        if x_dest < 8:
            if state == piece.CAPTURE:
                pawn_moves.append(Capture(pos, Coordinate(target_y, x_dest)))
            elif state == piece.EN_PASSANT:
                moves.append(EnPassant(pos, Coordinate(target_y, x_dest), Coordinate(pos.y, x_dest)))
                
        # Capture right and en passant
        x_dest = pos.x-1
        if not x_dest < 0:
            state=is_capture(board_data, Coordinate(target_y, x_dest))
            
            if state == piece.CAPTURE:
                pawn_moves.append(Capture(pos, Coordinate(target_y, x_dest)))
            elif state == piece.EN_PASSANT:
                moves.append(EnPassant(pos, Coordinate(target_y, x_dest), Coordinate(pos.y, x_dest)))
                
        # If pawn has reached promotion square
        if target_y == piece.PAWN_PROMOTE_POS[board_data.active]:
            for move in pawn_moves:
                for i in (piece.ROOK, piece.BISHOP, piece.KNIGHT, piece.QUEEN):
                    moves.append(Promotion(move.origin, move.dest, i))
        else:
            moves.append(pawn_moves)
                    
    # Castles
    if p_type == piece.KING:
        # If he's not in check
        if in_check(board_data, pos, False) == False:
            # QUEENSIDE
            if board_data.castles[board_data.active][0] and not in_check(board_data, Coordinate(pos.y, pos.x-1), False):
                # If it's not blocked   and the left square isn't in check
                if  len(keep_applying(board_data, pos, [0,-1], [0, 8])) == 3:
                    moves.append(QueenSideCastles(pos, Coordinate(pos.y, 1)))
                    

            if board_data.castles[board_data.active][1] and not in_check(board_data, Coordinate(pos.y, pos.x+1), False):
                # If no pieces block
                if  len(keep_applying(board_data, pos, [0,1], [0, 8])) == 2:
                    moves.append(KingSideCastles(pos, Coordinate(pos.y, 6)))



            
        
        

    # Check for checks
    moves = flatten(moves)
    legal_moves = []
    king_origin = find_king(board_data)
    for move in moves:
        kpos = king_origin
        if board_data.board[move.origin.y][move.origin.x].type == piece.KING:
            kpos = Coordinate(move.dest.y, move.dest.x)
            if isinstance(move, Castles):
                if isinstance(move, QueenSideCastles):
                    kpos_x = piece.KING_X_AFTER_CASTLES[0]
                                      
                else:
                    kpos_x = piece.KING_X_AFTER_CASTLES[1]
                kpos = Coordinate(kpos.y, kpos_x)

        if in_check(apply_move(board_data,move), kpos) == False:
            legal_moves.append(move)
        
    return legal_moves






def apply_move(board_data: BoardData, move) -> BoardData:
    temp = copy.deepcopy(board_data)
    temp.apply_move(move)
    return temp

def is_move_legal(board_data: BoardData, move: Move):
    if board_data[move.origin.y][move.origin.x] in piece.LINEAR_MOVERS:
        if move in get_linear_moves(board_data, cord):
            return True

    elif board_data[move.origin.y][move.origin.x] in piece.SINGULAR_MOVERS:
        pass
    return False


def get_moves(board_data: BoardData):
    moves = []
    # Iterate through all pieces from the active color
    for y in range(0, len(board_data.board[0])):

            for x in range(0, len(board_data.board[1])):
                if board_data.board[y][x] != piece.EMPTY:
                    # If piece is of active color
                    if board_data.board[y][x].color == board_data.active:
                        moves.append(get_piece_moves(board_data, Coordinate(y, x)))

    return flatten(moves)
