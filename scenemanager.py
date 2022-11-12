"""
Handles rendering and game logic
"""
import pygame
from json import load
from board import Board
from pathlib import Path
from button import TextButton
import texture
import sys
import time
import button
import player
import piece
import engine

class SceneManager():
    """
    Handles rendering and game logic
    """
    def __init__(self):
        pygame.init()
        # Open config file, and assign read json to config
        config_f = open(Path("config.json"))
        self.config = load(config_f)
        config_f.close()

        # Create window, and scale it to be fullscreen
        win = pygame.display.set_mode((0,0))
        self.screen_resolution =  [win.get_width(), win.get_height()]
        self.win_size = self.screen_resolution
        self.win = pygame.display.set_mode(self.win_size)

        # Set window caption, as indicated in config
        pygame.display.set_caption(self.config["title_text"])

        # Load in texture pack indicated in config, and load in starting position
        self.board = Board("assets/images/board_and_pieces/"+ self.config["texture_pack"], [48, 48])
        self.board.loadfen(self.config["starting_position"])

        # "Game states", indicate which function should be called at start of every frame
        self.MAINGAME_STATE = 1
        self.state = self.MAINGAME_STATE
        self.state_to_function = {self.MAINGAME_STATE: self.maingame}

        # Unscaled size the actual surface of game
        self.surface_size = [950, 540]
        self.surface = pygame.Surface(self.surface_size)

        # Offset applied from (0,0)
        self.board_offset = [round((self.surface_size[0] - self.board.square_size[0] * 8) / 2), round((self.surface_size[1] - self.board.square_size[0] * 8) / 2)]
        self.board_bottomright = [self.board_offset[0]+ self.board.surface.get_width(), self.board_offset[1]+ self.board.surface.get_height()]


        # Colors used in ui
        self.ui_bg = (10,10,10)
        self.ui_white = (255,255,255)
        self.ui_black = (0,0,0)
        self.ui_secondary = (30,30,30)
        self.ui_text = (255,255,255)
        self.ui_green = (124,252,0)

        # Fonts used in ui
        self.title_font =   pygame.font.Font(Path("assets/fonts/Gamer.TTF"),50)
        self.buttons_font = pygame.font.Font(Path("assets/fonts/Gamer.TTF"),50)

        # Title surface, and its position
        self.title_surface = self.title_font.render(self.config["title_text"], False, self.ui_text)
        self.title_pos = [texture.center_x(self.title_surface, self.surface_size), 20]

        # Directory containing sounds
        self.sound_pack = "assets/sounds/" + self.config["sound_pack"] +"/"

        # "main ui" buttons
        buttons = ["Play", "Settings", "Exit"]
        self.main_ui_buttons = button.ButtonHandler([])
        start = [35, self.board_offset[1]+5]
        height = 50
        width = 200
        gap = 5 + height
        for y in range (0,3):
            self.main_ui_buttons.buttons.append( button.TextButton([width,height], [start[0],start[1] + gap * y],Path(self.sound_pack + "click.wav"), buttons[y], self.buttons_font, self.ui_text, self.ui_secondary))


        # Player list, and portret ui
        self.portrets = "assets/images/ui/portrets/"+self.config["portrets"]+"/"
        self.portret_size = [75,75]
        self.players = [player.Human(self.portrets + "human.png", self.portret_size, "Human", self.buttons_font, self.ui_text), player.RandomBot(self.portrets + "bot.png", self.portret_size, "Random", self.buttons_font, self.ui_text)]
        self.player_index = 0
        self.active_players = [None, None]
        self.total_players = len(self.players)
        self.portret_underlay_gap = 10
        self.other_ui_rect = pygame.Rect([start[0],start[1]*3+height - 20],[width, height*4])
        self.portret_rect = pygame.Rect([self.other_ui_rect.left +texture.center_x(self.portret_size, self.other_ui_rect.size), self.other_ui_rect.top + round(self.portret_size[1] /4)], self.portret_size)
        self.portret_underlay = self.portret_rect.move([-self.portret_underlay_gap, -self.portret_underlay_gap])
        self.portret_underlay.size = [self.portret_underlay.width + self.portret_underlay_gap*2, self.portret_underlay.height+self.portret_underlay_gap*2]
        self.portret_name_rect = self.portret_rect.move(0, self.portret_size[1]+20)
        self.arrow_buttons = button.ButtonHandler([])
        arrow_buttons_size = [40,40]
        arrow_buttons_gap = 18
        self.arrow_buttons.buttons.append(button.TextButton(arrow_buttons_size, [self.portret_name_rect.left-arrow_buttons_gap-arrow_buttons_size[0], self.portret_name_rect.top] , Path(self.sound_pack + "click.wav"), "<", self.buttons_font, self.ui_text, self.ui_bg))
        self.arrow_buttons.buttons.append(button.TextButton(arrow_buttons_size, [self.portret_name_rect.right+arrow_buttons_gap, self.portret_name_rect.top] , Path(self.sound_pack + "click.wav"), ">", self.buttons_font, self.ui_text, self.ui_bg))
        confirm_button_size = [150,35]
        confirm_button_gap = 50
        self.confirm_button = button.TextButton(confirm_button_size, [self.other_ui_rect.left +texture.center_x(confirm_button_size, self.other_ui_rect.size), self.portret_name_rect.top +  confirm_button_gap], Path(self.sound_pack + "click.wav"),"Confirm",self.buttons_font, self.ui_black, self.ui_white)

        # Ui state
        self.PLAY_STATE = "PLAY"
        self.SETTINGS_STATE = "SETTINGS"
        self.ui_state = None
        self.select_color = piece.WHITE
        self.ingame = False

        # Game stuff



        # Delta time
        self.dt = 0
        self.last_time = time.time()

        # Is [-1,-1] if player hasn't clicked this frame, else is click position on surface
        self.click_pos = [-1,-1]

        # Board underlay
        self.board_underlay_size = [40,40]
        self.board_underlay = pygame.Rect([self.board_offset[0]- round(self.board_underlay_size[0]/2), self.board_offset[1]- round(self.board_underlay_size[1]/2)],[(self.board.square_size[0] * 8) + self.board_underlay_size[0], (self.board.square_size[1] * 8)+self.board_underlay_size[1]])

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

    def update_arrow_buttons(self):
        self.arrow_buttons.updates(self.click_pos)
        # Left
        if self.arrow_buttons.buttons[0].pressed == True:
            self.arrow_buttons.buttons[0].pressed = False
            self.player_index -= 1
            if self.player_index <= -self.total_players:
                self.player_index = 0
        # Right
        if self.arrow_buttons.buttons[1].pressed == True:
            self.arrow_buttons.buttons[1].pressed = False
            self.player_index += 1
            if self.player_index >= self.total_players:
                self.player_index = 0

    def update_confirm_button(self):
        self.confirm_button.update(self.click_pos)
        #
        if self.confirm_button.pressed:
            self.confirm_button.pressed = False
            if self.ui_state == self.PLAY_STATE:
                if self.select_color == piece.WHITE:
                    self.confirm_button.change_font_color(self.ui_white)
                    self.confirm_button.change_bg_color(self.ui_black)
                    self.active_players[0] = self.players[self.player_index]

                elif self.select_color == piece.BLACK:
                    self.confirm_button.change_font_color(self.ui_black)
                    self.confirm_button.change_bg_color(self.ui_white)
                    self.active_players[1] = self.players[self.player_index]

                self.select_color += 1
                if self.select_color > 1:
                    self.select_color = 0
                    self.ui_state = None
                    self.ingame = True


    def draw_main_ui(self):
        self.main_ui_buttons.draws(self.surface)

        if self.ui_state == self.PLAY_STATE:
            self.update_arrow_buttons()
            self.update_confirm_button()

            pygame.draw.rect(self.surface, self.ui_secondary, self.other_ui_rect)
            self.surface.blit(self.players[self.player_index].image, self.portret_rect)
            self.portret_name_rect.x =  self.other_ui_rect.left + texture.center_x(self.players[self.player_index].name_surf, self.other_ui_rect.size)
            pygame.draw.rect(self.surface, self.ui_bg, self.portret_underlay)
            self.surface.blit(self.players[self.player_index].image, self.portret_rect)
            self.surface.blit(self.players[self.player_index].name_surf, self.portret_name_rect)
            self.arrow_buttons.draws(self.surface)
            self.confirm_button.draw(self.surface)






        elif self.ui_state == self.SETTINGS_STATE:
            pass

    def is_click_on_board(self) -> bool:
        if self.click_pos[0] >= self.board_offset[0] and self.click_pos[1] >= self.board_offset[1]:
            if self.click_pos[0] <= self.board_bottomright[0] and self.click_pos[1] <= self.board_bottomright[1]:
                return True
        return False
    def update_board(self):
        if isinstance(self.active_players[self.board.board_data.active], player.Human):
            # If click is on board
            if self.is_click_on_board():
                # Please forgive me god
                pos = [-1,-1]
                for i in range(0, self.click_pos[0] - self.board_offset[0], self.board.square_size[0]):
                    pos[0] += 1
                for j in range(0, self.click_pos[1] - self.board_offset[1], self.board.square_size[1]):
                    pos[1] += 1

                self.active_players[self.board.board_data.active].touch(self.board.board_data, engine.Coordinate(pos[1], pos[0]))
        else:
            move =  self.active_players[self.board.board_data.active].move(self.board.board_data)
            if move != None:
                self.board.board_data.apply_move(move)
                



    def maingame(self):
        self.main_ui_buttons.updates(self.click_pos)
        self.update_main_ui()
        if self.ingame:
            self.update_board()


        # Drawing loop
        self.surface.fill(self.ui_bg)
        pygame.draw.rect(self.surface, self.ui_secondary, self.board_underlay)

        selected = None
        legal_moves = []
        if isinstance(self.active_players[self.board.board_data.active], player.Human):
            if self.active_players[self.board.board_data.active].selected != None:
                selected = [self.active_players[self.board.board_data.active].selected]
            legal_moves = self.active_players[self.board.board_data.active].legal_moves

        self.board.draw(self.surface, ((self.board_offset, self.board_offset)), selected, legal_moves)
        self.surface.blit(self.title_surface, self.title_pos)
        self.draw_main_ui()





    def update(self):
        self.state_to_function[self.state]()

    def screen_to_window(self):
        self.win.blit(pygame.transform.scale(
            self.surface, self.win_size), (0, 0))

    def start(self):
        while True:
            self.click_pos =  [-1,-1]
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
