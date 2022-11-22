import piece
import copy
from typing import Optional

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
    def __init__(self, origin: Coordinate):
        self.origin = origin
        self.dest = piece.cas
        
class QueenSideCastles():
    def __init__(self):
        pass
class KingSideCastles():
    def __init__(self):
        pass

        

class BoardData():
    """
    Represents all data of a chess board
    """
    def __init__(self):
        self.empty_board()

    def empty_board(self):
        # Empty board
        self.board = []
        for i in range(0, 8):
            self.board.append([])
            for j in range(0, 8):
                self.board[i].append(piece.EMPTY)

        # Reset other fields
        self.active  = piece.WHITE
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

        # Just apply the move
        if isinstance(move, Move):
            self.board[move.dest.y][move.dest.x] = self.board[move.origin.y][move.origin.x]
            self.board[move.origin.y][move.origin.x] = piece.EMPTY
            
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
        combs = [[-1, 1, 1, -1], [1, -1, 1, -1]]
        moves = []
        # For every movement pattern
        for pattern in movement_patterns:
            # Reversed
            for i in range(0,2):
                # For every combination of negative and positive
                for j in range(0, 4):
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
#



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
def in_check(board_data : BoardData, origin: Coordinate) -> bool:

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
    
    target_y = origin.y - piece.PAWN_MOVEMENT[piece.ACTIVE_TO_INACTIVE[board_data.active]][0]
    if is_piece(board_data, Coordinate(target_y, origin.x + 1), piece.PAWN) and is_color(board_data, Coordinate(target_y, origin.x + 1), piece.ACTIVE_TO_INACTIVE[board_data.active]):
        return True
    if is_piece(board_data, Coordinate(target_y, origin.x - 1), piece.PAWN) and is_color(board_data, Coordinate(target_y, origin.x - 1), piece.ACTIVE_TO_INACTIVE[board_data.active]):
        return True
    return False




def is_dest(board_data : BoardData, moves: list[Move], target: list[int]) -> bool:
    for move in moves:
        if board_data.board[move.dest.y][move.dest.x] != piece.EMPTY:
            if board_data.board[move.dest.y][move.dest.x].type in target:
                return True
    return False

def is_piece(board_data: BoardData, pos: Coordinate, piece: int):
    try:
        if p_type == piece:
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

def  keep_applying(board_data: BoardData, start: Coordinate, movement_pattern: tuple[int, int]):
    moves = []
    y = start.y + movement_pattern[0]
    x = start.x  + movement_pattern[1]
    while y < 8 and y > -1 and x < 8 and x > -1:
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
        state=is_capture(board_data, Coordinate(target_y, pos.x+1))
        if state == piece.CAPTURE:
            pawn_moves.append(Capture(pos, Coordinate(target_y, pos.x + 1)))
        elif state == piece.EN_PASSANT:
            moves.append(EnPassant(pos, Coordinate(target_y, pos.x + 1), Coordinate(pos.y, pos.x + 1)))
        # Capture right and en passant
        state=is_capture(board_data, Coordinate(target_y, pos.x-1))
        if state == piece.CAPTURE:
            pawn_moves.append(Capture(pos, Coordinate(target_y, pos.x -1)))
        elif state == piece.EN_PASSANT:
            moves.append(EnPassant(pos, Coordinate(target_y, pos.x - 1), Coordinate(pos.y, pos.x - 1)))
            
        # If pawn has reached promotion square
        if target_y == piece.PAWN_PROMOTE_POS[board_data.active]:
            for move in pawn_moves:
                for i in (piece.ROOK, piece.BISHOP, piece.KNIGHT, piece.QUEEN):
                    moves.append(Promotion(move.origin, move.dest, i))
        else:
            moves.append(pawn_moves)
                    
    # Castles
    if p_type == piece.KING:
        # QUEENSIDE
        if board_data.castles[board_data.active][0]:
            # Check if the dest is actually free ->
            moves.append(QueenSideCastles())
            
        if board_data.castles[board_data.active][1]:
            moves.append(KingSideCastles())

            
        
        

    # Check for checks
    moves = flatten(moves)
    legal_moves = []
    king_origin = find_king(board_data)
    for move in moves:
        kpos = king_origin
        if board_data.board[move.origin.y][move.origin.x].type == piece.KING:
            kpos = Coordinate(move.dest.y, move.dest.x)
        
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


    # Check for castles (or skips if king was in check)

    # Check for en passants (and cancels them out if it results in a check afterwards)
    # Check for promotions, and double pawn movements (and cancels them out if it results in a check afterwards)


    return flatten(moves)
