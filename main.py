import pygame
import sys
import json
import piece
import board
from pathlib import Path


pygame.init()

config_f = open(Path("config.json"))
config = json.load(config_f)
config_f.close()

board.Board("ekfoe")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
