# Button class
class Button:
    # Constructor,
    # Size and pos will determine self.rect,
    # Image will be loaded in, scaled to size and stored in self.image,
    # Sound will be loaded in and played when Button is clicked,
    # Self.clicked is set to false by default
    def __init__(self, size, pos, sound):
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.sound = pygame.mixer.Sound(sound)
        self.image = pygame.Surface((0,0))
        self.clicked = False

    # If click_pos overlaps with self.rect,
    # Invoke self.clicked_function, play self.sound and set self.clicked to true
    def update(self, click_pos):
        # If click position and button rect overlap...
        if self.rect.collidepoint(click_pos):
            # Play self.sound
            self.sound.play()

            # Set self.clicked to true
            self.clicked = True

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
    def __init_(self, size, pos, sound, text, font, textcolor, color):
        super().init(self, size, pos, sound)
        self.font = pygame.font.Font(font, 125)
        self.font_surf = self.start_font.render(text, True, textcolor)
