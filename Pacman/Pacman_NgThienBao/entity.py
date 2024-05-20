import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity(object):
    """Represents an entity in the game, useful for Ghosts to chase Pacman.
    Attributes:
        name (str): The name of the entity.
        directions (dict): A dictionary mapping direction constants to Vector2 objects representing the direction vectors.
        direction (int): The current direction of the entity.
        speed (float): The speed of the entity in pixels per second.
        radius (int): The radius of the entity's circle.
        collideRadius (int): The radius used for collision detection.
        color (tuple): The color of the entity.
        visible (bool): Indicates whether the entity is visible or not.
        disablePortal (bool): Indicates whether the entity can pass through portals or not.
        goal (Vector2): The goal position of the entity.
        directionMethod (function): The method used to determine the next direction of the entity.
        node (Node): The current node the entity is on.
        startNode (Node): The starting node of the entity.
        target (Node): The target node the entity is moving towards.
        position (Vector2): The current position of the entity.
        image (Surface): The image used to represent the entity.
    """

    def __init__(self, node):
        """Initializes a new instance of the Entity class.

        Args:
            node (Node): The starting node of the entity.
        """
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        """Sets the position of the entity to the position of the current node."""
        self.position = self.node.position.copy()

    def update(self, dt):
        """Updates the position of the entity based on its current direction and speed.

        Args:
            dt (float): The time elapsed since the last update in seconds.
        """
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def validDirection(self, direction):
        """Checks if the given direction is a valid direction for the entity to move in.

        Args:
            direction (int): The direction to check.

        Returns:
            bool: True if the direction is valid, False otherwise.
        """
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        """Gets the new target node for the entity based on the given direction.

        Args:
            direction (int): The direction to move in.

        Returns:
            Node: The new target node.
        """
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        """Checks if the entity has overshot its target node.

        Returns:
            bool: True if the entity has overshot its target, False otherwise.
        """
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        """Reverses the direction of the entity and swaps the current node and target node."""
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        """Checks if the given direction is opposite to the current direction of the entity.

        Args:
            direction (int): The direction to check.

        Returns:
            bool: True if the direction is opposite, False otherwise.
        """
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def validDirections(self):
        """Gets the valid directions for the entity to move in.

        Returns:
            list: A list of valid directions.
        """
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        """Chooses a random direction from the given list of directions.

        Args:
            directions (list): A list of valid directions.

        Returns:
            int: The randomly chosen direction.
        """
        return directions[randint(0, len(directions)-1)]

    def goalDirection(self, directions):
        """Chooses a direction based on the goal for the entity.

        Args:
            directions (list): A list of valid directions.

        Returns:
            int: The chosen direction based on the goal.
        """
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    def setStartNode(self, node):
        """Sets the starting node of the entity.

        Args:
            node (Node): The starting node.
        """
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        """Sets the position between two nodes for the entity.

        Args:
            direction (int): The direction of movement.
        """
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        """Resets the entity to its initial state."""
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        """Sets the speed of the entity.

        Args:
            speed (float): The speed in pixels per second.
        """
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        """Renders the entity on the screen.

        Args:
            screen (Surface): The surface to render on.
        """
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)
