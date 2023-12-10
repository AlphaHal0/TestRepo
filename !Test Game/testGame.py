import pygame
from settings import *
from classes import Player
from functions import core_functions

# Set fundamentals
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.Font(None, 256)

# Declare game stuff
player = Player(200, 200, 20, 20, screen)
obstacles = [pygame.Rect(210, 210, 50, 50)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    core_functions(screen, clock, FPS)
    
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
    for rect in obstacles:
        pygame.draw.rect(screen, (0, 255, 0), rect)

    # Check for collisions
    if (index := pygame.Rect.collidelist(player.get_rect(), obstacles)) != -1:
        pygame.draw.rect(screen, (255, 0, 0), obstacles[index])
    
    # Check for border collision and display the player
    player.border_collision_check()
    player.display()
    
    # Update the display
    pygame.display.update()

pygame.quit()