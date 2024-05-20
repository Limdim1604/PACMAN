
from constants import *

class MainMode(object):
    """Represents the main mode of the game.

    Attributes:
        timer (float): The timer for the mode.
        mode (str): The current mode of the game.
        time (int): The duration of the mode.
    """
    
    def __init__(self):
        """Initializes the MainMode object."""
        self.timer = 0
        self.scatter() 

    def update(self, dt):
        """Updates the mode based on the elapsed time.

        Args:
            dt (float): The elapsed time since the last update.
        """
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        """Sets the mode to scatter mode."""
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        """Sets the mode to chase mode."""
        self.mode = CHASE
        self.time = 20
        self.timer = 0


class ModeController(object):
    """Controls the modes of the entity."""
    
    def __init__(self, entity):
        """Initializes the ModeController object.

        Args:
            entity (Entity): The entity to control the modes for.
        """
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity 

    def update(self, dt):
        """Updates the modes for the entity.

        Args:
            dt (float): The elapsed time since the last update.
        """
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode

    def setFreightMode(self):
        """Sets the mode to freight mode."""
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def setSpawnMode(self):
        """Sets the mode to spawn mode."""
        if self.current is FREIGHT:
            self.current = SPAWN