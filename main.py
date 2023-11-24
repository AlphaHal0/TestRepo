# Import and initialize the pygame library
import pygame

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialise PyGame
pygame.init()

# Constants for game
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Run until the user asks to quit
running = True
while running:
    clock.tick(FPS)

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    circle = pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    for event in pygame.event.get():
        # Game close mechanic
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            # Movement Mechanic
            if event.key == pygame.K_w:
                circle.move_ip(0, -2)
        

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()