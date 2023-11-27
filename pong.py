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
    K_SPACE,
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
BALL_RADIUS = 16

# Ball start position
BALL_START_X = 960
BALL_START_Y = 540

# Ball velocity
BALL_VELOCITY = 5

PADDLE_HEIGHT = 200
PADDLE_WIDTH = 30
PADDLE_VELOCITY = 15


class Ball():
    def __init__(self, colour, radius, pos_x, pos_y, vel_x, vel_y):
        self.radius = radius
        self.colour = colour
        self.pos_x, self.pos_y = pos_x, pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.collided = False
        self.disabled = False
        self.update()
    
    def update(self):
        #print(f"{self.pos_x}, {self.pos_y}")
        #self.rect = pygame.draw.circle(screen, self.colour, (self.pos_x, self.pos_y), self.radius)
        self.rect = pygame.draw.circle(screen, self.colour, (self.pos_x, self.pos_y), self.radius)

class Paddle():
    def __init__(self, pos_x, pos_y, height, width, velocity):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.colour = WHITE
        self.height = height
        self.width = width
        self.velocity = velocity
        self.update()
        # rect = pygame.draw.rect(screen, (colourRGB), (ball_x, ball_y, width, height)
    
    def update(self):
        #self.rect = pygame.draw.rect(screen, WHITE, (self.pos_x, self.pos_y, 10, 100))
        self.rect = pygame.draw.rect(screen, WHITE, (self.pos_x, self.pos_y, self.width, self.height))

def spawn_ball(i):
    print(f"Created ball at index {i}")
    balls.append(
        Ball(WHITE, BALL_RADIUS, BALL_START_X, BALL_START_Y, (BALL_VELOCITY + random.randint(0,i))*(1 if i%2 == 0 else -1), BALL_VELOCITY/5 + random.randint(-20,20))
    )

# Scoring system
score = 0

paddle_a = Paddle(SCREEN_WIDTH / 30, (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)
paddle_b = Paddle((SCREEN_WIDTH / 30) *29, (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)

# Create balls
balls = []
for i in range(NUM_BALLS):
    # Add ball to list
    spawn_ball(i)

space_key_pressed = False
# Run until the user asks to quit
pygame.display.set_caption("Pong Test Game")
pygame.display.update()
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

    if keys[pygame.K_SPACE]:
        if not space_key_pressed:
            spawn_ball(len(balls))
            space_key_pressed = True
    else:
        space_key_pressed = False

    for ball in balls:
        # Do not simulate if ball is disabled
        if ball.disabled:
            continue

        # Paddle-ball collision detection
        if ball.rect.collidelist([paddle_a,paddle_b]) != -1:
            if not ball.collided:
                ball.vel_x *= -1
                ball.collided = True
        else:
            ball.collided = False
        
        # Test for boundary collision
        if ball.pos_y >= SCREEN_HEIGHT - ball.radius or ball.pos_y < ball.radius:
            ball.vel_y *= -1
        if ball.pos_x >= SCREEN_WIDTH - ball.radius or ball.pos_x < ball.radius:
            ball.disabled = True

        # Move the ball
        ball.pos_x += ball.vel_x
        ball.pos_y += ball.vel_y

        # Update positions
        ball.update()
    paddle_a.update() 
    paddle_b.update()

    # Update the display
    pygame.display.update()

pygame.quit()
