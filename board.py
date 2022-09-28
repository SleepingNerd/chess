import pygame
import piece
import texture

# path


class Board():

    def __init__(self, texture_pack, square_size):

        self.square_size = square_size
        self.board = []
        self.turn = piece.WHITE
        self.castles = []
        self.last_capture = 0
        self.en_passants = []
        self.surface = pygame.Surface([square_size[0] * 8, square_size[1] * 8])
        self.load_texture_pack(texture_pack)

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

    def empty_board(self):
        self.board = []
        for i in range(0, 8):
            self.board.append([])
            for j in range(0, 8):
                self.board[i].append(piece.EMPTY)

    def loadfen(self, fen):
        self.empty_board()

        fen = fen.split(" ")
        fen[0] = fen[0].split("/")

        for rank in range(0, len(fen[0])):
            file = 0
            for ch in fen[0][rank]:
                if file > 7:
                    break

                elif ch in piece.CH_TO_PIECE:
                    self.board[rank][file] = piece.CH_TO_PIECE[ch]
                    file += 1
                else:
                    file += int(ch)

        self.turn = piece.CH_TO_COLOR[fen[1]]

    def draw(self, dest, pos):
        for i in range(0, 8):
            for j in range(0, 8):
                pygame.draw.rect(self.surface, self.texture_pack.empty[(i + j) % 2], pygame.Rect(
                    [i * self.square_size[0], j * self.square_size[1]], self.square_size))

        for y in range(0, len(self.board[0])):
            for x in range(0, len(self.board[1])):
                if self.board[y][x] != piece.EMPTY:
                    self.surface.blit(self.texture_pack.pieces[self.board[y][x].color][self.board[y][x].type], [
                                      x*self.square_size[0], y * self.square_size[1]])


        dest.blit(self.surface, pos)
