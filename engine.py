import piece
import copy

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
class Promote(Move):
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

        # Not important for now
        elif isinstance(move, Replace):
            pass
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
                board_data.board[len(fen[0])- 1 -rank][file] = piece.CH_TO_PIECE[ch]
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



# For bishop, king (not castles tho), queen, rook
def get_linear_moves(board_data: BoardData, cord: Coordinate, movement_patterns: list[tuple[int, int]]) -> list[Coordinate]:
    moves = []
    # For every pattern
    for pattern in movement_patterns:
        # For index
        for n in pattern(-1)
                
                
                
                
    return flatten(moves)
                
                
            
        
#  Horse, king
def get_singular_moves(board_data: BoardData, cord: Coordinate) -> list[Move]:
    return []

def  keep_applying(board_data: BoardData, start: Coordinate, movement_pattern: tuple[int, int]):    
    moves = []
    y = start.y
    x = start.x
    while y < 8 and y > 0:
        y +=movement_pattern[0]
        while x < 8 and x > 0:
            x +=movement_pattern[0]
            state = is_capture(board_data, Coordinate(y,x))
            if state == piece.BLOCKED:
                break;
            elif state == piece.CAPTURE:
                moves.append(Capture(start, Coordinate(y, x)))
            else:
                moves.append(Move(start, Coordinate(y, x)))
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

def get_piece_moves(board_data: BoardData, pos: Coordinate) -> list[Coordinate]:
    moves = []
    # If piece is of linear movement type, bishop, queen, rook
    if  board_data.board[pos.y][pos.x].type in piece.LINEAR_MOVERS:
        moves.append(get_linear_moves(board_data, Coordinate(pos.y, pos.x)))

    # If piece is of singular movement type, king horse
    elif board_data.board[pos.y][pos.x].type in piece.SINGULAR_MOVERS:
        moves.append(get_singular_moves(board_data, Coordinate(pos.y, pos.x)))

    # If piece is a pawn
    elif board_data.board[pos.y][pos.x].type == piece.PAWN:
        target_y = pos.y+piece.PAWN_MOVEMENT[board_data.active][0]
        # If he can move forward
        if board_data.board[target_y][pos.x] == piece.EMPTY:
            moves.append(Move(pos, Coordinate(target_y, pos.x)))
            # If he can double hop
            if pos.y == piece.PAWN_DOUBLEHOP_POS[board_data.active]:
                target_cord = Coordinate(pos.y+piece.PAWN_DOUBLEHOP_MOVEMENT[board_data.active][0], pos.x)
                if board_data.board[target_cord.y][target_cord.x]== piece.EMPTY:
                    moves.append(DoubleHop(pos,target_cord))
        # If he can capture left and en passant
        state=is_capture(board_data, Coordinate(target_y, pos.x+1))
        if state == piece.CAPTURE:
            moves.append(Capture(pos, Coordinate(target_y, pos.x + 1)))
        elif state == piece.EN_PASSANT:
            moves.append(EnPassant(pos, Coordinate(target_y, pos.x + 1), Coordinate(pos.y, pos.x + 1)))
        # Capture right and en passant
        state=is_capture(board_data, Coordinate(target_y, pos.x-1))
        if state == piece.CAPTURE:
            moves.append(Capture(pos, Coordinate(target_y, pos.x -1)))
        elif state == piece.EN_PASSANT:
            moves.append(EnPassant(pos, Coordinate(target_y, pos.x - 1), Coordinate(pos.y, pos.x - 1)))
    # Castles
    else:
        pass

    return moves






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





def in_check(board_data: BoardData, color) -> bool:
    "Returns true, if color's king is in check"
    position = None
    # Find king
    for y in range(0, 7):
        for x in range(0, 7):
            if board_data.board[y][x].type == piece.KING and board_data.board[y][x].color == color:
                position = Coordinate(y, x)
    # Ah man












def get_moves(board_data: BoardData):
    moves = []
    # First of all check if the king is in check


    # Iterate through all pieces from the active color
    for y in range(0, len(board_data.board[0])):

            for x in range(0, len(board_data.board[1])):
                if board_data.board[y][x] != piece.EMPTY:
                    # If piece is of active color
                    if board_data.board[y][x].color == board_data.active:
                        pass


    # Check for castles (or skips if king was in check)

    # Check for en passants (and cancels them out if it results in a check afterwards)

    # Check for promotions, and double pawn movements (and cancels them out if it results in a check afterwards)
    return moves
