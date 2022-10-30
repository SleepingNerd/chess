import pygame
from texture import center

# Converts pos on window_size (or really just any size) to a pos on dest_size
def convert_window_pos(pos, window_size, dest_size):
    return [round(pos[0] / (window_size[0] /dest_size[0])), round(pos[1] / (window_size[1] /dest_size[1]))]

# Class used to group and manage muiltiple buttons into one object
class ButtonHandler():
    # buttons should be a list containing Button objects
    def __init__(self, buttons):
        self.buttons = buttons
    def updates(self, click_pos):
        if click_pos[0] != None and click_pos[1] != None:
            for button in self.buttons:
                button.update(click_pos)
    def draws(self, dest):
        for button in self.buttons:
                button.draw(dest)


# Button class
class Button:
    # Constructor,
    # Size and pos will determine self.rect,
    # Image will be loaded in, scaled to size and stored in self.image,
    # Sound will be loaded in and played when Button is clicked,
    # Self.pressed is set to false by default
    def __init__(self, size, pos, sound):
        self.rect = pygame.Rect(pos, size)
        self.sound = pygame.mixer.Sound(sound)
        self.image = pygame.Surface(self.rect.size)
        self.pressed = False

    # If click_pos overlaps with self.rect,
    # Invoke self.clicked_function, play self.sound and set self.clicked to true
    def update(self, click_pos):

        # If click position and button rect overlap...
        if self.rect.collidepoint(click_pos):
            # Play self.sound
            self.sound.play()

            # Set self.pressed to true
            self.pressed = True

            # Call my clicked function
            self.clicked_function()

    # Invoked whenever button is pressed
    # Does nothing here, but can be overwritten in a child class
    def clicked_function(self):
        pass

    # Blits self.image on surf at self.rect
    def draw(self, surf):
        surf.blit(self.image, self.rect)

class TextButton(Button):
    def __init__(self, size, pos, sound, text, font, font_color, bg_color, antialiasing=False):
        super().__init__(size, pos, sound) # super(Button, self)
        self.font = font
        self.antialiasing = antialiasing
        self.text = text
        self.font_color = font_color
        self.bg_color = bg_color
        self.redraw_button()


    def redraw_button(self):
        font_surf = self.font.render(self.text, self.antialiasing, self.font_color, self.bg_color)
        self.surf = pygame.Surface(self.rect.size)
        self.surf.fill(self.bg_color)
        self.surf.blit(font_surf, center(font_surf, self.rect.size))

    def draw(self, dest):
        dest.blit(self.surf, self.rect)
    def change_font_color(self, color):
        self.font_color = color
        self.redraw_button()


    def change_bg_color(self, color):
        self.bg_color = color
        self.redraw_button()
