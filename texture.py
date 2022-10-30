import pygame
from pathlib import Path

# Format indicator/header for the 'complex' TexturePack format
COMPLEX_HEADER = '+'

def center_x(surface, dest_size):
    if isinstance(surface, pygame.Surface):
        surface = surface.get_size()
    return round((dest_size[0] / 2) - (surface[0] / 2))

def center_y(surface, dest_size):
    return round((dest_size[1] / 2) - (surface.get_height() / 2))

def center(surface, dest_size):
    return [center_x(surface, dest_size), center_y(surface,dest_size)]

def load_and_scale(path, scale):
    pygame.transform.scale(pygame.image.load(path), scale)

def load_and_scale_animation(path, frames, scale):
    image = pygame.image.load(Path(path)).convert_alpha()
    width = image.get_width()
    height = image.get_height()

    step = round(width / frames)
    animation = []
    for offset in range(0, width, step):
        surface = pygame.transform.scale(get_slice(pygame.Rect((offset, 0), (step, height)), image), scale)
        animation.append(surface)
    return animation


def get_slice(rect: pygame.Rect, image: pygame.Surface, colorkey: tuple[int, int, int] = None) -> pygame.Surface:
    """
        Returns sliced rect from image as an alpha surface,
        and colorkeys it (if a colorkey has been specified)
    """
    # Create empty alpha surface, of rect.size
    surf = pygame.Surface(rect.size).convert_alpha()
    surf.fill((0,0,0,0))

    # Blit rect from image on the surface
    surf.blit(image, (0, 0), rect)

    # If colorkey isn't None, apply colorkey
    if colorkey != None:
        pygame.transform.threshold(surf, surf, colorkey, set_color=(0,0,0,0), threshold=(0,0,0,0), set_behavior=1, inverse_set = True)

    # Return resulting surface
    return surf

"""
Class representing a "texture pack" for all pieces and the chess board
"""
class TexturePack:
    def __init__(self, board: pygame.Surface, pieces: list[list[pygame.Surface]]):
        self.board = board
        self.pieces = pieces

    def scale(self, square_size: tuple[int, int]):
        """
        Scales every piece to square_size, and the board to 8*square_size
        """
        for color in range(0, len(self.pieces)):
            for piece in range(0, len(self.pieces[color])):
                self.pieces[color][piece] = pygame.transform.scale(self.pieces[color][piece], square_size)
        self.board = pygame.transform.scale(self.board, [square_size[0] *8,square_size[1] *8])

def read_texture_pack(path: str) -> TexturePack:
    """
    Returns a TexturePack object, from path

    The image read from path can be interpeted in two ways:
    1. The default way, generally easier to import,
       (2 color chess board, pieces shouldn't contain those 2 colors)
    2. The complex way, indicated by the file name starting with COMPLEX_HEADER,
       (custom chess board, all colors can be used for pieces)
    """

    # Determine format
    file = path.split("/")
    file = file[len(file)-1]

    # Load image
    image = pygame.image.load(Path(path)).convert_alpha()
    pieces = [[], []]

    # If file should be read the complex way
    if file[0] == COMPLEX_HEADER:
        # Determine square_size
        square_size = [round(image.get_width() / 8),
                       round(image.get_height() / 10)]

        # Read pieces and pawns
        for color in range(0, 2):
            for x in range(0, 6):
                pieces[color].append(get_slice(pygame.Rect([x*square_size[0], color * square_size[1]], square_size), image))

        # Read board
        board = get_slice(pygame.Rect([0, 2*square_size[1]], [8*square_size[0], 8*square_size[1]]), image)

        # Return resulted TexturePack object
        return TexturePack(board, pieces)

    # If file should be read the simple way
    else:
        # Determine square_size
        square_size = [round(image.get_width() / 8),
                       round(image.get_height() / 8)]

        # Determine background colors, so we can colorkey them away later
        third_row = square_size[1]*2
        empty = [image.get_at([0, third_row]), image.get_at(
                [square_size[0], third_row])]

        # Keeps track of the 'current' colorkey
        square_color = 0
        # Keeps track of the current row
        row = 0

        # Read black and white's pieces
        for color in range(-1, 1):
            for x in range(0, 5):
                pieces[color].append(get_slice(pygame.Rect([x*square_size[0], row], square_size), image, empty[square_color]))
                square_color += 1
                if square_color == 2:
                    square_color = 0
            row = square_size[1] * 7
        color = 0

        # Read black and white's pawns
        for y in range(square_size[1] * 6, 0, -square_size[1] * 5):
            pieces[color].append(get_slice(pygame.Rect([0, y], square_size), image, empty[square_color]))
            square_color = 1
            color = 1

        # Read board
        board = pygame.Surface([square_size[0] *8, square_size[1] *8])
        for i in range(0, 8):
            for j in range(0, 8):
                pygame.draw.rect(board, empty[(i + j) % 2], pygame.Rect(
                    [i * square_size[0], j * square_size[1]], square_size))

        # Return resulted TexturePack object
        return TexturePack(board, pieces)


def load_and_scale_animation(path, frames, scale):
    image = pygame.image.load(Path(path)).convert_alpha()
    width = image.get_width()
    height = image.get_height()

    step = round(width / frames)
    animation = []
    for offset in range(0, width, step):
        surface = pygame.transform.scale(get_slice(pygame.Rect((offset, 0), (step, height)), image), scale)
        animation.append(surface)
    return animation


# Class used to manage animations
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
            self.set_current_image()


    def set_current_image(self):
        self.current_image = self.state_to_animation[self.state][0][self.frame]

    def get_current_image(self):
        return self.current_image
