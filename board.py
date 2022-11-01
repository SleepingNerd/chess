import pygame
import piece
import texture


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
        self.turn  = piece.WHITE
        # Q then K
        self.castles = [[False, False], [False, False]]
        self.en_passant = None
        self.halfmoves = 0
    

        
    

# path
class Board():

    def __init__(self, texture_pack, square_size):

        self.square_size = square_size
        self.surface = pygame.Surface([square_size[0] * 8, square_size[1] * 8])
        self.load_texture_pack(texture_pack)
        self.board_data = BoardData()

    # Loads texture pack and scales to self.square_size
    def load_texture_pack(self, texture_pack):
        if isinstance(texture_pack, str):


            self.texture_pack = texture.read_texture_pack(texture_pack)
        elif isinstance(texture_pack, texture.TexturePack):
            self.texture_pack = texture_pack
        else:
            raise TypeError(str(texture_pack)
                            + "must be of type TexturePack or string!")
        self.texture_pack.scale(self.square_size)

    def loadfen(self, fen):
        self.board_data = readfen(fen)

    def draw(self, dest, pos):
        self.surface.blit(self.texture_pack.board, (0,0))
        

        for y in range(0, len(self.board_data.board[0])):
            for x in range(0, len(self.board_data.board[1])):
                if self.board_data.board[y][x] != piece.EMPTY:
                    self.surface.blit(self.texture_pack.pieces[self.board_data.board[y][x].color][self.board_data.board[y][x].type], [
                                      x*self.square_size[0], y * self.square_size[1]])


        dest.blit(self.surface, pos)



def readfen(fen: str) -> BoardData:
    # BoardData object
    board_data = BoardData()

    # Split fen
    fen = fen.split(" ")
    # Split position at \
    fen[0] = fen[0].split("/")
    
    # Position
    for rank in range(0, len(fen[0])):
        file = 0
        for ch in fen[0][rank]:
            if file > 7:
                break
            elif ch in piece.CH_TO_PIECE:
                board_data.board[rank][file] = piece.CH_TO_PIECE[ch]
                file += 1
            else:                    
                file += int(ch)
    # Active color
    board_data.turn = piece.CH_TO_COLOR[fen[1]]
    
    # Castles right
    for ch in fen[2]:
        i = piece.CH_TO_CASTLES[ch]
        board_data.castles[i[0]][i[1]] = True
        
    # If there's a possible en passant target
    if fen[3] != '-':
        board_data.en_passant = [int(fen[3][1])-1, ]
        print(board_data.en_passant)
        
        
    
    
    # Halfmove clock
    
    #
    return board_data
    
    