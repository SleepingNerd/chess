import piece
import copy

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
        self = apply_move(self, move)

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



# For bishop, bishop, and maybe pawn
def get_linear_moves(board_data: BoardData, cord: Coordinate) -> list[Move]:
    movements = piece.PIECE_TO_MOVEMENT[board_data.board[cord.y][cord.x].type]
    moves = []

    # God forgive me for this
    for movement in movements:
        for index in range(0, 2):
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    for y in range(1, 8):
                        y_cord = cord.y+movement[index]*y*i
                        if y_cord < 0 or y_cord > 7:
                            break

                        for x in range(1, 8):
                            x_cord = cord.y+movement[1-index]*x*j
                            if x_cord < 0 or x_cord > 7:
                                break

                            if board_data.board[y_cord][x_cord] != piece.EMPTY:
                                if board_data.board[y_cord][x_cord].color == board_data.active:
                                    y = 100
                                    break

                            moves.append(Move(cord, Coordinate(y_cord, x_cord)))
    return moves

def get_piece_moves(board_data: BoardData, pos: Coordinate) -> list[Move]:
    # If piece is of linear movement type
    if  board_data.board[pos.y][pos.x].type in piece.LINEAR_MOVERS:

        moves.append(get_linear_moves(board_data, Coordinate(pos.y, pos.x)))

    # If piece is of singular movement type
    elif board_data.board[pos.y][pos.x].type in piece.SINGULAR_MOVERS:
            moves.append(get_singular_moves(board_data, Coordinate(pos.y, pos.x)))



#  Horse, king
def get_singular_moves(board_data: BoardData, cord: Coordinate) -> list[Move]:
    movements = piece.PIECE_TO_MOVEMENT[board_data.board[cord.y][cord.x].type]
    moves = []

    for movement in movements:
        for index in range(0, 2):
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    y = cord.y+movement[index]*i
                    if y < 0 or y > 7:
                        continue
                    x = cord.y+movement[1-index]*j
                    if x < 0 or x > 7:
                        continue

                    if board_data.board[y][x] != piece.EMPTY:
                        if board_data.board[y][x].color == board_data.active:
                            continue
                    moves.append(Move(cord, Coordinate(y, x)))
    return moves


def apply_move(board_data: BoardData, move) -> BoardData:
    temp = copy.deepcopy(board_data)

    if isinstance(move, Move):
        temp.board[move.dest.y][move.dest.x] = temp.board[move.origin.y][move.origin.x]
        temp.board[move.origin.y][move.origin.x] = piece.EMPTY
    elif isinstance(move, Replace):
        pass
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
