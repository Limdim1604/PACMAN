import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites

class Ghost(Entity):
    """
    Represents a ghost in the game.

    Attributes:
        node (Node): The starting node of the ghost.
        pacman (Pacman): The Pacman object in the game.
        blinky (Blinky): The Blinky ghost object, used by Inky for chasing.
        name (str): The name of the ghost.
        points (int): The points awarded to Pacman for eating the ghost in Freight mode.
        goal (Vector2): The target position for the ghost.
        directionMethod (function): The method used to determine the ghost's direction.
        mode (ModeController): Manages the ghost's current mode (e.g., Scatter, Chase, Freight).
        homeNode (Node): The node the ghost returns to after being eaten.
        spawnNode (Node): The node from which the ghost spawns.
        sprites (GhostSprites): The sprite object for the ghost.
    """

    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes a Ghost object.

        Args:
            node (Node): The starting node of the ghost.
            pacman (Pacman): The Pacman object in the game.
            blinky (Blinky): The Blinky ghost object.
        """
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        """
        Resets the ghost to its initial state.
        """
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        """
        Updates the ghost's state every frame.

        Args:
            dt (float): Time elapsed since the last frame.
        """
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        """
        Sets the ghost's target position for the Scatter mode.
        """
        self.goal = Vector2() 

    def chase(self):
        """
        Sets the ghost's target position for the Chase mode.
        """
        self.goal = self.pacman.position

    def spawn(self):
        """
        Sets the ghost's target position for the Spawn mode.
        """
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        """
        Sets the node from which the ghost spawns.

        Args:
            node (Node): The spawn node for the ghost.
        """
        self.spawnNode = node

    def startSpawn(self):
        """
        Starts the Spawn mode for the ghost.
        """
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection 
            self.spawn() 

    def startFreight(self):
        """
        Starts the Freight mode for the ghost.
        """
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        """
        Transitions the ghost to normal mode.
        """
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)


class Blinky(Ghost):
    """
    Represents the red Blinky ghost.
    """
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes a Blinky ghost object.

        Args:
            node (Node): The starting node of the ghost.
            pacman (Pacman): The Pacman object in the game.
            blinky (Blinky): The Blinky ghost object (not used for Blinky itself).
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    """
    Represents the pink Pinky ghost.
    """
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes a Pinky ghost object.

        Args:
            node (Node): The starting node of the ghost.
            pacman (Pacman): The Pacman object in the game.
            blinky (Blinky): The Blinky ghost object.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        """
        Sets Pinky's target position for the Scatter mode.
        """
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self):
        """
        Sets Pinky's target position for the Chase mode.
        """
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class Inky(Ghost):
    """
    Represents the cyan Inky ghost.
    """
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes an Inky ghost object.

        Args:
            node (Node): The starting node of the ghost.
            pacman (Pacman): The Pacman object in the game.
            blinky (Blinky): The Blinky ghost object, used for Inky's chasing behavior.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        """
        Sets Inky's target position for the Scatter mode.
        """
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        """
        Sets Inky's target position for the Chase mode.
        """
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    """
    Represents the orange Clyde ghost.
    """
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes a Clyde ghost object.

        Args:
            node (Node): The starting node of the ghost.
            pacman (Pacman): The Pacman object in the game.
            blinky (Blinky): The Blinky ghost object.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        """
        Sets Clyde's target position for the Scatter mode.
        """
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        """
        Sets Clyde's target position for the Chase mode, based on distance from Pacman.
        """
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class GhostGroup(object):
    """
    Manages a group of ghost objects.
    """
    def __init__(self, node, pacman):
        """
        Initializes a GhostGroup object.

        Args:
            node (Node): The starting node for all ghosts in the group.
            pacman (Pacman): The Pacman object in the game.
        """
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        """
        Allows iteration over the ghosts in the group.
        """
        return iter(self.ghosts)

    def update(self, dt):
        """
        Updates the state of all ghosts in the group.

        Args:
            dt (float): Time elapsed since the last frame.
        """
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        """
        Starts Freight mode for all ghosts in the group.
        """
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        """
        Sets the spawn node for all ghosts in the group.

        Args:
            node (Node): The spawn node for the ghosts.
        """
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        """
        Update the points awarded for eating each ghost in Freight mode.
        """
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        """
        Resets the points awarded for eating each ghost in Freight mode to their default value.
        """
        for ghost in self:
            ghost.points = 200

    def hide(self):
        """
        Hides all ghosts in the group.
        """
        for ghost in self:
            ghost.visible = False

    def show(self):
        """
        Shows all ghosts in the group.
        """
        for ghost in self:
            ghost.visible = True

    def reset(self):
        """
        Resets all ghosts in the group to their initial state.
        """
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        """
        Renders all ghosts in the group on the screen.

        Args:
            screen (pygame.Surface): The surface to render on.
        """
        for ghost in self:
            ghost.render(screen)