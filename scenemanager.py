import pygame


class SceneManager():


    def __init__(self):

        self.START_STATE = 0

        self.screen_size = [900, 900]
        self.surface = pygame.Surface(self.screen_size)

        self.state = self.START_STATE
        self.start_bg = (217, 160, 102)
        self.click_pos = [-1, -1, -1]




        self.state_to_function = {self.START_STATE: self.start}

    def start(self):
        self.surface.fill(self.start_bg)










    def update(self):

        if pygame.event.get(pygame.mouse.get_pressed(1)):
            self.click_pos = pygame.mouse.get_pos()
        else:
            self.click_pos = [-1, -1, -1]

        self.state_to_function[self.state]()
