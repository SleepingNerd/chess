import pygame


def read_texture_pack(path):
    image = pygame.image.load(path)
    square_size = [round(image.get_width() / 16),
                   round(image.get_height() / 16)]

    texture_pack = TexturePack()
    #

    dict = {}


class Piece():
    def __init__(self, color, type):
        self.type = type
        self.color = color


class Board():
    def __init__(self, texture_pack):
        self.empty =
