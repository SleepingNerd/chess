import piece
import copy

def flatten( twodlist) -> list:
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
        self.en_passant = None
        self.halfmoves = 0
    def apply_move(self, move: Move):
        if isinstance(move, Move):
            self.board[move.dest.y][move.dest.x] = self.board[move.origin.y][move.origin.x]
            self.board[move.origin.y][move.origin.x] = piece.EMPTY
        elif isinstance(move, Replace):
            pass
       
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
def get_linear_moves(board_data: BoardData, cord: Coordinate) -> list[Coordinate]:
    return []

#  Horse, king
def get_singular_moves(board_data: BoardData, cord: Coordinate) -> list[Move]:
    return []

# Checks if a move is blocked (by a other piece) 
def is_blocked(board_data: BoardData, move: Move, moving_pattern: tuple[int, int]):
    # Keep applying moving_pattern until active or non active piece is 
    for y in range(move.origin.y+moving_pattern[0], move.dest.y+1, moving_pattern[0]):
        #
        for x in range(move.origin.y+moving_pattern[1], move.dest.x+1, moving_pattern[1]):
            if board_data.board[y][x] != piece.EMPTY:
                # If piece is blocked by an active color
                if board_data.board[y][x].color == board_data.active:
                    return piece.BLOCKED_BY_ACTIVE
                # Elif piece is blocked by an inactive color 
                elif board_data.board[y][x].color == board_data.active:
                    if y == move.dest.y and x == move.dest.x:
                        return piece.CAPTURE
                    else: 
                        return piece.BLOCKED_BY_INACTIVE
            else:
                if y == move.dest.y and x == move.dest.x:
                        return piece.NOT_BLOCKED
                    
                
    
    # If it was impossible for that move to happen
    return piece.MOVING_PATTERN_MISTAKE
                 

        
        

    

    
    

def get_piece_moves(board_data: BoardData, pos: Coordinate) -> list[Coordinate]:
    moves = []
    # If piece is of linear movement type
    if  board_data.board[pos.y][pos.x].type in piece.LINEAR_MOVERS:

        moves.append(get_linear_moves(board_data, Coordinate(pos.y, pos.x)))

    # If piece is of singular movement type
    elif board_data.board[pos.y][pos.x].type in piece.SINGULAR_MOVERS:
        moves.append(get_singular_moves(board_data, Coordinate(pos.y, pos.x)))
            
    # If piece is a pawn
    elif board_data.board[pos.y][pos.x].type == piece.PAWN:
        target_y = pos.y+piece.PAWN_MOVEMENT[board_data.active][0] 
        # If he can move forward
        if board_data.board[target_y][pos.x] == piece.EMPTY:
            moves.append(Coordinate(target_y, pos.x))
            # If he can double hop
            if pos.y == piece.PAWN_DOUBLEHOP_POS[board_data.active]:
                target_cord = Coordinate(pos.y+piece.PAWN_DOUBLEHOP_MOVEMENT[board_data.active][0], pos.x)
                if board_data.board[target_cord.y][target_cord.x]== piece.EMPTY:
                    moves.append(target_cord)
        # If he can capture left

        
                    
                    
            
                
                    
                    
            
            

    # Castles
    else:
        pass
    
    return flatten(moves)
        





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
