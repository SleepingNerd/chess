import pygame
from pathlib import Path

# Format indicator/header
COMPLEX_HEADER = '+'

# Empty from left top to right
# Pieces is a dict

def center_x(surface, dest_size):
    return round((dest_size[0] / 2) - (surface.get_width() / 2))


def center_y(surface, dest_size):
    return round((dest_size[1] / 2) - (surface.get_height() / 2))

def load_and_scale(path, scale):
    pygame.transform.scale(pygame.image.load(path), scale)

def load_and_scale_animation(path, frames, scale):
    image = pygame.image.load(path).convert_alpha()

    width = image.get_width()
    height = image.get_height()

    step = round(width / frames)
    animation = []
    for offset in range(0, width, step):
        surface = pygame.transform.scale(get_slice(pygame.Rect((offset, 0), (step, height)), image), scale)
        animation.append(surface)
    return animation


def get_slice(rect, image, colorkey=None):

    surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    surf.blit(image, (0, 0), rect)

    if colorkey != None:
        surf.set_colorkey(colorkey)

    return surf


class AnimationHandler:
    def __init__(self):
        self.animations = []
    def update(self, dt):
        for animation in self.animations:
            animation.update(dt)

    def get_image(self, id):
        for animation in self.animations:
            if animation.id == id:
                return animation.get_current_image()

    def add(self, animation):
        self.animations.append(animation)

    def remove(self, id):
        len = len(self.animations)
        for i in range(0, len):
            if self.animations[i].id == id:
                del self.animations[i]
                len -= 1






class Animation:
    def __init__(self, animation_states_to_path, base_size, time_per_frame, start_state, id):

        self.state_to_animation = {}
         #0: path
         #1: frames (always from left to right)
         #2: scale to scale to if it has

        self.id = id

        for key in animation_states_to_path.keys():
            self.state_to_animation[key] = ["image_array", "total_frames"]

            if len(animation_states_to_path) == 3:
                scale = animation_states_to_path[key][2]
            else:
                scale = base_size

            self.state_to_animation[key][0] = load_and_scale_animation(animation_states_to_path[key][0], animation_states_to_path[key][1], scale)
            self.state_to_animation[key][1] = animation_states_to_path[key][1]


        self.state = start_state
        self.frame = 0
        self.time_per_frame = time_per_frame
        self.time_since_last = 0
        self.set_current_image()


    def update(self, dt):
        self.time_since_last += dt
        if self.time_since_last >= self.time_per_frame:
            self.time_since_last = self.time_since_last - self.time_per_frame
            self.frame += 1
            if self.frame >= self.state_to_animation[self.state][1]:
                self.frame = self.frame - self.state_to_animation[self.state][1]

    def set_current_image(self):
        self.current_image = self.state_to_animation[self.state][0][self.frame]

    def get_current_image(self):
         return self.current_image

class TexturePack:
    def __init__(self, empty, pieces):
        self.empty = empty
        self.pieces = pieces

    def scale(self, size):
        for color in range(0, len(self.pieces)):
            for piece in range(0, len(self.pieces[color])):
                self.pieces[color][piece] = pygame.transform.scale(self.pieces[color][piece], size)


# Returns surface from square of image starting at position with size of square_size
# NOTE: position is NOT muiltiplied by square_size




# Path should be a string, or a Path object

# Rules for basic:
# Must be 8 by 8
# One image
# Image must not have colors used for background
# Background must be a check pattern with two colors
def read_texture_pack(path):
    # Determine format
    file = path.split("/")
    file = file[len(file)-1]

    # Load image
    image = pygame.image.load(Path(path))

    pieces = [[], []]

    if file[0] == COMPLEX_HEADER:
        square_size = [round(image.get_width() / 8),
                       round(image.get_height() / 10)]

        for color in range(0, 2):
            for x in range(0, 5):
                pieces[color].append(get_slice(pygame.Rect([x*square_size[0], row], square_size), image, empty[square_color]))





    else:
        square_size = [round(image.get_width() / 8),
                       round(image.get_height() / 8)]

        # Read first two empty squares from third row (matches with first two color from left top)
        third_row = square_size[1]*2
        empty = [image.get_at([0, third_row]), image.get_at(
                [square_size[0], third_row])]

        # Keeps track of the pieces colorkey
        square_color = 0
        row = 0

        # Black and white's pieces
        for color in range(0, 2):

            for x in range(0, 5):
                pieces[color].append(get_slice(pygame.Rect([x*square_size[0], row], square_size), image, empty[square_color]))

                square_color += 1
                if square_color == 2:
                    square_color = 0
            row = square_size[1] * 7

        # Black and white's pawns
        for y in range(square_size[1] * 6, 0, -square_size[1] * 5):

            pieces[color].append(get_slice(pygame.Rect([0, y], square_size), image, empty[square_color]))
            square_color = 1
            color = 0

        return TexturePack(empty, pieces)


    def read_texture_pack(path, path2):
        pass
