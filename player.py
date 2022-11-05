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
            # If piece of other color
            else:
                self.apply(board_data, pos)
        # If it's empty
        else:
            self.apply(board_data, pos)
    # NOTE: In only checks for identity
    def apply(self, board_data: engine.BoardData, pos: engine.Coordinate):
        for move in self.legal_moves:
            if move.dest.y == pos.y and move.dest.x == pos.x:
                board_data.apply_move(move)
                self.reset()
                return True
        self.reset()
        return False
