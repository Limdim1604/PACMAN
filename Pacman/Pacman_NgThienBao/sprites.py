
import pygame
import numpy as np
from animation import Animator
from constants import *

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    """A class representing a spritesheet"""

    def __init__(self):
        """Initialize the Spritesheet object."""
        self.sheet = pygame.image.load("Pacman_NgThienBao/spritesheet_pacman2.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def getImage(self, x, y, width, height):
        """Get a specific image from the spritesheet.

        Args:
            x (int): The x-coordinate of the top-left corner of the image.
            y (int): The y-coordinate of the top-left corner of the image.
            width (int): The width of the image.
            height (int): The height of the image.
            
        Returns:
            pygame.Surface: The image from the spritesheet.
        """
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacmanSprites(Spritesheet):
    """Class representing the sprites for Pacman entity."""
    
    def __init__(self, entity):
        """Initialize the PacmanSprites object.
        
        Args:
            entity: The Pacman entity.
        """
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()         
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def defineAnimations(self):
        """Define the animations for Pacman's movement directions."""
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    def update(self, dt):
        """Update the image of the Pacman entity based on its current state and direction.
        
        Args:
            dt (float): The time elapsed since the last update.
        """
        if self.entity.alive == True:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == STOP:
                self.entity.image = self.getImage(*self.stopimage)
        else:
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        """Reset all animations to their initial state."""
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        """Get the starting image for Pacman."""
        return self.getImage(8, 0)

    def getImage(self, x, y):
        """Get a specific image for Pacman.
        
        Args:
            x (int): The x-coordinate of the top-left corner of the image.
            y (int): The y-coordinate of the top-left corner of the image.
            
        Returns:
            pygame.Surface: The image for Pacman.
        """
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class GhostSprites(Spritesheet):
    """Class representing the sprites for the ghosts."""
    
    def __init__(self, entity):
        """Initialize the GhostSprites object.
        
        Args:
            entity: The ghost entity.
        """
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()

    def update(self, dt):
        """Update the image of the ghost entity based on its current state and direction.
        
        Args:
            dt (float): The time elapsed since the last update.
        """
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.getImage(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(8, 4)
               
    def getStartImage(self):
        """Get the starting image for the ghost."""
        return self.getImage(self.x[self.entity.name], 4)

    def getImage(self, x, y):
        """Get a specific image for the ghost.
        
        Args:
            x (int): The x-coordinate of the top-left corner of the image.
            y (int): The y-coordinate of the top-left corner of the image.
            
        Returns:
            pygame.Surface: The image for the ghost.
        """
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class FruitSprites(Spritesheet):
    """Class representing the sprites for the fruits."""
    
    def __init__(self, entity, level):
        """Initialize the FruitSprites object.
        
        Args:
            entity: The fruit entity.
            level (int): The current level of the game.
        """
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        self.entity.image = self.getStartImage(level % len(self.fruits))

    def getStartImage(self, key):
        """Get the starting image for the fruit.
        
        Args:
            key (int): The key to select the starting image.
            
        Returns:
            pygame.Surface: The starting image for the fruit.
        """
        return self.getImage(*self.fruits[key])

    def getImage(self, x, y):
        """Get a specific image for the fruit.
        
        Args:
            x (int): The x-coordinate of the top-left corner of the image.
            y (int): The y-coordinate of the top-left corner of the image.
            
        Returns:
            pygame.Surface: The image for the fruit.
        """
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class LifeSprites(Spritesheet):
    """Class representing the sprites for the lives."""
    
    def __init__(self, numlives):
        """Initialize the LifeSprites object.
        
        Args:
            numlives (int): The number of lives.
        """
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        """Remove an image from the list of life images."""
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        """Reset the life images based on the number of lives.
        
        Args:
            numlives (int): The number of lives.
        """
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))

    def getImage(self, x, y):
        """Get a specific image for the life.
        
        Args:
            x (int): The x-coordinate of the top-left corner of the image.
            y (int): The y-coordinate of the top-left corner of the image.
            
        Returns:
            pygame.Surface: The image for the life.
        """
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class MazeSprites(Spritesheet):
    """Class representing the sprites for the maze."""
    
    def __init__(self, mazefile, rotfile):
        """Initialize the MazeSprites object.
        
        Args:
            mazefile (str): The file path of the maze file.
            rotfile (str): The file path of the rotation file.
        """
        Spritesheet.__init__(self)
        self.data = self.readMazeFile("Pacman_NgThienBao/" + mazefile)
        self.rotdata = self.readMazeFile("Pacman_NgThienBao/" + rotfile)

    def getImage(self, x, y):
        """Get a specific image for the maze.
        
        Args:
            x (int): The x-coordinate of the top-left corner of the image.
            y (int): The y-coordinate of the top-left corner of the image.
            
        Returns:
            pygame.Surface: The image for the maze.
        """
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile):
        """Read the maze file and return the maze data as a numpy array.
        
        Args:
            mazefile (str): The file path of the maze file.
            
        Returns:
            numpy.ndarray: The maze data as a numpy array.
        """
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        """Construct the background for the game screen based on the maze data.
        
        Args:
            background (pygame.Surface): The surface to draw the background on.
            y (int): The y-coordinate of the background.
            
        Returns:
            pygame.Surface: The updated background surface.
        """
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background

    def rotate(self, sprite, value):
        """Rotate the given sprite by the specified value.
        
        Args:
            sprite (pygame.Surface): The sprite to rotate.
            value (int): The rotation value in multiples of 90 degrees.
            
        Returns:
            pygame.Surface: The rotated sprite.
        """
        return pygame.transform.rotate(sprite, value*90)
