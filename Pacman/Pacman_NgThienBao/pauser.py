
class Pause(object):
    """A class that represents the pause state of a game.

    Attributes:
        paused (bool): The current pause state.
        timer (float): The timer for tracking the elapsed time during the pause.
        pauseTime (float): The duration of the pause in seconds.
        func (function): The function to be executed after the pause time has elapsed.

    """

    def __init__(self, paused=False):
        """Initializes the Pause class.

        Args:
            paused (bool, optional): The initial pause state. Defaults to False.
        """
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None
        
    def update(self, dt):
        """Updates the pause state.

        Args:
            dt (float): The time elapsed since the last update.

        Returns:
            function or None: The function to be executed after the pause time has elapsed, or None if no function is set.
        """
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func 
        return None

    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        """Sets the pause state.

        Args:
            playerPaused (bool, optional): Whether the player is paused. Defaults to False.
            pauseTime (float, optional): The duration of the pause in seconds. Defaults to None.
            func (function, optional): The function to be executed after the pause time has elapsed. Defaults to None.
        """
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    def flip(self):
        """Toggles the pause state."""
        self.paused = not self.paused
