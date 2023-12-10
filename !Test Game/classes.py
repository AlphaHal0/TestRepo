import pygame
from settings import *
from random import randint

class Text:
    def __init__(self, screen, colour, size, font=None):
        if font is None: font = pygame.font.Font(None, size)

        self.colour = colour
        self.size = size
        self.font = font
        self.screen = screen

    def display(self, text, x, y):
        surface = self.font.render(text, True, self.colour, self.size)
        self.screen.blit(surface, dest=(x, y))

# Base class from which all entities are subclassed.
class Entity:
    def __init__(self, x, y, width, height, screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.screen = screen
    
    # Function to run collisions with borders of the screen
    def border_collision_check(self):
        # Get window dimensions
        width, height = self.screen.get_size()

        # Run collision checks and adjust co-ordinates as necessary
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y+self.rect.height > height:
            self.rect.y = height-self.rect.height
        
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x+self.rect.width > width:
            self.rect.x = width-self.rect.width
    

# Player class
class Player(Entity):
    def __init__(self, x, y, width, height, screen):
        super().__init__(x, y, width, height, screen)
        self.speed = 2.5
    
    # Function to handle player movement
    def move(self, direction):
        if direction == "up": self.rect.move_ip(0, -self.speed)
        if direction == "down": self.rect.move_ip(0, self.speed)
        if direction == "left": self.rect.move_ip(-self.speed, 0)
        if direction == "right": self.rect.move_ip(self.speed, 0)

    # Function to display player
    def display(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)


# Handler for obstacles
class ObstacleHandler:
    def __init__(self, screen):
        width, height = screen.get_size()
        self.obstacles = []
        self.obstacle_speed = 1
        self.obstacle_height = height*0.02
        self.obstacle_start_y = height*0.2
        self.screen = screen

        # Minimums and maximums
        self.GAPS_WIDTH = (int(width*0.1), int(width*0.2))

        # Bootstrap the obstacles array
        self.generate_new_obstacles(-height*0.25)
        self.generate_new_obstacles(-height*0.50)
        self.generate_new_obstacles(-height*0.75)
        self.generate_new_obstacles(-height*1)

    
    def move_obstacles(self):
        """
        Move all of the obstacles downwards, and handle them if they go off screen. Also calls on generate_new_obstacles.
        """
        new_obstacles = []  # New list of obstacles that haven't gone below the screen.

        # Iterate and move each obstacle and remove if the go below the screen
        obstacle_went_off_screen = False # Whether an obstacle went off screen
        for i, obstacle in enumerate(self.obstacles):
            obstacle.move_ip(0, self.obstacle_speed)
            obstacle = self.obstacles[i] # Update the obstacle variable

            # If it hasn't gone off the screen, add it to the new_obstacles list
            if obstacle.y < self.screen.get_size()[1]+obstacle.height:
                new_obstacles.append(obstacle)
            else:
                obstacle_went_off_screen = True
        
        self.obstacles = new_obstacles

        # If some obstacles went off the screen, add a new layer.
        if obstacle_went_off_screen:
            self.generate_new_obstacles(-self.obstacle_height)
    
    def display_obstacles(self):
        """
        Draw all of the obstacles in the handler.
        """
        for rect in self.obstacles:
            pygame.draw.rect(self.screen, (0, 255, 0), rect)
        
    
    def generate_new_obstacles(self, y):
        """
        Generate a new layer of obstacles.
        Each layer of obstacles has 2 gaps where the player can go through. Each gap is generated randomly and
            they may intersect. Each gap has a width from 1/20 to 1/10 of the screen width.
        """

        # Generate the gaps.
        gaps = []
        for _ in range(2):
            gap_start = randint(0, self.screen.get_size()[0])
            gaps.append([gap_start, gap_start+randint(*self.GAPS_WIDTH)])
        
        # Now, make the borders around the gaps. Sort them by starting point and then create blocks between them
        gaps = sorted(gaps, key=lambda x: x[0])
        blocks = []
        current_point = 0 # Current point that the next block will start at
        for gap in gaps:
            # Only add if the gap is in front of you (if they intersect it will be behind.)
            if gap[0] > current_point:
                blocks.append([current_point, gap[0]])
            current_point = gap[1]
        
        # Add another block to fill in until the end if it hasnt been reached
        width = self.screen.get_size()[0]
        if current_point < width:
            blocks.append([current_point, width])
        
        # Add the obstacles to self.obstacles as Rect objects
        for block in blocks:
            self.obstacles.append(pygame.Rect(block[0], y, block[1]-block[0], self.obstacle_height))

