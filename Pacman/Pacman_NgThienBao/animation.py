
from constants import *

class Animator(object):
    """
    Represents an animation object that manages a sequence of frames.

    Attributes:
        frames (list): A list of frames for the animation.
        current_frame (int): The index of the current frame.
        speed (int): The speed of the animation in frames per second.
        loop (bool): Indicates whether the animation should loop or not.
        dt (float): The elapsed time since the last frame change.
        finished (bool): Indicates whether the animation has finished or not.
    """

    def __init__(self, frames=[], speed=20, loop=True):
        """
        Initializes an Animator object.

        Args:
            frames (list): A list of frames for the animation.
            speed (int): The speed of the animation in frames per second.
            loop (bool): Indicates whether the animation should loop or not.
        """
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False

    def reset(self):
        """
        Resets the animation to its initial state.
        """
        self.current_frame = 0
        self.finished = False

    def update(self, dt):
        """
        Updates the animation based on the elapsed time.

        Args:
            dt (float): The elapsed time since the last update.

        Returns:
            The current frame of the animation.
        """
        if not self.finished:
            self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                self.current_frame -= 1
   
        return self.frames[self.current_frame]

    def nextFrame(self, dt):
        """
        Advances to the next frame of the animation.

        Args:
            dt (float): The elapsed time since the last frame change.
        """
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0





                        
