# Check and install required packages if not installed
import os

# Set current working directory to the location of this Python file
PATH_TO_FILE = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH_TO_FILE)

try:
    # Import necessary modules
    import pygame
    import pygame.freetype
    import random

    # Import utility functions
    from utils import *

except ImportError:
    if input("Some packages are not installed, would you like to install them? (y/n): ").lower() == "y":
        import subprocess

        # Install dependencies
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
    print("Done, please run the Python script again")
    quit()

# Import custom settings file
from settings import *

# Ensure the number of balls doesn't exceed the cleanup value
if NUM_BALLS > MAX_BALL_STORAGE:
    raise ValueError("Ball count cannot be greater than the cleanup threshold")

# Define colours
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize PyGame
pygame.init()

# Set clock cycles
clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Define Ball class
class Ball:
    def __init__(self, colour, radius, pos_x, pos_y, vel_x, vel_y):
        self.radius = radius
        self.colour = colour
        self.color = colour
        self.pos_x, self.pos_y = pos_x, pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.collided = False
        self.disabled = False
        self.time_until_move = BALL_START_DELAY
        self.update()

    def update(self):
        # Re-draw the updated circle
        self.rect = pygame.draw.circle(screen, self.colour, (self.pos_x, self.pos_y), self.radius)

# Define Paddle class
class Paddle:
    def __init__(self, colour, pos_x, pos_y, height, width, velocity):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.colour = colour
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

# Create paddles
paddle_a = Paddle(WHITE, SCREEN_WIDTH / 30, (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY)
if PRACTICE_MODE:
    paddle_b = Paddle(
        GREY,
        SCREEN_WIDTH - PADDLE_WIDTH*2,
        0, SCREEN_HEIGHT, PADDLE_WIDTH*2, PADDLE_VELOCITY,
    )
else:
    paddle_b = Paddle(
        WHITE,
        (SCREEN_WIDTH / 30) * 29,
        (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), 
        PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VELOCITY,
    )

# Define function to spawn a ball
def spawn_ball(i):
    balls.append(Ball(WHITE, BALL_RADIUS, BALL_START_X, BALL_START_Y, clamp(BALL_VELOCITY+i, 0, MAX_BALL_VELOCITY) * (-1 if i%2 else 1), BALL_VELOCITY))
    print(f"Created ball at count {i} index {len(balls)-1}")

# Create balls
ball_counter = 0
balls = []
for i in range(NUM_BALLS):
    # Add ball to list
    spawn_ball(ball_counter)
    ball_counter += 1

space_key_pressed = False

# Set window caption
pygame.display.set_caption("Pong Test Game")
pygame.display.update()

# Scoring system
score_a = 0
score_b = 0

# Font Details
font_path = FONT_PATH
font_size = 60  

# Audio Setup
seed = random.choice(list(open('seeds.txt')))
random.seed(seed)

# Define sound file paths
wall_bounce_sound = './assets/sound/bounce.mp3'
paddle_bounce_sound = './assets/sound/paddle_bounce.mp3'

# Define background music list
MUSIC_PATH = './assets/sound/background_audio/'
song_list = os.listdir(MUSIC_PATH)
print('\n'.join(song_list))


# Initialize variables for background music
current_song_index = 0
previous_song = None
cached_music_volume = 0
ears_protected = False

# Define function to shuffle background music
def shuffle_music():
    global current_song_index, previous_song
    while True:
        new_song_index = random.randint(0, len(song_list) - 1)
        if new_song_index != current_song_index:
            current_song_index = new_song_index
            break
    previous_song = song_list[current_song_index]
    return previous_song

# Define function to play wall bounce sound
def play_wall_bounce():
    wall_bounce = pygame.mixer.Sound(wall_bounce_sound)
    wall_bounce.play()

# Define function to play paddle bounce sound
def play_paddle_bounce():
    paddle_bounce = pygame.mixer.Sound(paddle_bounce_sound)
    paddle_bounce.play()

# Set up event for music end
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

# Define function to play background music
def play_background_music(next_song):
    global cached_music_volume, ears_protected, MUSIC_VOLUME
    pygame.mixer.music.load(MUSIC_PATH+next_song)

    if next_song.endswith("erika_ear_damage.mp3") and I_WOULD_PREFER_TO_KEEP_MY_EARS_THANK_YOU_VERY_MUCH:
        cached_music_volume = MUSIC_VOLUME
        ears_protected = True
        MUSIC_VOLUME = 0.02
    elif ears_protected:
        ears_protected = False
        MUSIC_VOLUME = cached_music_volume

    print(f"Now playing: {next_song}")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play()

if MUSIC_CHOICE == True:
    play_background_music(shuffle_music())

elif MUSIC_CHOICE == False:
    pass

else:
    # Display audio popup
    screen.fill(BLACK)
    audio_popup_font = pygame.font.Font(FONT_PATH, 36)
    audio_popup = audio_popup_font.render("Do you want to play backing audio? [y/n]", True, WHITE)
    screen.blit(audio_popup, dest=(center_text(audio_popup.get_width(), SCREEN_WIDTH), SCREEN_HEIGHT // 2 - 50))
    pygame.display.update()

    # Wait for user input to start or skip audio
    pygame.event.clear()
    i = 0
    while i < 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    play_background_music(shuffle_music())
                    i += 1
                elif event.key == pygame.K_n:
                    i += 1
                else:
                    pass

font = pygame.font.Font(font_path, font_size)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Game close mechanic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MUSIC_END:
            play_background_music(shuffle_music())

        # Allow the user to navigate songs by using the ", and . keys (symbolised by the < and > for forwards and backwards)"
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_COMMA:  # Previous song
                current_song_index = (current_song_index - 1) % len(song_list)
                play_background_music(song_list[current_song_index])
            elif event.key == pygame.K_PERIOD:  # Next song
                current_song_index = (current_song_index + 1) % len(song_list)
                play_background_music(song_list[current_song_index])

    # Font Rendering
    if pygame.mixer.music.get_busy(): # check if music is currently playing
        volume_display = font.render(f"{int(MUSIC_VOLUME*100)}%", True, GREY)
        screen.blit(volume_display, dest=(SCREEN_WIDTH-volume_display.get_width(), 0))
    score_display = font.render(f"{score_a} | {score_b}", True, WHITE)
    screen.blit(score_display, dest=(center_text(score_display.get_width(), SCREEN_WIDTH), 0))

    # Optimize the ball array by removing ghost (disabled) balls
    if len(balls) > MAX_BALL_STORAGE:
        if CONTINUE_ON_OVERFLOW:  # do we want to keep going?
            # remove all disabled balls
            active_balls = []  # Create temporary array to store active balls
            for ball in balls:
                if not ball.disabled:
                    active_balls.append(ball)  # Add the active balls into a new array
            print(f"Cleanup: old={len(balls)} new={len(active_balls)}")
            balls = active_balls  # Add only active balls into new array
            # Fail-safe in case the number of active balls exceeds the cleanup value
            if len(balls) > MAX_BALL_STORAGE:
                raise RuntimeError("Active ball count cannot be greater than the cleanup threshold")
        else:
            running = False

    # Keypress detection
    keys = pygame.key.get_pressed()

    # Tell the paddles to process the key inputs
    paddle_a.move(keys[pygame.K_w], keys[pygame.K_s])

    if not PRACTICE_MODE:
        paddle_b.move(keys[pygame.K_UP], keys[pygame.K_DOWN])

    # Change music volume
    if keys[pygame.K_EQUALS] and MUSIC_VOLUME < 1:
        MUSIC_VOLUME += 0.01
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
    
    if keys[pygame.K_MINUS] and MUSIC_VOLUME > 0:
        MUSIC_VOLUME -= 0.01
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

    # Spawn a new ball when the space key is pressed
    if keys[pygame.K_SPACE]:
        if not space_key_pressed:
            spawn_ball(ball_counter)
            ball_counter += 1
            space_key_pressed = True
    else:
        space_key_pressed = False

    # Ball simulation
    for ball in balls:
        # Do not simulate if ball is disabled
        if ball.disabled:
            continue
        
        # Wait until the ball is ready to move
        if ball.time_until_move > 0:
            ball.time_until_move -= 1
            ball.update()
            continue

        # Paddle-ball collision detection
        if ball.rect.collidelist([paddle_a, paddle_b]) != -1:
            if not ball.collided:
                ball.vel_x *= -1
                ball.collided = True
                play_paddle_bounce()
        else:
            ball.collided = False

        # Test for boundary collision
        if ball.pos_y >= SCREEN_HEIGHT - ball.radius or ball.pos_y < ball.radius:
            ball.vel_y *= -1
            play_wall_bounce()

        if ball.pos_x >= SCREEN_WIDTH - ball.radius or ball.pos_x < ball.radius:
            # Increase score for the respective team
            if ball.pos_x >= SCREEN_WIDTH - ball.radius:  # Team B
                score_a += 1
            if ball.pos_x < ball.radius:  # Team A
                score_b += 1

            ball.disabled = True  # Turn the ball into a ghost (does not simulate)
            spawn_ball(ball_counter)
            ball_counter += 1
            print(f"SCORES: {score_a} : {score_b}")

        # Move the ball
        ball.pos_x += ball.vel_x
        ball.pos_y += ball.vel_y

        # Update positions
        ball.update()

    # Update paddle positions
    paddle_a.update()
    paddle_b.update()

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
