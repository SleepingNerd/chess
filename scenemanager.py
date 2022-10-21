from cgitb import text
import pygame

from json import load
from board import Board
from pathlib import Path
import texture
import sys
import time
import button
import player


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

        self.board = Board("assets/images/board_and_pieces/"
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
        buttons = ["Play", "Settings", "Exit"]
        self.main_ui_buttons = button.ButtonHandler([])
        start = [35, self.board_gap_corner[1]+5]
        self.portrets = "assets/images/ui/portrets/"+self.config["portrets"]+"/"
        
        self.portret_size = [75,75]
        self.players = [player.Player(self.portrets + "player.png", self.portret_size, "Player", self.buttons_font, self.ui_text)]
        self.player_index = 0
        
        height = 50
        width = 200
        gap = 5 + height 
        for y in range (0,3):
            self.main_ui_buttons.buttons.append( button.TextButton([width,height], [start[0],start[1] + gap * y],Path(self.sound_pack + "click.wav"), buttons[y], self.buttons_font, self.ui_text, self.ui_secondary)) 
            
        self.portret_underlay_gap = 10
        self.other_ui_rect = pygame.Rect([start[0],start[1]*3+height - 20],[width, height*4])
        self.portret_rect = pygame.Rect([self.other_ui_rect.left +texture.center_x(self.portret_size, self.other_ui_rect.size), self.other_ui_rect.top + round(self.portret_size[1] /2)], self.portret_size)
        self.portret_underlay = self.portret_rect.move([-self.portret_underlay_gap, -self.portret_underlay_gap])
        self.portret_underlay.size = [self.portret_underlay.width + self.portret_underlay_gap*2, self.portret_underlay.height+self.portret_underlay_gap*2]
        self.portret_name_rect = self.portret_rect.move(0, self.portret_size[1]+20)


        
        self.PLAY_STATE = "PLAY"
        self.SETTINGS_STATE = "SETTINGS"
        self.ui_state = None
        

        self.state_to_function = {self.MAIN_MENU_STATE: self.start_screen, self.INGAME_STATE: self.ingame}

        self.dt = 0
        self.last_time = time.time()

        self.start_animator = texture.AnimationHandler()

        # Is [None,None,None] if player hasn't clicked this frame, else is click position on surface
        self.click_pos = [None, None]
        self.board_underlay_size = [40,40]
        self.board_underlay = pygame.Rect([self.board_gap_corner[0]- round(self.board_underlay_size[0]/2), self.board_gap_corner[1]- round(self.board_underlay_size[1]/2)],[(self.board.square_size[0] * 8) + self.board_underlay_size[0], (self.board.square_size[1] * 8)+self.board_underlay_size[1]])
    def start_screen(self):
        self.start_animator.update(self.dt)
        self.surface.fill(self.ui_bg)
        self.surface.blit(self.start_animator.get_image(self.TITLE), (0,0))

    def update_main_ui(self):
        # Play pressed:
        if self.main_ui_buttons.buttons[0].pressed:
            self.main_ui_buttons.buttons[0].pressed = False
            self.ui_state = self.PLAY_STATE 
        # Settings pressed:
        elif self.main_ui_buttons.buttons[1].pressed:
            self.main_ui_buttons.buttons[1].pressed = False
            self.ui_state = self.SETTINGS_STATE        
        # Exit
        elif self.main_ui_buttons.buttons[2].pressed:
            self.quit()       
            
    def draw_main_ui(self):
        self.main_ui_buttons.draws(self.surface)
        
        if self.ui_state == self.PLAY_STATE:
            pygame.draw.rect(self.surface, self.ui_secondary, self.other_ui_rect)
            self.surface.blit(self.players[self.player_index].image, self.portret_rect)
            self.portret_name_rect.x =  self.other_ui_rect.left + texture.center_x(self.players[self.player_index].name_surf, self.other_ui_rect.size)
            pygame.draw.rect(self.surface, self.ui_secondary, self.portret_underlay)
            self.surface.blit(self.players[self.player_index].image, self.portret_rect)

            self.surface.blit(self.players[self.player_index].name_surf, self.portret_name_rect)
        
            
            
        elif self.ui_state == self.SETTINGS_STATE:
            pass
            
    
    def ingame(self):
        self.main_ui_buttons.updates(self.click_pos)
        
        self.update_main_ui()
        
            
        
        
        
        # Drawing loop
        self.surface.fill(self.ui_bg)
        pygame.draw.rect(self.surface, self.ui_secondary, self.board_underlay)
        self.board.draw(self.surface, ((self.board_gap_corner, self.board_gap_corner)))
        self.surface.blit(self.title_surface, self.title_pos)
        self.draw_main_ui()
        
        
        
        

    def update(self):
        self.state_to_function[self.state]()

    def screen_to_window(self):
        self.win.blit(pygame.transform.scale(
            self.surface, self.win_size), (0, 0))

    def start(self):
        while True:
            self.click_pos = [None, None]
            self.dt = time.time() - self.last_time
            self.last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click_pos = button.convert_window_pos(event.pos, self.win_size, self.surface_size)
                        

            self.update()
            self.screen_to_window()
            pygame.display.flip()
    def quit(self):
        pygame.quit()
        sys.exit()
        
