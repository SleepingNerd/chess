import pygame
import piece
import texture
import engine
from typing import Optional

# path
class Board():
    def __init__(self, texture_pack, square_size):
        self.square_size = square_size
        self.surface = pygame.Surface([square_size[0] * 8, square_size[1] * 8])
        self.load_texture_pack(texture_pack)
        self.board_data = engine.BoardData()
        self.selected_overlay = pygame.Surface(self.square_size, pygame.SRCALPHA)
        self.selected_overlay.fill((100, 200, 100, 200))
        self.legal_move_overlay = pygame.Surface(self.square_size, pygame.SRCALPHA)
        pygame.draw.circle(self.legal_move_overlay, (100, 200, 100, 200), [round(self.square_size[0]/2), round(self.square_size[1]/2)], 5,5)
        self.capture_overlay = pygame.Surface(self.square_size, pygame.SRCALPHA)
        self.capture_overlay.fill((200, 100, 100, 200))
        self.promotion_overlay = pygame.Surface(self.square_size, pygame.SRCALPHA)
        self.promotion_overlay.fill((100, 200, 50, 40))
        self.castles_overlay = pygame.Surface(self.square_size, pygame.SRCALPHA)
        self.castles_overlay.fill((255,50, 50, 150))






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

    def draw(self, dest, pos, selected : Optional[list[engine.Coordinate]] = None, legal_moves : list[engine.Move] = []):
        self.surface.blit(self.texture_pack.board, (0,0))

        if selected != None:
            for selected in selected:
                self.surface.blit(self.selected_overlay, (selected.x * self.square_size[0], selected.y * self.square_size[1]))

        for i in range(0,len(legal_moves)):
            move = legal_moves[i]
            move_dest = (move.dest.x * self.square_size[0], move.dest.y * self.square_size[1])
            
            if isinstance(move, engine.Capture) or isinstance(move, engine.EnPassant):
                self.surface.blit(self.capture_overlay, move_dest)
            elif isinstance(move, engine.Promotion):
                self.surface.blit(self.promotion_overlay, move_dest)
                i += 3
            elif isinstance(move, engine.Castles):
                self.surface.blit(self.castles_overlay, move_dest)

            elif isinstance(move, engine.Move):
                self.surface.blit(self.legal_move_overlay, move_dest)
            

        for y in range(0, len(self.board_data.board[0])):
            for x in range(0, len(self.board_data.board[1])):
                if self.board_data.board[y][x].type != piece.EMPTY:
                    self.surface.blit(self.texture_pack.pieces[self.board_data.board[y][x].color][self.board_data.board[y][x].type], [
                                      x*self.square_size[0], y * self.square_size[1]])

        dest.blit(self.surface, pos)
