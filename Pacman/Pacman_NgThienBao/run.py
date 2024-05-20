import pygame  # Initialize Pygame
from pygame.locals import *  # Import constants like QUIT, KEYDOWN, K_SPACE, etc.
from constants import *  # Import game-specific constants
from sys import *  # Import system functions and environment variables
from pacman import Pacman  # Import Pacman class
from nodes import NodeGroup  # Import NodeGroup class
from pellets import PelletGroup  # Import PelletGroup class
from ghosts import GhostGroup  # Import GhostGroup class
from fruit import Fruit  # Import Fruit class
from pauser import Pause  # Import Pause class
from text import TextGroup  # Import TextGroup class
from sprites import LifeSprites  # Import LifeSprites class
from sprites import MazeSprites  # Import MazeSprites class
from mazedata import MazeData  # Import MazeData class

class GameController(object):
    """
    The main game controller class. Manages game logic, rendering, and events.

    Attributes:
        screen (pygame.Surface): The main game window.
        background (pygame.Surface): The background image (either normal or flashing).
        background_norm (pygame.Surface): The normal background image.
        background_flash (pygame.Surface): The flashing background image.
        clock (pygame.time.Clock): The game clock for controlling frame rate.
        fruit (Fruit): The fruit object, if present.
        pause (Pause): The pause object for handling game pauses.
        level (int): The current game level.
        lives (int): The number of remaining lives.
        score (int): The player's current score.
        textgroup (TextGroup): The group containing on-screen text elements.
        lifesprites (LifeSprites): The sprite group containing the player's lives.
        flashBG (bool): Flag indicating whether to flash the background.
        flashTime (float): The duration of the background flash.
        flashTimer (float): Timer for the background flash.
        fruitCaptured (list): A list of fruit sprites that have been captured.
        fruitNode (Node): The node where the fruit spawns.
        mazedata (MazeData): The data object containing information about the maze.
        running (bool): Flag indicating whether the game is running.
        high_score (int): The highest score achieved.

    Methods:
        setBackground(): Creates the normal and flashing background images.
        startScreen(): Displays the initial game start screen.
        startScreen2(): Displays the screen for choosing music and showing instructions.
        startGame(): Initializes a new game level.
        update(): Updates game logic, events, and rendering.
        checkEvents(): Handles keyboard and mouse events.
        checkPelletEvents(): Checks for Pacman eating pellets and power pellets.
        checkGhostEvents(): Checks for Pacman colliding with ghosts.
        checkFruitEvents(): Checks for Pacman eating the fruit.
        showEntities(): Shows Pacman and ghosts.
        hideEntities(): Hides Pacman and ghosts.
        nextLevel(): Starts the next level.
        restartGame(): Restarts the game from the beginning.
        resetLevel(): Resets the current level.
        updateScore(): Updates the player's score.
        render(): Renders game objects to the screen.
    """

    def __init__(self):
        """
        Initializes the GameController object.
        """
        pygame.init()  # Initialize Pygame
        pygame.mixer.init()  # Initialize sound mixer
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)  # Create the game window
        self.background = None  # Initialize background image
        self.background_norm = None  # Initialize normal background image
        self.background_flash = None  # Initialize flashing background image
        self.clock = pygame.time.Clock()  # Create a game clock
        self.fruit = None  # Initialize fruit object
        self.pause = Pause(True)  # Initialize pause object
        self.level = 0  # Initialize level
        self.lives = 8  # Initialize lives
        self.score = 0  # Initialize score
        self.textgroup = TextGroup()  # Initialize text group
        self.lifesprites = LifeSprites(self.lives)  # Initialize life sprites
        self.flashBG = False  # Initialize background flash flag
        self.flashTime = 0.2  # Set background flash duration
        self.flashTimer = 0  # Initialize background flash timer
        self.fruitCaptured = []  # Initialize list of captured fruit sprites
        self.fruitNode = None  # Initialize fruit node
        self.mazedata = MazeData()  # Initialize maze data
        self.running = True  # Set game running flag
        self.high_score = 0  # Initialize high score

    def setBackground(self):
        """
        Creates the normal and flashing background images for the current level.
        """
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()  # Create normal background surface
        self.background_norm.fill(OPTIONAL)  # Fill with optional color
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()  # Create flashing background surface
        self.background_flash.fill(BLACK)  # Fill with black color
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level % 5)  # Construct maze for normal background
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)  # Construct maze for flashing background
        self.flashBG = False  # Reset background flash flag
        self.background = self.background_norm  # Set initial background to normal

    def startScreen(self):
        """
        Displays the initial game start screen with instructions.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            self.screen.fill((0, 250, 255))  # Fill background with light blue
            font = pygame.font.Font("Pacman_NgThienBao/UVN.TTF", 28)  # Set font for instructions

            instructions = ["ĐỒ ÁN CUỐI KỲ DSA", "GAME PACMAN", "Nguyễn Thiên Bảo", "Nhấn Space để tiếp tục"]
            for i, instruction in enumerate(instructions):
                instruction_text = font.render(instruction, 1, (255, 20, 100))  # Render instruction text
                instruction_pos = instruction_text.get_rect(centerx=self.screen.get_width()/2, centery=self.screen.get_height()/5 + 60 * (i+1))  # Set position for instruction text
                self.screen.blit(instruction_text, instruction_pos)  # Draw instruction text

            pygame.display.flip()  # Update display

    def startScreen2(self):
        """
        Displays the screen for choosing music and showing game instructions.
        """
        self.music_options = [  # List of music options
            "Pacman_NgThienBao/BTS_FAKELOVE.mp3",
            "Pacman_NgThienBao/BUONGDOITAYNHAURA.mp3",
            "Pacman_NgThienBao/CAUSEILOVEYOU.mp3",
            "Pacman_NgThienBao/HARUHARU.mp3",
            "Pacman_NgThienBao/XICHLINH.mp3",
            "Pacman_NgThienBao/ATTACKONTITAN1.mp3",
            "Pacman_NgThienBao/5CMS.mp3"
        ]
        self.music_option_names = [  # List of music option names
            "[Fake Love Orchestral]",
            "[Buông Đôi Tay Nhau Ra]",
            "[Cause I Love You]",
            "[BigBang-Haru Haru]",
            "[Xích Linh Remix]",
            "[Attack On Titan]",
            "[5 Cm/s]"
        ]
        self.music_option_texts = []  # List to store rendered music option texts
        font = pygame.font.Font("Pacman_NgThienBao/UVN.TTF", 20)  # Set font for music options and instructions
        instructions = ["Click chuột để chọn nhạc, có thể không chọn", "Nhấn Space để chơi và tạm dừng", "Giữ nút mũi tên để di chuyển"]  # List of game instructions
        self.music_option_states = [False] * len(self.music_option_names)  # Initialize music option states (False by default)
        for i, instruction in enumerate(instructions):
            instruction_text = font.render(instruction, 1, (255, 255, 255))
            instruction_pos = instruction_text.get_rect(centerx=self.screen.get_width()/2, centery=self.screen.get_height()/10 + 40 * i)
            self.music_option_texts.append((instruction_text, instruction_pos))
        for i, music_option_name in enumerate(self.music_option_names):
            music_option_text = font.render(music_option_name, 1, (0, 255, 255))
            music_option_pos = music_option_text.get_rect(centerx=self.screen.get_width()/2, centery=self.screen.get_height()/10 + 40 * (i + len(instructions)))
            self.music_option_texts.append((music_option_text, music_option_pos))
        high_score_text = font.render(f"Highest Score: {self.high_score}", 1, (100, 255, 100))  # Render high score text
        high_score_pos = high_score_text.get_rect(centerx=self.screen.get_width()/2, centery=self.screen.get_height()/10 + 40 * (len(self.music_option_names) + len(instructions)))
        self.music_option_texts.append((high_score_text, high_score_pos))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for i, (music_option_text, music_option_pos) in enumerate(self.music_option_texts[len(instructions):]):
                        if music_option_pos.collidepoint(x, y):
                            if i < len(self.music_options):
                                pygame.mixer.music.load(self.music_options[i])
                                pygame.mixer.music.set_volume(1)
                                pygame.mixer.music.play(-1)
                                self.music_option_states = [False] * len(self.music_option_names)
                                self.music_option_states[i] = True
                                for j, music_option_name in enumerate(self.music_option_names):
                                    color = YELLOW if self.music_option_states[j] else (0, 255, 255)
                                    music_option_text = font.render(music_option_name, 1, color)
                                    music_option_pos = music_option_text.get_rect(centerx=self.screen.get_width()/2, centery=self.screen.get_height()/10 + 40 * (j + len(instructions)))
                                    self.music_option_texts[j + len(instructions)] = (music_option_text, music_option_pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not pygame.mixer.music.get_busy():
                            pygame.mixer.music.load(self.music_options[0])
                            pygame.mixer.music.set_volume(0)
                            pygame.mixer.music.play(-1)
                        return

            self.screen.fill((OPTIONAL))
            for music_option_text, music_option_pos in self.music_option_texts:
                self.screen.blit(music_option_text, music_option_pos)
            pygame.display.flip()

    def startGame(self):
        """
        Initializes a new game level.
        """
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name + ".txt", self.mazedata.obj.name + "_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("Pacman_NgThienBao/" + self.mazedata.obj.name + ".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup("Pacman_NgThienBao/" + self.mazedata.obj.name + ".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    def update(self):
        """
        Updates the game state, events, and rendering.
        """
        dt = self.clock.tick(30) / 800.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        """
        Handles keyboard and mouse events.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            # self.hideEntities()

    def checkPelletEvents(self):
        """
        Checks for Pacman eating pellets and power pellets.
        """
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                effect_sound = pygame.mixer.Sound("Pacman_NgThienBao/WAKUWAKU.mp3")
                effect_sound.play()
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        """
        Checks for Pacman colliding with ghosts.
        """
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    effect_sound = pygame.mixer.Sound("Pacman_NgThienBao/WAKUWAKU.mp3")
                    effect_sound.play()
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        effect_sound = pygame.mixer.Sound("Pacman_NgThienBao/WAKUWAKU.mp3")
                        effect_sound.play()
                        if self.lives <= 0:
                            pygame.mixer.music.stop()
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                            self.high_score = max(self.score, self.high_score)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        """
        Checks for Pacman eating the fruit.
        """
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        """
        Shows Pacman and ghosts.
        """
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        """
        Hides Pacman and ghosts.
        """
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        """
        Starts the next level.
        """
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        """
        Restarts the game from the beginning.
        """
        # pygame.mixer.music.load("Pacman_NgThienBao/BUONGDOITAYNHAURA.mp3")
        self.startScreen2()
        self.lives = 8
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        """
        Resets the current level.
        """
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def updateScore(self, points):
        """
        Updates the player's score.
        """
        self.score += points
        self.textgroup.updateScore(self.score)

    def render(self):
        """
        Renders game objects to the screen.
        """
        self.screen.blit(self.background, (0, 0))
        # self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i + 1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()


if __name__ == "__main__":
    """
    Main function to run the game.
    """
    game = GameController()
    game.startScreen()
    game.startScreen2()
    game.startGame()

    while game.running:
        game.update()