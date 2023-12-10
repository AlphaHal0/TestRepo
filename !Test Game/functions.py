import pygame
from settings import *

def core_functions(screen, clock, fps):
    clock.tick(fps)
    screen.fill((0,0,0))

# def check_range_intersections(ranges):
#     """
#     Takes a list of ranges in the format [min, max] and checks if any overlap. If so, it merges them and then returns the final array.
#     The algorithim:
#     - Sort the list
#     - Go through each item past you and check if any of it's points is within your two points
#     """
#     new_ranges = ranges
#     for range in ranges:
#         for crange in new_ranges:
#             if range[0] <= crange[0] <= range[1] or range[0] <= crange[1] <= range[1]:




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