import pygame
import sys
import json
import piece
from board import Board
from pathlib import Path
from scenemanager import SceneManager


pygame.init()

win_size = [800, 800]
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Bichess")

scene_manager = SceneManager()


config_f = open(Path("config.json"))
config = json.load(config_f)
config_f.close()

board = Board("assets/texture_packs/"
              + config["texture_pack"], [round(720/8), round(720/8)])
board.loadfen(config["starting_position"])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene_manager.update()
    win.blit(pygame.transform.scale(scene_manager.surface, win_size), (0, 0))
    board.draw(win, [0, 0])
    pygame.display.flip()
