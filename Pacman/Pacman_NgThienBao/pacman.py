
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    """Class representing the Pacman entity in the game.

    Attributes:
        node (Node): The current node that Pacman is on.
        name (str): The name of the entity.
        color (tuple): The color of the entity.
        direction (Vector2): The current direction of movement.
        alive (bool): Indicates if Pacman is alive or not.
        sprites (PacmanSprites): The sprite manager for Pacman.

    """

    def __init__(self, node):
        """Initialize Pacman with the given node.

        Args:
            node (Node): The starting node for Pacman.

        """
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        """Reset Pacman to its initial state."""
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        """Handle Pacman's death."""
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        """Update Pacman's position.

        Args:
            dt (float): The time elapsed since the last update.

        """
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        """Check which key is pressed.

        Returns:
            int: The direction corresponding to the pressed key.

        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        """Check if Pacman is eating any pellets.

        Args:
            pelletList (list): List of pellets in the game.

        Returns:
            Pellet or None: The pellet that Pacman is eating, or None if no pellet is being eaten.

        """
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        """Check if Pacman is colliding with a ghost.

        Args:
            ghost (Ghost): The ghost to check collision with.

        Returns:
            bool: True if Pacman is colliding with the ghost, False otherwise.

        """
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        """Check if Pacman is colliding with another entity.

        Args:
            other (Entity): The other entity to check collision with.

        Returns:
            bool: True if Pacman is colliding with the other entity, False otherwise.

        """
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False
