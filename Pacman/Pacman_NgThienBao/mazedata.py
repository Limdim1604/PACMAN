
from constants import *

class MazeBase(object): 
    """Represents the base class for a maze in a Pacman game.

    Attributes:
        portalPairs (dict): A dictionary containing the portal pairs in the maze.
        homeoffset (tuple): The offset of the home nodes in the maze.
        ghostNodeDeny (dict): A dictionary containing the areas where ghosts are denied access.
    """

    def __init__(self):
        """Initialize the MazeBase object."""
        
        self.portalPairs = {}
        self.homeoffset = (0, 0)
        self.ghostNodeDeny = {UP:(), DOWN:(), LEFT:(), RIGHT:()}

    def setPortalPairs(self, nodes):
        """Set the portal pairs in the maze.

        Args:
            nodes (object): The nodes object representing the maze nodes.
        """
     
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)

    def connectHomeNodes(self, nodes):
        """Connect the home nodes in the maze.

        Args:
            nodes (object): The nodes object representing the maze nodes.
        """
      
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)

    def addOffset(self, x, y):
        """Add an offset to the given coordinates.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            tuple: The updated coordinates with the offset.
        """
      
        return x+self.homeoffset[0], y+self.homeoffset[1]

    def denyGhostsAccess(self, ghosts, nodes):
        """Deny access to ghosts in certain areas of the maze.

        Args:
            ghosts (object): The ghosts object representing the ghosts in the game.
            nodes (object): The nodes object representing the maze nodes.
        """
     
        nodes.denyAccessList(*(self.addOffset(2, 3) + (LEFT, ghosts)))
        nodes.denyAccessList(*(self.addOffset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.denyAccessList(*(values + (direction, ghosts)))


class Maze1(MazeBase):
    """Class representing Maze 1."""
    
    def __init__(self):
        """Initialize the Maze1 object."""
     
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0:((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)
        self.ghostNodeDeny = {UP:((12, 14), (15, 14), (12, 26), (15, 26)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}


class Maze2(MazeBase):
    """Class representing Maze 2."""
    
    def __init__(self):
        """Initialize the Maze2 object."""

        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0:((0, 4), (27, 4)), 1:((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {UP:((9, 14), (18, 14), (11, 23), (16, 23)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}


class MazeData(object):
    """Class representing the maze data."""
    
    def __init__(self):
        """Initialize the MazeData object."""
     
        self.obj = None
        self.mazedict = {0:Maze1, 1:Maze2}

    def loadMaze(self, level):
        """Load the maze based on the given level."""
   
        self.obj = self.mazedict[level%len(self.mazedict)]()
        
