import pygame

from json import load
from board import Board
from pathlib import Path
import texture
import sys
import time


class SceneManager():

    def __init__(self):
        pygame.init()

        config_f = open(Path("config.json"))
        self.config = load(config_f)
        config_f.close()

        self.win_size = [600, 600]
        self.win = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.config["title_text"])

        self.board = Board("assets/texture_packs/"
                           + self.config["texture_pack"], [round(720/8), round(720/8)])
        self.board.loadfen(self.config["starting_position"])

        self.START_STATE = 0

        self.surface_size = [600, 600]
        self.surface = pygame.Surface(self.surface_size)

        self.state = self.START_STATE
        self.start_bg = (217, 160, 102)
        self.click_pos = [-1, -1, -1]

        self.title_font = pygame.font.Font(
            "assets/fonts/" + self.config["title_font"], 125)
        self.title_rotation = 0
        self.title_rotation_range = [-10, 10]
        self.title_rotation_speed = 9
        self.title_surf = self.title_font.render(
            self.config["title_text"], True, self.config["title_color"])
        self.state_to_function = {self.START_STATE: self.start_screen}

        self.dt = 0
        self.last_time = time.time()

    def start_screen(self):
        self.surface.fill(self.start_bg)
        self.surface.blit(pygame.transform.rotate(self.title_surf, self.title_rotation), [texture.center_x(
            self.title_surf, self.surface_size), 100])

        self.title_rotation += self.dt*self.title_rotation_speed

        if self.title_rotation < self.title_rotation_range[0]:
            self.title_rotation = self.title_rotation_range[0]
            self.title_rotation_speed *= -1
        elif self.title_rotation > self.title_rotation_range[1]:
            self.title_rotation = self.title_rotation_range[1]
            self.title_rotation_speed *= -1

    def ingame():
        pass

    def update(self):
        self.state_to_function[self.state]()

    def screen_to_window(self):
        self.win.blit(pygame.transform.scale(
            self.surface, self.win_size), (0, 0))

    def start(self):
        while True:
            self.dt = time.time() - self.last_time
            self.last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.screen_to_window()
            pygame.display.flip()
