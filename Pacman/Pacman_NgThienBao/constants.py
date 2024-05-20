'''the file contains the constants used in the game'''
TILEWIDTH = 16 # kích thước chiều rộng của 1 ô (pixel)
TILEHEIGHT = 16 # kích thước chiều cao của 1 ô (pixel)
NROWS = 36 # số hàng của bản đồ 
NCOLS = 28 # số cột của bản đồ
SCREENWIDTH = NCOLS*TILEWIDTH # kích thước chiều rộng của màn hình (pixel)
SCREENHEIGHT = NROWS*TILEHEIGHT # kích thước chiều cao của màn hình (pixel)
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT) # kích thước màn hình
# định nghĩa màu sắc theo mã màu RGB,
# mỗi màu sẽ có 3 giá trị từ 0 đến 255, 
# tương ứng với màu đỏ, màu xanh và màu xanh lá cây
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255,100,150)
TEAL = (100,255,255)
ORANGE = (230,190,40)
GREEN = (0, 255, 0)
OPTIONAL = ( 50, 0, 50)
#https://gaubaccuc.ucoz.com/bangmamau
#các dấu như up và down, left và right, đều trái dấu nhau, khi cần chuyển đổi thì nhân với -1 là đẹp
STOP = 0 
UP = 1
DOWN = -1 
LEFT = 2
RIGHT = -2
PORTAL = 3 

PACMAN = 0
PELLET = 1
POWERPELLET = 2
GHOST = 3
BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUIT = 8
#giá trị tương ứng nào cũng không quan trọng, miễn là chúng khác nhau :v
SCATTER = 0
CHASE = 1 
FREIGHT = 2 
SPAWN = 3 

SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4
