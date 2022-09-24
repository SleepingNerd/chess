import pygame
from pathlib import Path

# Empty from left top to right
# Pieces is a dict

def center_x(surface, dest_size):
    return round((dest_size[0] / 2) - (surface.get_width() / 2))


def center_y(surface, dest_size):
    return round((dest_size[1] / 2) - (surface.get_height() / 2))

def load_and_scale(path, scale):
    pygame.transform.scale(pygame.image.load(path), scale)

def load_and_scale_animation(path, frames, scale):
    image = pygame.image.load(path)

    width = image.get_width()
    height = image.get_height()

    step = round(width / frames)
    animation = []
    for offset in range(0, width, step):
        surf = pygame.Surface((step, height))
        surf.blit(image, (0, 0), ())












class Animation:
    def __init__(self, animation_states_to_path, base_size, time_per_frame, start_state):

        self.state_to_animation = {}
         #0: path
         #1: frames (always from left to right)
         #2: scale to scale to if it has

        for key in animation_states_to_path.keys():
            self.state_to_animation[key] = "image_array"

            if len(animation_states_to_path) == 3:
                size = animation_states_to_path[key][2]
            else:
                size = base_size

            self.state_to_animation[key] =
            animation_states_to_path[key][0]







        self.state = start_state
        self.frame = 0
        self.time_since_last = 0




class TexturePack:
    def __init__(self, empty, pieces):
        self.empty = empty
        self.pieces = pieces

    def scale(self, size):
        for color in self.pieces:
            for piece in color:
                piece = pygame.transform.scale(piece, size)

# Returns surface from square of image starting at position with size of square_size
# NOTE: position is NOT muiltiplied by square_size


def get_square_surf(position, square_size, image, colorkey):
    surf = pygame.Surface(square_size)
    rect = pygame.Rect(position, square_size)
    surf.blit(image, (0, 0), rect)
    surf.set_colorkey(colorkey)
    return surf


# Path should be a string, or a Path object
def read_texture_pack(path):
    image = pygame.image.load(Path(path))
    square_size = [round(image.get_width() / 8),
                   round(image.get_height() / 8)]

    # Read first two empty squares from third row (matches with first two color from left top)
    third_row = square_size[1]*2
    empty = [image.get_at([0, third_row]), image.get_at(
            [square_size[0], third_row])]

    pieces = [[], []]
    # Keeps track of the pieces colorkey
    square_color = 0
    row = 0

    # Black and white's pieces
    for color in range(0, 2):

        for x in range(0, 5):

            pieces[color].append(get_square_surf(
                [x*square_size[0], row], square_size, image, empty[square_color]))

            square_color += 1
            if square_color == 2:
                square_color = 0
        row = square_size[1] * 7

    # Black and white's pawns
    for y in range(square_size[1] * 6, 0, -square_size[1] * 5):

        pieces[color].append(get_square_surf(
            [0, y], square_size, image, empty[square_color]))
        square_color = 1
        color = 0

    return TexturePack(empty, pieces)
