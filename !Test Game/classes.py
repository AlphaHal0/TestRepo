import pygame
from settings import *

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

# Base class from which all entities are subclassed.
class Entity:
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
    
    # Function to run collisions with borders of the screen
    def border_collision_check(self):
        # Get window dimensions
        width, height = self.screen.get_size()

        # Run collision checks and adjust co-ordinates as necessary
        if self.y < 0:
            self.y = 0
        elif self.y+self.height > height:
            self.y = height-self.height
        
        if self.x < 0:
            self.x = 0
        elif self.x+self.width > width:
            self.x = width-self.width
    
    def get_rect(self):
        """
        Function to return the entity as a pygame.Rect object.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
    

# Player class
class Player(Entity):
    def __init__(self, x, y, width, height, screen):
        super().__init__(x, y, width, height, screen)
        self.speed = 5
    
    # Function to handle player movement
    def move(self, direction):
        if direction == "up": self.y -= self.speed
        if direction == "down": self.y += self.speed
        if direction == "left": self.x -= self.speed
        if direction == "right": self.x += self.speed

    # Function to display player
    def display(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.get_rect())

