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

class Player:
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.screen = screen
    
    def move(self, direction):
        width, height = self.screen.get_size()
        if direction == "up":
            self.y -= self.speed
            if self.y-(self.height/2) < 0:
                self.y = self.height/2
        elif direction == "down":
            self.y += self.speed
            if self.y+(self.height/2) > height:
                self.y = height-self.height/2
                
    def display(self):
        pygame.draw.rect(self.screen,(255, 0, 0), 
                        [self.x+(self.width/2),
                        self.y-(self.height/2), 
                        self.width, self.height], 0)