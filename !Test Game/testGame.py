import pygame

from settings import *
from classes import *
from functions import *

FPS = 60

# Set fundamentals
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

font = pygame.font.Font(None, 256)

running = True
while running:
    core_functions(screen, clock, FPS)
    
    # Game close mechanic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Text(screen, font, "amogus", x=10,y=20)
    
    screen.update()

pygame.quit()
