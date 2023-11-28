# ------------------------------------------------------------------------- #
# DO NOT EDIT THE TEMPLATE FILE UNLESS YOU ARE CHANGING THE DEFAULT OPTIONS #
# ------------------------------------------------------------------------- #
# Constants for game

# Settings file version
VERSION = 6

# Display settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
FONT_PATH = "assets/font/default.ttf"

# Number of balls to create
NUM_BALLS = 1

# When to remove disabled balls in the array
MAX_BALL_STORAGE = 16
# Whether to continue (True) or end (False) the game once above value is met
CONTINUE_ON_OVERFLOW = True

# Ball dimensions
BALL_RADIUS = 8

# Ball start position
BALL_START_X = 960
BALL_START_Y = 540

# Initial ball velocity
BALL_VELOCITY = 8
BALL_START_DELAY = 30

# Maximum possible velocity of the ball
MAX_BALL_VELOCITY = BALL_VELOCITY

# Paddle options
PADDLE_HEIGHT = 150
PADDLE_WIDTH = 10
PADDLE_VELOCITY = 20

# Only use one paddle
PRACTICE_MODE = False

# Audio settings
MUSIC_VOLUME = 0.8 # value from 0.0 to 1.0
MUSIC_CHOICE = None # set to True or False to select music choice
I_WOULD_PREFER_TO_KEEP_MY_EARS_THANK_YOU_VERY_MUCH = False
