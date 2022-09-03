import pygame

# Constants to represent piece values in a human readable way
WHITE = 0
BLACK = 1

ROOK = 0
HORSE = 1
BISHOP = 2
QUEEN = 3
KING = 4

PAWN = 5

# Empty from left top to right
# Pieces is a dict


class TexturePack:
    def __init__(self, empty, pieces):
        self.empty = empty
        self.pieces = pieces


def read_texture_pack(path):

    image = pygame.image.load(path)
    square_size = [round(image.get_width() / 8),
                   round(image.get_height() / 8)]

    # Read first two empty squares from third row (matches with first two color from left top)
    third_row = square_size[1]*2
    empty = []

    empty = [image.get_at(0, third_row), image.get_at(
        square_size[0], third_row)]
