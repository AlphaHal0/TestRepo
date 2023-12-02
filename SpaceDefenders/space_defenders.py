# Import settings and constants
from config import *
try:
    # Import necessary modules
    import os
    import pygame
    import pygame.freetype
    import random
except ImportError:
    if input("Some packages are not installed, would you like to install them? (y/n): ").lower() == "y":
        import subprocess

        # Install dependencies
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
        print("Done, please run the Python script again")
    quit()

# Set current working directory to the location of this Python file
PATH_TO_FILE = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH_TO_FILE)

# Initialize PyGame
pygame.init()

# Set core data
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set window caption
pygame.display.set_caption("Space Defenders Test Game")
pygame.display.update()

# Class Definitions:
class Entity:
    def __init__(self, shape, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 4, velocity=15, health=100, max_health=100, base_damage=10, w=None, h=None, r=None, colour=WHITE):
        self.shape = shape
        self.x = x
        self.y = y
        self.velocity = velocity
        self.health = health
        self.max_health = max_health
        self.base_damage = base_damage
        self.w = w
        self.h = h
        self.r = r
        self.colour = colour
        self.update()

    def update(self):
        if self.shape == "rect":
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h))
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r)

class Player(Entity):
    def __init__(self, x=None, y=None, health=100, max_health=100):
        super().__init__("rect", health=health, max_health=max_health, w=100, h=100)
        # only override values if x and y have been specified
        if x: self.x = x
        if y: self.y = y
        self.health = health
        self.max_health = max_health

    def move(self, left, right):
        if left and self.x > 0:
            self.x -= self.velocity
            
        if right and self.x < SCREEN_WIDTH - self.w:
            self.x += self.velocity

class Enemy(Entity):
    def __init__(self, x=None, y=None, health=10, max_health=10):
        super().__init__("rect", health=health, max_health=max_health, w=10, h=10)
        if x: self.x = x
        if y: self.y = y
        self.health = health
        self.max_health = max_health

class Meteor(Entity):
    def __init__(self, x, y):
        super().__init__("circle", r=10)
        self.x = x
        self.y = y

def core_functions():
    clock.tick(FPS)
    screen.fill(BLACK)

def player_controls():
    # Store user keypresses
    keys = pygame.key.get_pressed()

    # Tell player to process key input
    player.move(
        (keys[pygame.K_a] + keys[pygame.K_LEFT]),
        (keys[pygame.K_d] + keys[pygame.K_RIGHT])
    )
    player.update()

# Spawn Player
player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 0.85), 100, 100)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    core_functions()
    player_controls()


    # Update the display
    pygame.display.update()

pygame.quit()