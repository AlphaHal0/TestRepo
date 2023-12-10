import pygame
from settings import *
from classes import Player, ObstacleHandler, Text
from functions import core_functions

# Set fundamentals
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.Font(None, 256)

# Declare game stuff
player = Player(200, 200, 20, 20, screen)
obstacle_handler = ObstacleHandler(screen)
scene = "GAME"

# Main runtime
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and scene == "DEAD":
            # If enter key is pressed and you are dead restart the game.
            player = Player(200, 200, 20, 20, screen)
            obstacle_handler = ObstacleHandler(screen)
            scene = "GAME"


    core_functions(screen, clock, FPS)
    if scene == "GAME":
        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            player.move("down")
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        
        # Draw the obstacle
        obstacle_handler.move_obstacles()
        obstacle_handler.display_obstacles()

        # Check for collisions
        if pygame.Rect.collidelist(player.rect, obstacle_handler.obstacles) != -1:
            scene = "DEAD"
            continue
        
        # Check for border collision and display the player
        player.border_collision_check()
        player.display()
    elif scene == "DEAD":
        text = Text(screen, (255, 0, 0), 45)
        text.display("you died", 100, 100)
        text.display("you are worthless", 100, 200)
        text.display("enter to restart", 100, 300)
    
    # Update the display
    pygame.display.update()

pygame.quit()