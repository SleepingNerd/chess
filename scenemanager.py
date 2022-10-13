import pygame

from json import load
from board import Board
from pathlib import Path
import texture
import sys
import time
import button


class SceneManager():

    def __init__(self):
        pygame.init()

        config_f = open(Path("config.json"))
        self.config = load(config_f)
        config_f.close()

        win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen_resolution =  [win.get_width(), win.get_height()]

        self.win_size = self.screen_resolution
        self.win = pygame.display.set_mode(self.win_size)





        pygame.display.set_caption(self.config["title_text"])

        self.fullscreen = False

        self.board = Board("assets/texture_packs/"
                           + self.config["texture_pack"], [48, 48])
        self.board.loadfen(self.config["starting_position"])




        self.MAIN_MENU_STATE = 0
        self.INGAME_STATE = 1
        self.START_STATE = self.INGAME_STATE

        self.surface_size = [950, 540]
        self.board_gap_corner = [(self.surface_size[0] - self.board.square_size[0] * 8) / 2, (self.surface_size[1] - self.board.square_size[0] * 8) / 2]

        self.surface = pygame.Surface(self.surface_size)

        self.state = self.START_STATE

        self.ui_bg = (10,10,10)
        self.ui_secondary = (30,30,30)
        self.ui_text = (255,255,255)


        self.title_font =   pygame.font.Font(Path("assets/fonts/Gamer.TTF"),50)
        self.buttons_font = pygame.font.Font(Path("assets/fonts/Gamer.TTF"),50)
        self.title_surface = self.title_font.render(self.config["title_text"], False, self.ui_text)
        self.title_pos = [texture.center_x(self.title_surface, self.surface_size), 20]
        
        self.sound_pack = "assets/sounds/" + self.config["sound_pack"] +"/"
        
        self.main_ui_buttons = button.ButtonHandler([button.TextButton([200,100], [20,100],Path(self.sound_pack + "click.wav"), "Play", self.buttons_font, self.ui_text, self.ui_secondary)])




        self.state_to_function = {self.MAIN_MENU_STATE: self.start_screen, self.INGAME_STATE: self.ingame}

        self.dt = 0
        self.last_time = time.time()

        self.start_animator = texture.AnimationHandler()

        self.TITLE = "CHESS_TITLE"
        self.TITLE_IDLE = "IDLE"
        self.start_animator.add(texture.Animation({self.TITLE_IDLE: [Path("assets/images/title.png"), 2]},[600, 200],0.25,self.TITLE_IDLE, self.TITLE))
        # Is [None,None,None] if player hasn't clicked this frame, else is click position on surface
        self.click_pos = [None, None, None]
        self.board_underlay_size = [40,40]
        self.board_underlay = pygame.Rect([self.board_gap_corner[0]- round(self.board_underlay_size[0]/2), self.board_gap_corner[1]- round(self.board_underlay_size[1]/2)],[(self.board.square_size[0] * 8) + self.board_underlay_size[0], (self.board.square_size[1] * 8)+self.board_underlay_size[1]])
    def start_screen(self):
        self.start_animator.update(self.dt)
        self.surface.fill(self.ui_bg)
        self.surface.blit(self.start_animator.get_image(self.TITLE), (0,0))




    def ingame(self):
        self.surface.fill(self.ui_bg)
        pygame.draw.rect(self.surface, self.ui_secondary, self.board_underlay)
        self.board.draw(self.surface, ((self.board_gap_corner, self.board_gap_corner)))
        self.surface.blit(self.title_surface, self.title_pos)
        self.main_ui_buttons[0].draw(self.surface)

    def update(self):
        self.state_to_function[self.state]()

    def screen_to_window(self):
        self.win.blit(pygame.transform.scale(
            self.surface, self.win_size), (0, 0))

    def start(self):
        while True:
            self.click_pos = [None, None, None]
            self.dt = time.time() - self.last_time
            self.last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click_pos = button.convert_window_pos(event.pos, self.win_size, self.surface_size)
                        

            self.update()
            self.screen_to_window()
            pygame.display.flip()
