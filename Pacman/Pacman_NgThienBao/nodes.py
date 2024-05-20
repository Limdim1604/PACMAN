import pygame
from vector import Vector2
from constants import *
import numpy as np

# X: empty space
# +: node
# .: horizontal/vertical path

class Node(object):
    """
    The Node class will contain information about the node's position, 
    neighboring nodes, and entity access.

    Attributes:
        position (Vector2): The position of the node on the screen.
        neighbors (dict): A dictionary storing the neighboring nodes of the current node.
        Keys are directions (UP, DOWN, LEFT, RIGHT, PORTAL) and values are Node objects.
        access (dict): A dictionary storing the entity access to the current node.
        Keys are directions (UP, DOWN, LEFT, RIGHT) and values are lists of entities allowed to access.
        ...
    """
    def __init__(self, x, y):
        """
        Initializes a new Node object.

        Args:
            x (int): The x-coordinate of the node.
            y (int): The y-coordinate of the node.
        """
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
                       DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
                       LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
                       RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def denyAccess(self, direction, entity):
        """
        Denies entity access to a specific direction.

        Args:
            direction (int): The direction to deny access.
            entity (Entity): The entity to deny access.
        """
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allowAccess(self, direction, entity):
        """
        Allows entity access to a specific direction.

        Args:
            direction (int): The direction to allow access.
            entity (Entity): The entity to allow access.
        """
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)
    
    def render(self, screen):
        """
        Renders the connecting lines and nodes on the game screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    """
    The NodeGroup class will contain information about the nodes in a level.same graph

    Attributes:
        level (str): The name of the text file containing level information.
        nodesLUT (dict): A dictionary storing all nodes in the level.
            Keys are the pixel coordinates of the node and values are Node objects.
        nodeSymbols (list): A list of characters in the text file representing nodes.
        pathSymbols (list): A list of characters in the text file representing paths.
        homekey (tuple): The pixel coordinates of the home node.
    """
    def __init__(self, level):
        """
        Initializes a new NodeGroup object.

        Args:
            level (str): The name of the text file containing level information.
        """
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None

    def readMazeFile(self, textfile):
        """
        Reads in the text file using numpy's loadtxt.

        Args:
            textfile (str): The name of the text file containing level information.

        Returns:
            numpy.ndarray: A numpy array containing data from the text file.
        """
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        """
        Creates a table storing nodes from data in the text file.

        Args:
            data (numpy.ndarray): A numpy array containing data from the text file.
            xoffset (int): The horizontal offset of the node table from pixel coordinates.
            yoffset (int): The vertical offset of the node table from pixel coordinates.
        """
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        """
        Converts the row and column in the text file to actual pixel values on the screen.

        Args:
            x (int): The column in the text file.
            y (int): The row in the text file.

        Returns:
            tuple: The pixel coordinates of the node.
        """
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        """
        Connects nodes horizontally.

        Args:
            data (numpy.ndarray): A numpy array containing data from the text file.
            xoffset (int): The horizontal offset of the node table from pixel coordinates.
            yoffset (int): The vertical offset of the node table from pixel coordinates.
        """
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        """
        Connects nodes vertically.

        Args:
            data (numpy.ndarray): A numpy array containing data from the text file.
            xoffset (int): The horizontal offset of the node table from pixel coordinates.
            yoffset (int): The vertical offset of the node table from pixel coordinates.
        """
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getStartTempNode(self):
        """
        Returns the node where Pacman starts.

        Returns:
            Node: The node where Pacman starts.
        """
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        """
        Connects the portal pairs.

        Args:
            pair1 (tuple): The pixel coordinates of the first portal.
            pair2 (tuple): The pixel coordinates of the second portal.
        """
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def createHomeNodes(self, xoffset, yoffset):
        """
        Creates the home nodes for ghosts.

        Args:
            xoffset (int): The horizontal offset of the node table from pixel coordinates.
            yoffset (int): The vertical offset of the node table from pixel coordinates.

        Returns:
            tuple: The pixel coordinates of the home node.
        """
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeTable(homedata, xoffset, yoffset) 
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):     
        """
        Connects the home nodes to other nodes.

        Args:
            homekey (tuple): The pixel coordinates of the home node.
            otherkey (tuple): The pixel coordinates of the other node.
            direction (int): The direction of the connection.
        """
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

    def getNodeFromPixels(self, xpixel, ypixel):
        """
        Returns the node from the given pixel coordinates.

        Args:
            xpixel (int): The x-coordinate in pixels.
            ypixel (int): The y-coordinate in pixels.

        Returns:
            Node: The node corresponding to the given pixel coordinates.
        """
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None
    
    def getNodeFromTiles(self, col, row):
        """
        Returns the node from the given row and column coordinates.

        Args:
            col (int): The column in the text file.
            row (int): The row in the text file.

        Returns:
            Node: The node corresponding to the given row and column coordinates.
        """
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def denyAccess(self, col, row, direction, entity):
        """
        Denies entity access to a specific direction from a specific node.

        Args:
            col (int): The column in the text file.
            row (int): The row in the text file.
            direction (int): The direction to deny access.
            entity (Entity): The entity to deny access.
        """
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        """
        Allows entity access to a specific direction from a specific node.

        Args:
            col (int): The column in the text file.
            row (int): The row in the text file.
            direction (int): The direction to allow access.
            entity (Entity): The entity to allow access.
        """
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    def denyAccessList(self, col, row, direction, entities):
        """
        Denies entity access to a specific direction from a list of nodes.

        Args:
            col (int): The column in the text file.
            row (int): The row in the text file.
            direction (int): The direction to deny access.
            entities (list): The list of entities to deny access.
        """
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    def allowAccessList(self, col, row, direction, entities):
        """
        Allows entity access to a specific direction from a list of nodes.

        Args:
            col (int): The column in the text file.
            row (int): The row in the text file.
            direction (int): The direction to allow access.
            entities (list): The list of entities to allow access.
        """
        for entity in entities:
            self.allowAccess(col, row, direction, entity)

    def denyHomeAccess(self, entity):
        """
        Denies entity access to the down direction from the home node.

        Args:
            entity (Entity): The entity to deny access.
        """
        self.nodesLUT[self.homekey].denyAccess(DOWN, entity)

    def allowHomeAccess(self, entity):
        """
        Allows entity access to the down direction from the home node.

        Args:
            entity (Entity): The entity to allow access.
        """
        self.nodesLUT[self.homekey].allowAccess(DOWN, entity)

    def denyHomeAccessList(self, entities):
        """
        Denies entity access to the down direction from a list of nodes.

        Args:
            entities (list): The list of entities to deny access.
        """
        for entity in entities:
            self.denyHomeAccess(entity)

    def allowHomeAccessList(self, entities):
        """
        Allows entity access to the down direction from a list of nodes.

        Args:
            entities (list): The list of entities to allow access.
        """
        for entity in entities:
            self.allowHomeAccess(entity)

    def render(self, screen):
        """
        Renders the nodes on the game screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        for node in self.nodesLUT.values():
            node.render(screen)

# import pygame
# from vector import Vector2
# from constants import *
# import numpy as np

# # X: khoảng trống (empty space)
# # +: nút (node)
# # .: đường dẫn dọc/ngang (horizontal/vertical path)

# class Node(object): #Lớp Node sẽ chứa thông tin về vị trí của nút, các nút lân cận và quyền truy cập của các thực thể
#     def __init__(self, x, y):
#         self.position = Vector2(x, y)
#         self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
#         self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
#                        DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
#                        LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
#                        RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

#     #Hàm này sẽ cấm thực thể truy cập vào một hướng cụ thể
#     def denyAccess(self, direction, entity):
#         if entity.name in self.access[direction]:
#             self.access[direction].remove(entity.name)

#     #Hàm này sẽ cho phép thực thể truy cập vào một hướng cụ thể
#     def allowAccess(self, direction, entity):
#         if entity.name not in self.access[direction]:
#             self.access[direction].append(entity.name)
    
#     #Hàm này có chức năng vẽ các đường kết nối và các nút trên màn hình game
#     def render(self, screen):
#         for n in self.neighbors.keys():
#             if self.neighbors[n] is not None:
#                 line_start = self.position.asTuple()
#                 line_end = self.neighbors[n].position.asTuple()
#                 pygame.draw.line(screen, WHITE, line_start, line_end, 4)
#                 pygame.draw.circle(screen, RED, self.position.asInt(), 12)

# class NodeGroup(object): #Lớp NodeGroup sẽ chứa thông tin về các nút trong một màn chơi
#     def __init__(self, level):
#         self.level = level
#         self.nodesLUT = {}
#         self.nodeSymbols = ['+', 'P', 'n']
#         self.pathSymbols = ['.', '-', '|', 'p']
#         data = self.readMazeFile(level)
#         self.createNodeTable(data)
#         self.connectHorizontally(data)
#         self.connectVertically(data)
#         self.homekey = None

#     #Hàm này sẽ đọc trong tệp text bằng loadtxt của numpy
#     def readMazeFile(self, textfile):
#         return np.loadtxt(textfile, dtype='<U1')

#     def createNodeTable(self, data, xoffset=0, yoffset=0):
#         for row in list(range(data.shape[0])):
#             for col in list(range(data.shape[1])):
#                 if data[row][col] in self.nodeSymbols:
#                     x, y = self.constructKey(col+xoffset, row+yoffset)
#                     self.nodesLUT[(x, y)] = Node(x, y)

#     #Hàm này chỉ đơn giản là chuyển đổi hàng và cột trong tệp text
#     #thành các giá trị pixel thực tế trên màn hình 
#     #bằng cách nhân chúng với giá trị mà chúng ta đã đặt cho kích thước ô
#     def constructKey(self, x, y):
#         return x * TILEWIDTH, y * TILEHEIGHT

#     #Hàm kết nối các nút theo chiều ngang
#     def connectHorizontally(self, data, xoffset=0, yoffset=0):
#         for row in list(range(data.shape[0])):
#             key = None
#             for col in list(range(data.shape[1])):
#                 if data[row][col] in self.nodeSymbols:
#                     if key is None:
#                         key = self.constructKey(col+xoffset, row+yoffset)
#                     else:
#                         otherkey = self.constructKey(col+xoffset, row+yoffset)
#                         self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
#                         self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
#                         key = otherkey
#                 elif data[row][col] not in self.pathSymbols:
#                     key = None

#     #Hàm kết nối các nút theo chiều dọc
#     def connectVertically(self, data, xoffset=0, yoffset=0):
#         dataT = data.transpose()
#         for col in list(range(dataT.shape[0])):
#             key = None
#             for row in list(range(dataT.shape[1])):
#                 if dataT[col][row] in self.nodeSymbols:
#                     if key is None:
#                         key = self.constructKey(col+xoffset, row+yoffset)
#                     else:
#                         otherkey = self.constructKey(col+xoffset, row+yoffset)
#                         self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
#                         self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
#                         key = otherkey
#                 elif dataT[col][row] not in self.pathSymbols:
#                     key = None

#     #Hàm để cho ta biết nút mà ta muốn Pacman bắt đầu
#     def getStartTempNode(self):
#         nodes = list(self.nodesLUT.values())
#         return nodes[0]

#     #Hàm này sẽ kết nối các cặp cổng
#     def setPortalPair(self, pair1, pair2):
#         key1 = self.constructKey(*pair1)
#         key2 = self.constructKey(*pair2)
#         if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
#             self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
#             self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

#     #các con ma cũng cần nhà mà,vây nên ta phải tạo ra nhà cho chúng nó, pacman sẽ ko xâm nhập
#     def createHomeNodes(self, xoffset, yoffset):
#         homedata = np.array([['X','X','+','X','X'],
#                              ['X','X','.','X','X'],
#                              ['+','X','.','X','+'],
#                              ['+','.','+','.','+'],
#                              ['+','X','X','X','+']])

#         self.createNodeTable(homedata, xoffset, yoffset) 
#         self.connectHorizontally(homedata, xoffset, yoffset)
#         self.connectVertically(homedata, xoffset, yoffset)
#         self.homekey = self.constructKey(xoffset+2, yoffset)
#         return self.homekey

#     #Hàm này sẽ kết nối các nút nhà với các nút khác
#     def connectHomeNodes(self, homekey, otherkey, direction):     
#         key = self.constructKey(*otherkey)
#         self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
#         self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

#     #Hàm này sẽ trả về nút từ tọa độ pixel được cung cấp
#     def getNodeFromPixels(self, xpixel, ypixel):
#         if (xpixel, ypixel) in self.nodesLUT.keys():
#             return self.nodesLUT[(xpixel, ypixel)]
#         return None
    
#     #Hàm này sẽ trả về nút từ tọa độ hàng và cột được cung cấp
#     def getNodeFromTiles(self, col, row):
#         x, y = self.constructKey(col, row)
#         if (x, y) in self.nodesLUT.keys():
#             return self.nodesLUT[(x, y)]
#         return None

#     #Hàm này sẽ cấm thực thể truy cập vào một hướng cụ thể từ một nút cụ thể
#     def denyAccess(self, col, row, direction, entity):
#         node = self.getNodeFromTiles(col, row)
#         if node is not None:
#             node.denyAccess(direction, entity)

#     #Hàm này sẽ cho phép thực thể truy cập vào một hướng cụ thể từ một nút cụ thể
#     def allowAccess(self, col, row, direction, entity):
#         node = self.getNodeFromTiles(col, row)
#         if node is not None:
#             node.allowAccess(direction, entity)

#     #Hàm này sẽ cấm thực thể truy cập vào một hướng cụ thể từ một danh sách các nút
#     def denyAccessList(self, col, row, direction, entities):
#         for entity in entities:
#             self.denyAccess(col, row, direction, entity)

#     #Hàm này sẽ cho phép thực thể truy cập vào một hướng cụ thể từ một danh sách các nút
#     def allowAccessList(self, col, row, direction, entities):
#         for entity in entities:
#             self.allowAccess(col, row, direction, entity)

#     #Hàm này sẽ cấm thực thể truy cập vào hướng xuống từ nút nhà
#     def denyHomeAccess(self, entity):
#         self.nodesLUT[self.homekey].denyAccess(DOWN, entity)

#     #Hàm này sẽ cho phép thực thể truy cập vào hướng xuống từ nút nhà
#     def allowHomeAccess(self, entity):
#         self.nodesLUT[self.homekey].allowAccess(DOWN, entity)

#     #Hàm này sẽ cấm thực thể truy cập vào hướng xuống từ một danh sách các nút
#     def denyHomeAccessList(self, entities):
#         for entity in entities:
#             self.denyHomeAccess(entity)

#     #Hàm này sẽ cho phép thực thể truy cập vào hướng xuống từ một danh sách các nút
#     def allowHomeAccessList(self, entities):
#         for entity in entities:
#             self.allowHomeAccess(entity)

#     #vẽ các nút trên màn hình game
#     def render(self, screen):
#         for node in self.nodesLUT.values():
#             node.render(screen)