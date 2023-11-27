# circle = pygame.draw.circle(screen, (colourRGB), (ball_x, ball_y), radius)
# rect = pygame.draw.rect(screen, (colourRGB), (ball_x, ball_y, width, height)

import os
# Running the program via the Run button in VS Code etc. sometimes causes problems
# where this file cannot access other files in its directory.
# This will set the current working directory to where this Python file is located.
PATH_TO_FILE = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH_TO_FILE)


# Site Imports
try:
    import pygame
    import random
    from playsound import playsound
except ImportError:
    if input("Some packages are not installed, would you like to install them? (y/n): ").lower() == "y":
        import subprocess
        # Install dependencies
        subprocess.run(["pip","install","-r","requirements.txt"])
        import pygame
        import random
        from playsound import playsound
    else:
        quit()

# Local Imports

# Import custom settings file
try:
    from settings import *
except ImportError:
    # Create settings file
    template = open("settings_template.py", 'r') # Open the template
    new_settings = open("settings.py", 'w') # Create the new settings file
    new_settings.write(template.read()) # Copy template to new file
    new_settings.close()
    template.close()
    # Finally, import the newly created file
    from settings import *

# Fail-safe in case the number of balls exceeds the cleanup value
if NUM_BALLS > MAX_BALL_STORAGE:
    raise ValueError("Ball count cannot be greater than the cleanup threshold")

from utils import *

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

# Set clock cycles
clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

class Ball():
    def __init__(self, colour, radius, pos_x, pos_y, vel_x, vel_y):
        self.radius = radius
        self.colour = colour
        self.color = colour
        self.pos_x, self.pos_y = pos_x, pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.collided = False
        self.disabled = False
        self.update()
    
    def update(self):
        # Re-draw the updated circle
        self.rect = pygame.draw.circle(screen, self.colour, (self.pos_x, self.pos_y), self.radius)

class Paddle():
    def __init__(self, colour, pos_x, pos_y, height, width, velocity):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.colour = colour
        self.color = colour
        self.height = height
        self.width = width
        self.velocity = velocity
        self.update()

    def move(self, up, down):
        if up and self.pos_y > 0:
            self.pos_y -= self.velocity

        if down and self.pos_y < SCREEN_HEIGHT - self.height:
            self.pos_y += self.velocity
    
    def update(self):
        self.rect = pygame.draw.rect(screen, self.colour, (self.pos_x, self.pos_y, self.width, self.height))

# Scoring system
score = 0

# Define paddles
paddle_a = Paddle(RED, SCREEN_WIDTH / 30, (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)
paddle_b = Paddle(BLUE, (SCREEN_WIDTH / 30) *29, (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)

def spawn_ball(i):
    balls.append(
        Ball(WHITE, BALL_RADIUS, BALL_START_X, BALL_START_Y, clamp(BALL_VELOCITY + i / 5, 1, MAX_BALL_VELOCITY)*(1 if i%2 == 0 else -1), BALL_VELOCITY/5 + random.randint(-15,15))
    )
    print(f"Created ball at count {i} index {len(balls)}")

# Create balls
ball_counter = 0
balls = []
for i in range(NUM_BALLS):
    # Add ball to list
    spawn_ball(ball_counter)
    ball_counter += 1

space_key_pressed = False
# Run until the user asks to quit
pygame.display.set_caption("Pong Test Game")
pygame.display.update()
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Optimize the ball array by removing ghost (disabled) balls
    if len(balls) > MAX_BALL_STORAGE:
        if CONTINUE_ON_OVERFLOW: # do we want to keep going?
            # remove all disabled balls
            active_balls = [] # Create temporary array to store active balls
            for ball in balls:
                if not ball.disabled:
                    active_balls.append(ball) # Add the active balls into a new array
            print(f"Cleanup: old={len(balls)} new={len(active_balls)}")
            balls = active_balls # Add only active balls into new array
            # Fail-safe in case the number of active balls exceeds the cleanup value
            if len(balls) > MAX_BALL_STORAGE:
                raise RuntimeError("Active ball count cannot be greater than the cleanup threshold")
        else:
            running = False

    # Game close mechanic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keypress detection
    keys = pygame.key.get_pressed()

    # Tell the paddles to process the key inputs
    paddle_a.move(keys[pygame.K_w], keys[pygame.K_s])
    paddle_b.move(keys[pygame.K_UP], keys[pygame.K_DOWN])
    

    if keys[pygame.K_SPACE]:
        if not space_key_pressed:
            spawn_ball(ball_counter)
            ball_counter += 1
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
                playsound("assets/sound/bounce.mp3",False)
        else:
            ball.collided = False

        # Test for boundary collision
        if ball.pos_y >= SCREEN_HEIGHT - ball.radius or ball.pos_y < ball.radius:
            ball.vel_y *= -1
            playsound("assets/sound/bounce.mp3",False)
        if ball.pos_x >= SCREEN_WIDTH - ball.radius or ball.pos_x < ball.radius:
            ball.disabled = True # Turn the ball into a ghost (does not simulate)
            spawn_ball(ball_counter)
            ball_counter += 1

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
