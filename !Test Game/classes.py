class Text:
    def __init__(self, screen, font, text, colour=None, x=None, y=None, size=None):
        if colour is None: colour = (255, 255, 255)
        if x is None: x = 0
        if y is None: y = 0
        if size is None: size = 45

        self.screen = screen
        self.surface = font.render(text, True, colour, size)
        self.display(x, y)

    def display(self, x, y):
        self.screen.blit(self.surface, dest=(x, y))

class Player:
    def __init__(self, x, y, size, screen):
        self.x = x
        self.y = y
        self.size = size
    
    def move(self, direction):
        if direction == "up":
            pass
