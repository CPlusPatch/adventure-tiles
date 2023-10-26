from __future__ import annotations
from enum import Enum
from pos import Pos
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

class Align(Enum):
    """ The alignment of a set of multiple tiles, i.e. which corner it is rendered from """
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class TileType:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    Tiles types may have multiple 16x16 images for larger tiles.
    """
    name: str # In the format "base:stone_wall" for example
    passable: bool
    transparent: bool
    images: list[str] # The paths to the images
    size: Pos # The size of the tiles, where 1 means 16 pixels (for example, a 2x3 size would be 32x48 pixels, so 6 images)
    align: Align # The alignment of the tile, i.e. which corner it is rendered from

    def __init__(self, name: str, images: list[str], size: Pos, align: Align, passable: bool, transparent: bool):
        self.passable = passable
        self.transparent = transparent
        self.images = images
        self.name = name
        self.size = size
        self.align = align
    
    def get_sprite(self, surrounding_tiles: list[TileType]):
       """
       Allows you to get a sprite based on the surrounding tiles
         surrounding_tiles is a list of 8 tiles, starting from the top left and going clockwise
       """
       return self.images[0]

    def __repr__(self):
        return f"TileType({self.name}, {self.passable}, {self.transparent}, {self.images})"

    def on_interact(self, game: Game, pos: Pos):
        pass

    def on_walk(self, game: Game, pos: Pos):
        pass

    def on_attack(self, game: Game, pos: Pos):
        pass

    def on_destroy(self, game: Game, pos: Pos):
        pass

    def on_use(self, game: Game, pos: Pos):
        pass

class Grass(TileType):
    def __init__(self):
        super().__init__("base:grass", ["assets/tiles/grass_center.png"], Pos(1, 1), Align.TOP_LEFT, True, False)
    
    def on_walk(self, game: Game, pos: Pos):
        print("You walk on grass")
    
    def get_sprite(self, surrounding_tiles: list[TileType]):
        super().get_sprite(surrounding_tiles)

        # Possible sprites are grass_center
        # The sprite is chosen based on the surrounding tiles

        x = lambda x: isinstance(x, Water)
        tile = lambda x: f"assets/tiles/{x}"

        tiling = [x(tile) for tile in surrounding_tiles]

        anyValue = "any"

        # Matches tiling with an array of True, False, any to check if they match
        matches = lambda x: all([x[i] == tiling[i] or x[i] == anyValue for i in range(len(x))])

        # We first check if there is water

        if not any(tiling):
            return self.images[0]
        elif matches([True, False, False, False, False, False, False, False]):
            return tile("grass_water_1.png")
        elif matches([anyValue, True, anyValue, False, False, False, False, False]):
            return tile("grass_water_2.png")
        elif matches([anyValue, True, True, True, anyValue, False, False, False]):
            return tile("grass_water_2_3_4.png")
        elif matches([False, False, True, False, False, False, False, False]):
            return tile("grass_water_3.png")
        elif matches([False, False, anyValue, True, anyValue, False, False, False]):
            return tile("grass_water_4.png")
        elif matches([False, False, anyValue, True, True, True, anyValue, False]):
            return tile("grass_water_4_5_6.png")
        elif matches([False, False, False, False, True, False, False, False]):
            return tile("grass_water_5.png")
        elif matches([False, False, False, False, False, False, True, False]):
            return tile("grass_water_7.png")
        elif matches([False, False, False, False, anyValue, anyValue, anyValue, False]):
            return tile("grass_water_6.png")
        elif matches([anyValue, False, False, False, anyValue, True, True, True]):
            return tile("grass_water_6_7_8.png")
        elif matches([anyValue, False, False, False, False, False, anyValue, True]):
            return tile("grass_water_8.png")
        elif matches([True, True, anyValue, False, False, False, anyValue, True]):
            return tile("grass_water_top_and_left.png")
        else:
            return self.images[0]

        


class Water(TileType):
    def __init__(self):
        super().__init__("base:water", ["assets/tiles/water_center.png"], Pos(1,1), Align.TOP_LEFT, False, False)
    
    def on_walk(self, game: Game, pos: Pos):
        print("You walk on water")