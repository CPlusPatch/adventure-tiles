""" This module contains the Tile class, which represents a single square on the map """


import pygame
from pos import Pos
from tile_types import TileType


class Tile:
    """A tile is a single square on the map"""

    def __init__(self, tile_type: TileType):
        self.type = tile_type
        # Transparent
        self.surfaces = [
            pygame.Surface((16, 16), pygame.SRCALPHA) for _ in tile_type.images
        ]

    def load_surfaces(self, surrounding_tiles: list[TileType | None]):
        """Loads surfaces in accordance with surrounding tiles"""
        if self.type.size == Pos(1, 1):
            # try:
            self.surfaces[0] = pygame.image.load(
                self.type.get_sprites(surrounding_tiles)[0]
            ).convert_alpha()
            # except Exception as e:
            #    print(e)
            #    self.surfaces[0] = pygame.image.load(self.type.images[0]).convert_alpha()
            return

        # pylint: disable=consider-using-enumerate
        self.surfaces = [
            pygame.image.load(i).convert_alpha()
            for i in self.type.get_sprites(surrounding_tiles)
        ]

    def render(self, _pos: Pos):
        """
        Returns the image of the rendered tile as a Pygame Surface
        Tiles with a size larger than 1x1 will be concatenated as a single surface
        """
        if self.type.size == Pos(1, 1):
            return self.surfaces[0]
        else:
            surface = pygame.Surface(
                (self.type.size * Pos(16, 16)).to_int_tuple(), pygame.SRCALPHA
            )
            for x in range(self.type.size.x):
                for y in range(self.type.size.y):
                    surface.blit(
                        self.surfaces[x + y * self.type.size.x],
                        (x * 16, y * 16),
                    )
            return surface
