
import pygame
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        """
        Initializes a Text object.

        Args:
            text (str): The text to be displayed.
            color (tuple): The color of the text in RGB format.
            x (int): The x-coordinate of the text position.
            y (int): The y-coordinate of the text position.
            size (int): The font size of the text.
            time (float, optional): The lifespan of the text in seconds. Defaults to None.
            id (int, optional): The unique identifier of the text. Defaults to None.
            visible (bool, optional): Whether the text is visible or not. Defaults to True.
        """
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("Pacman_NgThienBao/PressStart2P-Regular.ttf")
        self.createLabel()

    def setupFont(self, fontpath):
        """
        Sets up the font for the text.

        Args:
            fontpath (str): The path to the font file.
        """
        self.font = pygame.font.Font(fontpath, self.size)

    def createLabel(self):
        """
        Creates the label surface for the text.
        """
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newtext):
        """
        Sets the text to a new value and updates the label.

        Args:
            newtext (str): The new text value.
        """
        self.text = str(newtext)
        self.createLabel()

    def update(self, dt):
        """
        Updates the text based on the elapsed time.

        Args:
            dt (float): The elapsed time since the last update in seconds.
        """
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen):
        """
        Renders the text on the screen.

        Args:
            screen (pygame.Surface): The surface to render the text on.
        """
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))


class TextGroup(object):
    def __init__(self):
        """
        Initializes a TextGroup object.
        """
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        self.showText(READYTXT)

    def addText(self, text, color, x, y, size, time=None, id=None):
        """
        Adds a new Text object to the group.

        Args:
            text (str): The text to be displayed.
            color (tuple): The color of the text in RGB format.
            x (int): The x-coordinate of the text position.
            y (int): The y-coordinate of the text position.
            size (int): The font size of the text.
            time (float, optional): The lifespan of the text in seconds. Defaults to None.
            id (int, optional): The unique identifier of the text. Defaults to None.

        Returns:
            int: The unique identifier of the added text.
        """
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def removeText(self, id):
        """
        Removes a Text object from the group.

        Args:
            id (int): The unique identifier of the text to be removed.
        """
        self.alltext.pop(id)
        
    def setupText(self):
        """
        Sets up the initial text objects in the group.
        """
        size = TILEHEIGHT
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText("SCORE", WHITE, 0, 0, size)
        self.addText("LEVEL", WHITE, 23*TILEWIDTH, 0, size)

    def update(self, dt):
        """
        Updates all the text objects in the group.

        Args:
            dt (float): The elapsed time since the last update in seconds.
        """
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    def showText(self, id):
        """
        Shows a specific text object in the group.

        Args:
            id (int): The unique identifier of the text to be shown.
        """
        self.hideText()
        self.alltext[id].visible = True

    def hideText(self):
        """
        Hides all the text objects in the group.
        """
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def updateScore(self, score):
        """
        Updates the score text.

        Args:
            score (int): The new score value.
        """
        self.updateText(SCORETXT, str(score).zfill(8))

    def updateLevel(self, level):
        """
        Updates the level text.

        Args:
            level (int): The new level value.
        """
        self.updateText(LEVELTXT, str(level + 1).zfill(3))

    def updateText(self, id, value):
        """
        Updates the text of a specific text object.

        Args:
            id (int): The unique identifier of the text object.
            value (str): The new text value.
        """
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    def render(self, screen):
        """
        Renders all the text objects on the screen.

        Args:
            screen (pygame.Surface): The surface to render the text on.
        """
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
