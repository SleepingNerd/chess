import pygame
import sys
import json
import piece

from scenemanager import SceneManager


pygame.init()

win_size = [800, 800]
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Bichess")

scene_manager = SceneManager()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene_manager.update()
    win.blit(pygame.transform.scale(scene_manager.surface, win_size), (0, 0))
    pygame.display.flip()
