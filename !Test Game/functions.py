import pygame
from settings import *

def core_functions(screen, clock, fps):
    clock.tick(fps)
    screen.fill((0,0,0))





# Debug Functions
def debug_player(player):
    print(f"""{player.x=}, {player.y=}
{player.width=}, {player.height=}""")
    
def debug_input(keys, player):
    if keys[pygame.K_DOWN]:
        print("Attempt down")
    if keys[pygame.K_UP]:
        print("Attempt up")
    if keys[pygame.K_LEFT]:
        print("Attempt left")
    if keys[pygame.K_RIGHT]:
        print("Attempt right")