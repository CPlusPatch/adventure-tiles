###########################################################
# GAME: A 2D tile-based game made with Pygame             #
# Gaspard WIERZBINSKI, 2023                               #
# Licensed under MIT                                      #
###########################################################
from enum import Enum
import pygame

RESOLUTION = (800, 600)

class Game:
    def loop(self):
        # Main game loop
        pass

class Pos:
    """ A 2D position, inside the game (center is 0,0) """
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Pos(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other):
        return Pos(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other):
        return Pos(self.x // other.x, self.y // other.y)

    def to_window_coords(self):
        """ Convert the position to window coordinates """
        return (self.x + RESOLUTION[0] / 2, self.y + RESOLUTION[1] / 2)

class Entity(pygame.sprite.Sprite):
    """ An entity is an object that can be rendered on the screen """
    pos: Pos
    size: Pos
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, pos: Pos, size: Pos):
        super().__init__()
        self.pos = pos
        self.size = size
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = pos.x
        self.rect.y = pos.y

    def update(self):
        """ Called every frame, at 60 frames a second """
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Tile:
    def __init__(self, type: string):
        pass

class Level:
    """ Each level is its own map of 2D tiles """

    def __init__(self, size: Pos):
        self.size = size
        self.tiles: list[Tile | None] = [None] * size.x * size.y
    
    def get_tile(self, pos: Pos):
        return self.tiles[pos.x + pos.y * self.size.x]

    def set_tile(self, pos: Pos, tile: Tile):
        self.tiles[pos.x + pos.y * self.size.x] = tile

    def render(self, camera_position: Pos):
        """ Render the level onto the screen, with the camera position taken into account """
        pass

class Game:
    screen: pygame.Surface
    level: Level
    camera_position: Pos
    entities: pygame.sprite.Group
    player: Entity

    def __init__(self):
        self.level = Level(Pos(16, 16))
        self.camera_position = Pos(0, 0)
        self.entities = pygame.sprite.Group()
        self.player = Entity(Pos(0, 0), Pos(16, 16))
        self.entities.add(self.player)
    
    def init_window(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("The Game")
    