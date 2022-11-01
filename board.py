import pygame
import piece
import texture
import engine

# path
class Board():
    def __init__(self, texture_pack, square_size):
        self.square_size = square_size
        self.surface = pygame.Surface([square_size[0] * 8, square_size[1] * 8])
        self.load_texture_pack(texture_pack)
        self.board_data = engine.BoardData()

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
        self.board_data = engine.readfen(fen)

    def draw(self, dest, pos):
        self.surface.blit(self.texture_pack.board, (0,0))
        

        for y in range(0, len(self.board_data.board[0])):
            for x in range(0, len(self.board_data.board[1])):
                if self.board_data.board[y][x] != piece.EMPTY:
                    self.surface.blit(self.texture_pack.pieces[self.board_data.board[y][x].color][self.board_data.board[y][x].type], [
                                      x*self.square_size[0], y * self.square_size[1]])


        dest.blit(self.surface, pos)




    