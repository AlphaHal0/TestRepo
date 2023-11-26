# circle = pygame.draw.circle(screen, (colourRGB), (ball_x, ball_y), radius)
# rect = pygame.draw.rect(screen, (colourRGB), (ball_x, ball_y, width, height)


# Import and initialize the pygame library
import pygame
import random

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

# Set clock cycles
clock = pygame.time.Clock()
FPS = 60

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Number of balls to create
NUM_BALLS = 1

# Ball dimensions
BALL_RADIUS = 8

# Ball start position
BALL_START_X = 960
BALL_START_Y = 540

# Ball velocity
BALL_VELOCITY = 5
BALL_VEL_X = BALL_VELOCITY
BALL_VEL_Y = BALL_VELOCITY

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 10
PADDLE_VELOCITY = 15


class Ball():
    def __init__(self, colour, radius, pos_x, pos_y, vel_x, vel_y):
        self.radius = radius
        self.rect = pygame.draw.circle(screen, colour, (pos_x, pos_y), radius)
        self.colour = colour
        self.pos_x, self.pos_y = pos_x, pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        print("Created ball")
    
    def update(self):
        print(f"{self.pos_x}, {self.pos_y}")
        self.rect = pygame.draw.circle(screen, self.colour, (self.pos_x, self.pos_y), self.radius)

class Paddle(pygame.Rect):
    def __init__(self, id, pos_x, pos_y, height, width, velocity):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = height
        self.width = width
        self.velocity = velocity
        # rect = pygame.draw.rect(screen, (colourRGB), (ball_x, ball_y, width, height)
        self.rect = pygame.draw.rect(screen, WHITE, (pos_x, pos_y, 10, 100))
    
    def update(self):
        print(f"{self.pos_x}, {self.pos_y}")
        self.rect = pygame.draw.rect(screen, WHITE, (self.pos_x, self.pos_y, 10, 100))



# paddle_b_x = (SCREEN_WIDTH / 30) * 29
# paddle_b_y = SCREEN_HEIGHT / 2



# Scoring system
score = 0



paddle_a = Paddle(1, SCREEN_WIDTH / 30, SCREEN_HEIGHT / 2, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)
paddle_b = Paddle(2, (SCREEN_WIDTH / 30) *29, SCREEN_HEIGHT / 2, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)

ball = Ball(WHITE, BALL_RADIUS, BALL_START_X, BALL_START_Y, BALL_VEL_X, BALL_VEL_Y)



# Run until the user asks to quit
pygame.display.set_caption("Pong Test Game")

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Game close mechanic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keypress detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.pos_y > 0:
        paddle_a.pos_y -= paddle_a.velocity
    if keys[pygame.K_s] and paddle_a.pos_y < 1080 - paddle_a.height:
        paddle_a.pos_y += paddle_a.velocity

    if keys[pygame.K_UP] and paddle_b.pos_y > 10:
        paddle_b.pos_y -= paddle_b.velocity

    if keys[pygame.K_DOWN] and paddle_b.pos_y < 1080 - paddle_a.height:
        paddle_b.pos_y += paddle_b.velocity

    # Move ball

    # Ball border detection
    #for ball in balls:
    ball.pos_x += ball.vel_x
    ball.pos_y += ball.vel_y
    if ball.pos_y >= SCREEN_HEIGHT - ball.radius or ball.pos_y < ball.radius:
        ball.vel_y *= -1
    if ball.pos_x >= SCREEN_WIDTH - ball.radius or ball.pos_x < ball.radius:
        ball.vel_x *= -1

    # Paddle-ball collision detection
    if paddle_a.pos_y == ball.pos_y and paddle_a.pos_x == ball.pos_x:
        ball.vel_y *= -1

    # Update positions
    ball.update()  
    paddle_a.update() 
    paddle_b.update()


    # Update the display
    pygame.display.update()



pygame.quit()

# Create balls
# balls = []
# for i in range(NUM_BALLS):
#     # Add ball to list
#     balls.append(
#         Ball(
#             WHITE,
#             BALL_RADIUS,
#             BALL_START_X,
#             BALL_START_Y,
#             i+5,
#             1 if i%2 == 0 else -1 # this looks stupid, but it's just me messing around and will be removed
#         )
#     )