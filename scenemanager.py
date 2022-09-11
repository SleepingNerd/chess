import pygame

from json import load
from board import Board
from pathlib import Path


class SceneManager():

    def __init__(self):
        pygame.init()

        config_f = open(Path("config.json"))
        self.config = load(config_f)
        config_f.close()

        self.win_size = [800, 800]
        self.win = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.config["title_text"])

        self.board = Board("assets/texture_packs/"
                           + self.config["texture_pack"], [round(720/8), round(720/8)])
        self.board.loadfen(self.config["starting_position"])

        self.START_STATE = 0

        self.screen_size = [900, 900]
        self.surface = pygame.Surface(self.screen_size)

        self.state = self.START_STATE
        self.start_bg = (217, 160, 102)
        self.click_pos = [-1, -1, -1]

        self.title_font = pygame.font.Font(
            "fonts/" + self.config["title_font"], 125)
        self.title_surf = self.title_font.render(self.config["title_text"], True, self.config["title_color"])
        self.state_to_function = {self.START_STATE: self.start}

    def start(self):
        self.surface.fill(self.start_bg)

    def update(self):

        self.state_to_function[self.state]()
