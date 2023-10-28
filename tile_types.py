""" This file contains all the tile types in the game. """
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Literal, Type
import pygame
from pos import Pos
from variables import RESOLUTION

if TYPE_CHECKING:
    from game import Game

pygame.display.set_mode(RESOLUTION)
pygame.display.init()


def overworld_subsurface(x1, y1, x2, y2):
    """Returns a subsurface of the main overworld image (in 16x16 chunks)"""
    overworld = pygame.image.load("assets/Overworld.png").convert_alpha()
    return overworld.subsurface(
        pygame.Rect(x1 * 16, y1 * 16, (x2 - x1) * 16, (y2 - y1) * 16)
    )


class Align(Enum):
    """The alignment of a set of multiple tiles, i.e. which corner it is rendered from"""

    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3


class TileType:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    Tiles types may have multiple 16x16 images for larger tiles.
    """

    name: str  # In the format "base:stone_wall" for example
    passable: bool
    transparent: bool
    images: list[pygame.surface.Surface]  # Image is chosen at random from these
    size: Pos  # The size of the tiles, where 1 means 16 pixels
    # (for example, a 2x3 size would be 32x48 pixels, so 6 images)
    align: Align  # The alignment of the tile, i.e. which corner it is rendered from
    z_index: int  # The z-index of the tile
    connected_tiles: list[pygame.surface.Surface]

    def __init__(
        self,
        name: str,
        images: list[pygame.surface.Surface],
        size: Pos,
        align: Align,
        passable: bool,
        transparent: bool,
        z_index: int = 0,
        connected_tiles: list[pygame.surface.Surface] = None,
    ):
        self.passable = passable
        self.transparent = transparent
        self.images = images
        self.name = name
        self.size = size
        self.align = align
        self.z_index = z_index
        # In the format
        # 0 1 2
        # 3   4
        # 5 6 7
        #
        # 8 9
        # 10 11
        self.connected_tiles = connected_tiles if connected_tiles else []

    def get_sprite(self, _surrounding_tiles: list[TileType]):
        """
        Allows you to get a sprite based on the surrounding tiles
          surrounding_tiles is a list of 8 tiles, starting from the top left and going clockwise
        """
        return self.images[0].copy()

    def __repr__(self):
        return (
            f"TileType({self.name}, {self.passable}, {self.transparent}, {self.images})"
        )

    def assign_dynamic_tile_borders(
        self,
        _name_template: str,
        other_type: Type[TileType],
        surrounding_tiles: list[TileType],
        connected_tiles=None,
    ):
        """Assigns dynamic tile borders based on the surrounding tiles"""
        tiling = [isinstance(tile, other_type) for tile in surrounding_tiles]

        connected_tiles = connected_tiles if connected_tiles else self.connected_tiles

        if len(connected_tiles) == 0:
            return self.images[0]

        any_value = "any"

        # We first check if there is water

        if not any(tiling):
            return self.images[0]
        elif matches([True, False, False, False, False, False, False, False], tiling):
            return connected_tiles[7]
        elif matches(
            [any_value, True, any_value, False, False, False, False, False], tiling
        ):
            return connected_tiles[6]
        elif matches(
            [any_value, True, True, True, any_value, False, False, False], tiling
        ):
            return connected_tiles[9]
        elif matches([False, False, True, False, False, False, False, False], tiling):
            return connected_tiles[5]
        elif matches(
            [False, False, any_value, True, any_value, False, False, False], tiling
        ):
            return connected_tiles[3]
        elif matches(
            [False, False, any_value, True, True, True, any_value, False], tiling
        ):
            return connected_tiles[11]
        elif matches([False, False, False, False, True, False, False, False], tiling):
            return connected_tiles[0]
        elif matches([False, False, False, False, False, False, True, False], tiling):
            return connected_tiles[2]
        elif matches(
            [False, False, False, False, any_value, any_value, any_value, False], tiling
        ):
            return connected_tiles[1]
        elif matches(
            [any_value, False, False, False, any_value, True, True, True], tiling
        ):
            return connected_tiles[10]
        elif matches(
            [any_value, False, False, False, False, False, any_value, True], tiling
        ):
            return connected_tiles[4]
        elif matches(
            [any_value, True, any_value, False, False, False, any_value, True], tiling
        ):
            return connected_tiles[8]
        # elif matches([True, False, True, False, False, False, False, False], tiling):
        #    return tile(f"{name_template}_1_3.png")
        # elif matches(
        #   [any_value, True, any_value, False, any_value, True, any_value, False],
        #    tiling,
        # ):
        #    return tile(f"{name_template}_2_6.png")
        # elif matches(
        #    [any_value, False, any_value, True, any_value, True, any_value, True],
        #    tiling,
        # ):
        #    return tile(f"{name_template}_4_6_8.png")
        # elif matches(
        #    [any_value, False, any_value, True, any_value, False, any_value, True],
        #    tiling,
        # ):
        #    return tile(f"{name_template}_4_8.png")
        # elif matches([False, False, False, False, True, False, True, False], tiling):
        #    return tile(f"{name_template}_5_7.png")
        # elif matches(
        #    [any_value, True, any_value, True, any_value, True, any_value, True], tiling
        # ):
        #    return tile(f"{name_template}_island.png")
        else:
            return self.images[0]

    def on_interact(self, game: Game, pos: Pos):
        """Called when the player interacts with the tile"""

    def on_walk(self, game: Game, pos: Pos):
        """Called when the player walks on the tile"""

    def on_attack(self, game: Game, pos: Pos):
        """Called when the player attacks the tile"""

    def on_destroy(self, game: Game, pos: Pos):
        """Called when the player destroys the tile"""

    def on_use(self, game: Game, pos: Pos):
        """Called when the player uses the tile"""


class Grass(TileType):
    """A grass tile"""

    def __init__(self):
        super().__init__(
            "base:grass",
            [overworld_subsurface(0, 0, 1, 1)],
            Pos(1, 1),
            Align.TOP_LEFT,
            True,
            False,
            connected_tiles=[
                # Water
                overworld_subsurface(2, 6, 3, 7),
                overworld_subsurface(3, 6, 4, 7),
                overworld_subsurface(4, 6, 5, 7),
                overworld_subsurface(2, 7, 3, 8),
                overworld_subsurface(4, 7, 5, 8),
                overworld_subsurface(2, 8, 3, 9),
                overworld_subsurface(3, 8, 4, 9),
                overworld_subsurface(4, 8, 5, 9),
                overworld_subsurface(2, 9, 3, 10),
                overworld_subsurface(3, 9, 4, 10),
                overworld_subsurface(2, 10, 3, 11),
                overworld_subsurface(3, 10, 4, 11),
                # Earth
                overworld_subsurface(0, 29, 1, 30),
                overworld_subsurface(1, 29, 2, 30),
                overworld_subsurface(2, 29, 3, 30),
                overworld_subsurface(0, 30, 1, 31),
                overworld_subsurface(2, 30, 3, 31),
                overworld_subsurface(0, 31, 1, 32),
                overworld_subsurface(1, 31, 2, 32),
                overworld_subsurface(2, 31, 3, 32),
                overworld_subsurface(0, 32, 1, 33),
                overworld_subsurface(1, 32, 2, 33),
                overworld_subsurface(0, 33, 1, 34),
                overworld_subsurface(1, 33, 2, 34),
            ],
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on grass")

    def get_sprite(self, surrounding_tiles: list[TileType]):
        super().get_sprite(surrounding_tiles)

        if any([isinstance(tile, Water) for tile in surrounding_tiles]):
            return self.assign_dynamic_tile_borders(
                "grass_water",
                Water,
                surrounding_tiles,
                connected_tiles=self.connected_tiles[:12],
            ).copy()
        elif any([isinstance(tile, Earth) for tile in surrounding_tiles]):
            return self.assign_dynamic_tile_borders(
                "earth/grass_earth",
                Earth,
                surrounding_tiles,
                connected_tiles=self.connected_tiles[12:],
            ).copy()
        else:
            return self.images[0].copy()


class Earth(TileType):
    """An earth tile"""

    def __init__(self):
        super().__init__(
            "base:earth",
            [overworld_subsurface(1, 30, 2, 31), overworld_subsurface(2, 32, 3, 33)],
            Pos(1, 1),
            Align.TOP_LEFT,
            True,
            False,
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on earth")


def matches(x: list[bool | Literal["any"]], tiling: list[bool]):
    """Matches tiling with an array of True, False, any to check if they match"""
    return all([x[i] == tiling[i] or x[i] == "any" for i in range(len(x))])


def tile(x):
    """Returns a tile path"""
    return [f"assets/tiles/{x}"]


class Water(TileType):
    """A water tile"""

    def __init__(self):
        super().__init__(
            "base:water",
            [overworld_subsurface(3, 7, 4, 8)],
            Pos(1, 1),
            Align.TOP_LEFT,
            False,
            False,
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on water")


TileRegistry = {
    "base:grass": Grass,
    "base:earth": Earth,
    "base:water": Water,
}
