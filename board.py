import pygame
import piece
import texture

# path


class Board():

    def __init__(self, texture_pack):
        if isinstance(texture_pack, str):
            self.texture_pack = texture.read_texture_pack(texture_pack)
        elif isinstance(texture_pack, TexturePack):
            self.texture_pack = TexturePack
        else:
            raise TypeError(str(texture_pack)
                            + "must be of type TexturePack or string!")

        self.board = []

        self.turn = piece.WHITE

        self.castles = []
        self.last_capture =  0
        self.en_passants = []


    def loadfen(fen):
        empty_board()

        fen = fen.split(" ")
        fen[0] =  fen[0].split("/")

        for rank in range(0, len(fen[0])):
            file = 0
            for ch in fen[0][rank]:
                if file > 7:
                    break;

                elif ch in piece.CH_TO_PIECE:
                    self.board[rank][file] = piece.CH_TO_PIECE[ch]
                    file += 1
                else:
                    file += int(ch)


        self.turn = piece.CH_TO_COLOR[fen[1]]






    def empty_board():
        self.board = []
        for i in range(0, 8):
            self.board.append([])
            for j in range(0, 8):
                self.board[i].append[piece.EMPTY]
