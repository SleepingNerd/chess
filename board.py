import pygame
import piece
import texture

# path


def read_fen()


class Board():

    def __init__(self, texture_pack):
        if isinstance(texture_pack, str):
            self.texture_pack = texture.read_texture_pack(texture_pack)
        elif isinstance(texture_pack, TexturePack):
            self.texture_pack = TexturePack
        else:
            raise TypeError(str(texture_pack)
                            + "must be of type TexturePack or string!")

    def loadfen()
