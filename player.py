import pygame
import engine
import piece
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

    def touch(self, board_data: engine.BoardData, pos: engine.Coordinate):
        # If it's not empty
        if  board_data.board[pos.y][pos.x] != piece.EMPTY:
            # If of his color
            if board_data.board[pos.y][pos.x].color == board_data.active:
                self.selected = pos
                self.legal_moves = engine.get_piece_moves(board_data, self.selected)
            else:
                if self.is_legal(board_data, pos):
                    board_data.apply_move(engine.Move(self.selected, pos))
                    self.reset()
                
        # If it's empty
        else:

            if self.is_legal(board_data, pos):
                board_data.apply_move(engine.Move(self.selected, pos))
                self.reset()
            else:
                self.reset()
                
    # NOTE: In only checks for identity
    def is_legal(self, board_data: engine.BoardData, pos: engine.Coordinate):
        for value in self.legal_moves:
            if value.y == pos.y and value.x == pos.x:
                return True
            
        return False
                


            
                
