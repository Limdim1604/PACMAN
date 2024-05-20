
import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

class Fruit(Entity):
    """A class representing a fruit entity in the Pacman game.

    Attributes:
        node (Node): The node where the fruit is located.
        level (int): The level of the game.
        name (str): The name of the fruit.
        color (tuple): The color of the fruit.
        lifespan (int): The lifespan of the fruit in seconds.
        timer (float): The timer to track the lifespan of the fruit.
        destroy (bool): Flag indicating if the fruit should be destroyed.
        points (int): The points awarded for collecting the fruit.
        sprites (FruitSprites): The sprites representing the fruit.

    """

    def __init__(self, node, level=0):
        """Initialize a Fruit object.

        Args:
            node (Node): The node where the fruit is located.
            level (int, optional): The level of the game. Defaults to 0.

        """
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100 + level * 20
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        """Update the state of the fruit over time.

        Args:
            dt (float): The time elapsed since the last update.

        """
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True