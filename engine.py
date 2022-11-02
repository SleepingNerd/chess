import piece


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

class Coordinate():
    def __init__(self, y, x):
        self.y = y
        self.x = x

class Move():
    def __init__(self, origin: Coordinate, dest:Coordinate):
        self.origin = origin
        self.dest   = dest
class AddPiece()

class RemovePiece()

class ReplacePiece

# For bishop, bishop, and maybe pawn
def get_linear_moves(board_data: BoardData, cord: Coordinate) -> List[Move]:
    movements = piece.PIECE_TO_MOVEMENT[board_data[cord.y][cord.x]]
    moves = []

    # God forgive me for this
    for movement in movements:
        for index in range(0, 2):
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    for y in range(1, 8):
                        y = cord.y+movement[index]*y*i
                        if y < 0 or y > 7:
                            break

                        for x in range(1, 8):
                            x = cord.y+movement[1-index]*x*j
                            if x < 0 or x > 7:
                                break

                            if BoardData[y][x] != piece.EMPTY:
                                if BoardData[y][x].color == board_data.active:
                                    y = 100
                                    break

                            moves.append()

# Pawn, horse, king
def get_singular_moves():
    pass


def get_moves(board_data: BoardData):
    # First of all check if the king is in check


    # Iterate through all pieces from the active color
    for y in range(0, len(board_data.board[0])):
            for x in range(0, len(board_data.board[1])):
                # If piece is of active color
                if board_data.board[y][x].color == board_data.active:
                    # If piece is of linear movement type
                    if  board_data.board[y][x].piece in piece.LINEAR_MOVERS:
                        get_linear_moves()


                    # If piece is of singular movement type
                    elif board_data.board[y][x].piece in piece.SINGULAR_MOVERS:



        # Collect all "Basic moves", and check if they result in check for the active piece's king (also deals with checks incflicted before the move)

    # Check for castles (or skips if king was in check)

    # Check for en passants (and cancels them out if it results in a check afterwards)

    # Check for promotions, and double pawn movements (and cancels them out if it results in a check afterwards)
