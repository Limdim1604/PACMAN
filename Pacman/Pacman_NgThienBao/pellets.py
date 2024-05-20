
import pygame
from vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    """
    Represents a pellet in the Pacman game.

    Attributes:
        name (str): The name of the pellet.
        position (Vector2): The position of the pellet on the screen.
        color (tuple): The color of the pellet.
        radius (int): The radius of the pellet.
        collideRadius (float): The collision radius of the pellet.
        points (int): The number of points the pellet is worth.
        visible (bool): Indicates whether the pellet is visible or not.
    """

    def __init__(self, row, column):
        """
        Initializes a new instance of the Pellet class.

        Args:
            row (int): The row index of the pellet.
            column (int): The column index of the pellet.
        """
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = (0,250,200)
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = 2 * TILEWIDTH / 16
        self.points = 10
        self.visible = True

    def render(self, screen):
        """
        Renders the pellet on the screen.

        Args:
            screen (pygame.Surface): The surface to render the pellet on.
        """
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)


class PowerPellet(Pellet):
    """
    Represents a power pellet in the Pacman game.

    Attributes:
        row (int): The row index of the power pellet.
        column (int): The column index of the power pellet.
        name (str): The name of the power pellet.
        radius (int): The radius of the power pellet.
        points (int): The number of points awarded for eating the power pellet.
        flashTime (float): The time interval for the power pellet to flash.
        timer (float): The current timer for the power pellet.

    """

    def __init__(self, row, column):
        """
        Initializes a new instance of the PowerPellet class.

        Args:
            row (int): The row index of the power pellet.
            column (int): The column index of the power pellet.
        """
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer= 0

    def update(self, dt):
        """
        Updates the state of the power pellet.

        Args:
            dt (float): The time elapsed since the last update.
        """
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup(object):
    """
    Represents a group of pellets in the game.

    Attributes:
        pelletList (list): A list of all the pellets in the group.
        powerpellets (list): A list of power pellets in the group.
        numEaten (int): The number of pellets eaten.
        ...
    """

    def __init__(self, pelletfile):
        """
        Initializes a new instance of the PelletGroup class.

        Args:
            pelletfile (str): The file path of the pellet data.
        """
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0

    def update(self, dt):
        """
        Updates the state of the pellets.

        Args:
            dt (float): The time elapsed since the last update.
        """
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def createPelletList(self, pelletfile):
        """
        Creates a list of pellets from the pellet data file.

        Args:
            pelletfile (str): The file path of the pellet data.
        """
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        """
        Reads the pellet data from a text file.

        Args:
            textfile (str): The file path of the pellet data.

        Returns:
            numpy.ndarray: The pellet data as a numpy array.
        """
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        """
        Checks if the pellet list is empty.

        Returns:
            bool: True if the pellet list is empty, False otherwise.
        """
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, screen):
        """
        Renders all the pellets on the screen.

        Args:
            screen (pygame.Surface): The surface to render the pellets on.
        """
        for pellet in self.pelletList:
            pellet.render(screen)