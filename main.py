import pygame
import sys
import json
import piece

pygame.init()

config_f = open("config.json")
config = json.load(config_f)
config_f.close()

e = "/assets/texture_packs/" + config["texture_pack"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
