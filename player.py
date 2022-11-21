import pygame
import engine
import piece
from random import choice
from typing import Optional
class Player():
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False):
        self.name = name
        self.name_surf = font.render(name, antialiasing,font_color )
        self.image = pygame.transform.scale(pygame.image.load(avatar_img).convert_alpha(), avatar_img_size)


class Human(Player):
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False):
        super().__init__(avatar_img, avatar_img_size,name, font, font_color, antialiasing)
        self.reset()
    def reset(self):
        self.selected = None
        self.legal_moves = []
        self.promotion = None

    def touch(self, board_data: engine.BoardData, pos: engine.Coordinate):
        # If it's not empty
        if  board_data.board[pos.y][pos.x] != piece.EMPTY:
            # If of his color
            if board_data.board[pos.y][pos.x].color == board_data.active:
                self.selected = pos
                self.legal_moves = engine.get_piece_moves(board_data, self.selected)
            # If piece of other color
            else:
                self.apply(board_data, pos)
        # If it's empty
        else:
            self.apply(board_data, pos)
    # NOTE: In only checks for identity
    def apply(self, board_data: engine.BoardData, pos: engine.Coordinate, p_type = None):
        for move in self.legal_moves:
            if move.dest.y == pos.y and move.dest.x == pos.x:
                # If it's a promotion move
                if isinstance(move, engine.Promotion):
                    if p_type == None:
                        self.promotion = move.dest
                        return False
                    elif move.type == p_type:
                        board_data.apply_move(move)
                else:
                    board_data.apply_move(move)
                    self.reset()
                    return True
        self.reset()
        return False
        
    def tell_type(self, board_data: engine.BoardData, p_type):
        self.apply(board_data, self.promotion, p_type)
    
    
class RandomBot(Player):
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False, dept=0):
        super().__init__(avatar_img, avatar_img_size,name, font, font_color, antialiasing)
    def move(self, board_data: engine.BoardData) -> Optional[engine.Move]:
        moves = engine.get_moves(board_data)
        if moves == []:
            return None
        return choice(moves)
    