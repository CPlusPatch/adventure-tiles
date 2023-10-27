""" This file contains all the tile types in the game. """
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Literal, Type
from pos import Pos

if TYPE_CHECKING:
    from game import Game


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
    images: list[str]  # The paths to the images
    size: Pos  # The size of the tiles, where 1 means 16 pixels
    # (for example, a 2x3 size would be 32x48 pixels, so 6 images)
    align: Align  # The alignment of the tile, i.e. which corner it is rendered from
    z_index: int  # The z-index of the tile

    def __init__(
        self,
        name: str,
        images: list[str],
        size: Pos,
        align: Align,
        passable: bool,
        transparent: bool,
        z_index: int = 0,
    ):
        self.passable = passable
        self.transparent = transparent
        self.images = images
        self.name = name
        self.size = size
        self.align = align
        self.z_index = z_index

    def get_sprites(self, _surrounding_tiles: list[TileType]):
        """
        Allows you to get a sprite based on the surrounding tiles
          surrounding_tiles is a list of 8 tiles, starting from the top left and going clockwise
        """
        return self.images

    def __repr__(self):
        return (
            f"TileType({self.name}, {self.passable}, {self.transparent}, {self.images})"
        )

    def assign_dynamic_tile_borders(
        self,
        name_template: str,
        other_type: Type[TileType],
        surrounding_tiles: list[TileType],
    ):
        """Assigns dynamic tile borders based on the surrounding tiles"""
        tiling = [isinstance(tile, other_type) for tile in surrounding_tiles]

        any_value = "any"

        # We first check if there is water

        if not any(tiling):
            return self.images
        elif matches([True, False, False, False, False, False, False, False], tiling):
            return tile(f"{name_template}_1.png")
        elif matches(
            [any_value, True, any_value, False, False, False, False, False], tiling
        ):
            return tile(f"{name_template}_2.png")
        elif matches(
            [any_value, True, True, True, any_value, False, False, False], tiling
        ):
            return tile(f"{name_template}_2_4.png")
        elif matches([False, False, True, False, False, False, False, False], tiling):
            return tile(f"{name_template}_3.png")
        elif matches(
            [False, False, any_value, True, any_value, False, False, False], tiling
        ):
            return tile(f"{name_template}_4.png")
        elif matches(
            [False, False, any_value, True, True, True, any_value, False], tiling
        ):
            return tile(f"{name_template}_4_6.png")
        elif matches([False, False, False, False, True, False, False, False], tiling):
            return tile(f"{name_template}_5.png")
        elif matches([False, False, False, False, False, False, True, False], tiling):
            return tile(f"{name_template}_7.png")
        elif matches(
            [False, False, False, False, any_value, any_value, any_value, False], tiling
        ):
            return tile(f"{name_template}_6.png")
        elif matches(
            [any_value, False, False, False, any_value, True, True, True], tiling
        ):
            return tile(f"{name_template}_6_8.png")
        elif matches(
            [any_value, False, False, False, False, False, any_value, True], tiling
        ):
            return tile(f"{name_template}_8.png")
        elif matches(
            [any_value, True, any_value, False, False, False, any_value, True], tiling
        ):
            return tile(f"{name_template}_2_8.png")
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
            return self.images

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
            ["assets/tiles/grass_center.png"],
            Pos(1, 1),
            Align.TOP_LEFT,
            True,
            False,
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on grass")

    def get_sprites(self, surrounding_tiles: list[TileType]):
        super().get_sprites(surrounding_tiles)

        if any([isinstance(tile, Water) for tile in surrounding_tiles]):
            return self.assign_dynamic_tile_borders(
                "grass_water", Water, surrounding_tiles
            )
        elif any([isinstance(tile, Earth) for tile in surrounding_tiles]):
            return self.assign_dynamic_tile_borders(
                "earth/grass_earth", Earth, surrounding_tiles
            )
        else:
            return self.images


class Earth(TileType):
    """An earth tile"""

    def __init__(self):
        super().__init__(
            "base:earth",
            ["assets/tiles/earth/earth1.png"],
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
            ["assets/tiles/water_center.png"],
            Pos(1, 1),
            Align.TOP_LEFT,
            False,
            False,
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on water")


class BridgeV(TileType):
    """A bridge tile"""

    def __init__(self):
        super().__init__(
            "base:bridge",
            [
                "assets/tiles/bridge/bridge1x1.png",
                "assets/tiles/bridge/bridge1x2.png",
                "assets/tiles/bridge/bridge1x3.png",
                "assets/tiles/bridge/bridge1x4.png",
                "assets/tiles/bridge/bridge1x5.png",
                "assets/tiles/bridge/bridge2x1.png",
                "assets/tiles/bridge/bridge2x2.png",
                "assets/tiles/bridge/bridge2x3.png",
                "assets/tiles/bridge/bridge2x4.png",
                "assets/tiles/bridge/bridge2x5.png",
                "assets/tiles/bridge/bridge3x1.png",
                "assets/tiles/bridge/bridge3x2.png",
                "assets/tiles/bridge/bridge3x3.png",
                "assets/tiles/bridge/bridge3x4.png",
                "assets/tiles/bridge/bridge3x5.png",
                "assets/tiles/bridge/bridge4x1.png",
                "assets/tiles/bridge/bridge4x2.png",
                "assets/tiles/bridge/bridge4x3.png",
                "assets/tiles/bridge/bridge4x4.png",
                "assets/tiles/bridge/bridge4x5.png",
                "assets/tiles/bridge/bridge5x1.png",
                "assets/tiles/bridge/bridge5x2.png",
                "assets/tiles/bridge/bridge5x3.png",
                "assets/tiles/bridge/bridge5x4.png",
                "assets/tiles/bridge/bridge5x5.png",
            ],
            Pos(5, 5),
            Align.TOP_LEFT,
            True,
            True,
            1,
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on bridge")


class BridgeH(TileType):
    """A bridge tile"""

    def __init__(self):
        super().__init__(
            "base:bridge",
            [
                "assets/tiles/bridge/r_90/bridge1x1.png",
                "assets/tiles/bridge/r_90/bridge1x2.png",
                "assets/tiles/bridge/r_90/bridge1x3.png",
                "assets/tiles/bridge/r_90/bridge1x4.png",
                "assets/tiles/bridge/r_90/bridge1x5.png",
                "assets/tiles/bridge/r_90/bridge2x1.png",
                "assets/tiles/bridge/r_90/bridge2x2.png",
                "assets/tiles/bridge/r_90/bridge2x3.png",
                "assets/tiles/bridge/r_90/bridge2x4.png",
                "assets/tiles/bridge/r_90/bridge2x5.png",
                "assets/tiles/bridge/r_90/bridge3x1.png",
                "assets/tiles/bridge/r_90/bridge3x2.png",
                "assets/tiles/bridge/r_90/bridge3x3.png",
                "assets/tiles/bridge/r_90/bridge3x4.png",
                "assets/tiles/bridge/r_90/bridge3x5.png",
                "assets/tiles/bridge/r_90/bridge4x1.png",
                "assets/tiles/bridge/r_90/bridge4x2.png",
                "assets/tiles/bridge/r_90/bridge4x3.png",
                "assets/tiles/bridge/r_90/bridge4x4.png",
                "assets/tiles/bridge/r_90/bridge4x5.png",
                "assets/tiles/bridge/r_90/bridge5x1.png",
                "assets/tiles/bridge/r_90/bridge5x2.png",
                "assets/tiles/bridge/r_90/bridge5x3.png",
                "assets/tiles/bridge/r_90/bridge5x4.png",
                "assets/tiles/bridge/r_90/bridge5x5.png",
                "assets/tiles/bridge/r_90/bridge6x1.png",
                "assets/tiles/bridge/r_90/bridge6x2.png",
                "assets/tiles/bridge/r_90/bridge6x3.png",
                "assets/tiles/bridge/r_90/bridge6x4.png",
                "assets/tiles/bridge/r_90/bridge6x5.png",
                "assets/tiles/bridge/r_90/bridge7x1.png",
                "assets/tiles/bridge/r_90/bridge7x2.png",
                "assets/tiles/bridge/r_90/bridge7x3.png",
                "assets/tiles/bridge/r_90/bridge7x4.png",
                "assets/tiles/bridge/r_90/bridge7x5.png",
            ],
            Pos(5, 7),
            Align.TOP_LEFT,
            True,
            True,
            1,
        )

    def on_walk(self, game: Game, pos: Pos):
        print("You walk on bridge")


TileRegistry = {
    "base:grass": Grass(),
    "base:earth": Earth(),
    "base:water": Water(),
    "base:bridge_v": BridgeV(),
    "base:bridge_h": BridgeH(),
}
