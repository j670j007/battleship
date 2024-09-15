import pygame_widgets
import pygame as pg
import os

# Should be a widget (draws a board)
# Stores an array
# and has function addShip() that adds to that array
# should also have function to lookup if coordinate has ship on it
# Doesnt need to know gamemode (1-5 ships)

# 0 for empty
# 1 for miss
# x for hit
# Ship class for ship
EMPTY_ROW = [0 for i in range(10)]

class Ship:
    def __init__(self, size, x=0, y=0) -> None:
        #self.x = 1
        #self.y = size # number 1-5 s.t. the ship is 1x(size)
        self.x = x #x position
        self.y = y #y position
        self.width = 70 * size  # placeholder
        self.height = 50  # Height is based on ship size
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)  #create rectangle for the ship for mouse movement purposes
        self.image = self.load_ship_image(size)  #assign image to shape based on size

    def load_ship_image(self, size):
        image_path = os.path.join("data", f"ship_{size}.png") #get image path based on given size
        image = pg.image.load(image_path).convert_alpha() #load image from path
        scaled = pg.transform.scale(image, (self.width, self.height)) #scale image based on dimensions
        return scaled

    def rotate90(self):
        self.x, self.y = self.y, self.x  #swap coords
        self.image = pg.transform.rotate(self.image, 90)  #rotate image
        self.width, self.height = self.height, self.width #swap height/width
        self.rect.width, self.rect.height = self.rect.height, self.rect.width  #swap width/height for the rect

    def move(self, offset):
        self.rect.move_ip(offset)  #move the ship's rectangle
        self.x, self.y = self.rect.topleft  #update the ship's coordinates

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  #draw ship based on rect's position

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)  #use pygame's rect's collidepoint to determine interaction with mouse

# Will have to be able to support a ship board or a attack board
class Board:
    def __init__(self) -> None:
        # always 10x10
        self.gameBoard = [EMPTY_ROW for i in range(10)]

    def draw(self, screen, x, y, size=200):
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200)

        # given x is left
        # given y is top
        BOARD_WIDTH = size
        BOARD_HEIGHT = size
        blockSize = int(BOARD_WIDTH / 10) # Set the size of the grid block
        x = int(x)
        y = int(y)

        for xDraw in range(x, x + BOARD_WIDTH, blockSize):
            for yDraw in range(y, y + BOARD_HEIGHT, blockSize):
                rect = pg.Rect(xDraw, yDraw, blockSize, blockSize)
                pg.draw.rect(screen, BLACK, rect, 1)

    def addToBoard(self, ship=Ship):
        #update array w/ ship position based off of where it is placed on the board
        print("drawing ship")
        pass