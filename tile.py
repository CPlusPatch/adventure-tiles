""" This module contains the Tile class, which represents a single square on the map """


import pygame
from pos import Vector2
from tile_types import TileType


class Tile:
    """A tile is a single square on the map"""

    surrounding_tiles: list[TileType | None]

    def __init__(self, tile_type: TileType):
        self.type = tile_type
        # Transparent
        self.surfaces = tile_type.images
        self.surrounding_tiles = []

    def load_surfaces(self, _surrounding_tiles: list[TileType | None]):
        """Loads surfaces in accordance with surrounding tiles"""
        self.surrounding_tiles = _surrounding_tiles
        return

        # pylint: disable=consider-using-enumerate

    def render(self, _pos: Vector2):
        """
        Returns the image of the rendered tile as a Pygame Surface
        Tiles with a size larger than 1x1 will be concatenated as a single surface
        """
        if self.type.size == Vector2(1, 1):
            return self.type.get_sprite(self.surrounding_tiles)
        else:
            surface = pygame.Surface(
                (self.type.size * Vector2(16, 16)).to_int_tuple(), pygame.SRCALPHA
            )
            for x in range(self.type.size.x):
                for y in range(self.type.size.y):
                    surface.blit(
                        self.surfaces[x + y * self.type.size.x],
                        (x * 16, y * 16),
                    )
            return surface
