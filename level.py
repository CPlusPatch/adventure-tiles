"""
This file contains the Level class, which is used to store the
map of tiles and render them to the screen
"""
from __future__ import annotations
import json
import os
from typing import TYPE_CHECKING, TypedDict
import uuid
import pygame
from pos import Pos
from tile import Tile, TileType
from tile_types import Grass, Water, Earth, TileRegistry
from ui import UI
from variables import ZOOM, GameStates
from main import Player

if TYPE_CHECKING:
    from game import Game

SIZE = 24
test_level = (
    [None] * SIZE
    + ([None] + [Tile(Grass())] * (SIZE - 2) + [None]) * (SIZE - 2)
    + [None] * SIZE
)


def clamp(n, smallest, largest):
    """Clamps a number between two values"""
    return max(smallest, min(n, largest))


PropData = TypedDict("PropData", {"type": Tile, "pos": Pos})
TileData = TypedDict("TileData", {"type": Tile, "pos": Pos})
PlayerData = TypedDict("PlayerData", {"pos": Pos, "health": int, "player": Player})


class Level:
    """Each level is its own map of 2D tiles"""

    size: Pos
    tiles: list[Tile | None]
    game: Game
    ui: UI
    edit_mode: bool
    map_editor_hotbar: list[TileType | None]
    selected_tile: int  # Index of selected tile in tile hotbar
    props: dict[str, PropData]
    players: dict[str, PlayerData]

    def __init__(self, size: Pos, game: Game):
        self.size = size
        self.tiles: list[Tile | None] = test_level
        self.game = game

        self.edit_mode = True
        self.map_editor_hotbar = [Grass(), Water(), Earth(), None, None]
        self.selected_tile = 0

        self.ui = UI(self.game, self)
        self.props = {}

        self.players = {}

        # Load surfaces of tiles
        self.reload_all_surfaces()

        # Get center position
        center_pos = self.game.camera_position
        # Load player 1
        self.players["0"] = {
            "pos": center_pos,
            "health": 100,
            "player": Player(center_pos),
        }

    def get_surrounding_tiles(self, pos: Pos) -> list[Tile | None]:
        """
        Returns a list of the 8 tiles surrounding the given position,
        starting from the top left and going clockwise
        """
        return [
            self.get_tile(pos + Pos(-1, -1)),
            self.get_tile(pos + Pos(0, -1)),
            self.get_tile(pos + Pos(1, -1)),
            self.get_tile(pos + Pos(1, 0)),
            self.get_tile(pos + Pos(1, 1)),
            self.get_tile(pos + Pos(0, 1)),
            self.get_tile(pos + Pos(-1, 1)),
            self.get_tile(pos + Pos(-1, 0)),
        ]

    def get_tile(self, pos: Pos) -> Tile | None:
        """Returns the tile at the given position"""
        # Check if out of range
        if pos.x < 0 or pos.x >= self.size.x or pos.y < 0 or pos.y >= self.size.y:
            return None
        return self.tiles[pos.x + pos.y * self.size.x]

    def set_tile(self, pos: Pos, tile: Tile):
        """Sets the tile at the given position"""
        self.tiles[pos.x + pos.y * self.size.x] = tile

        # Reload all tile surfaces
        self.reload_all_surfaces()

    def mouse_to_in_game_coordinates(self):
        """Returns the mouse position in in-game coordinates"""
        mouse_pos = Pos(*pygame.mouse.get_pos())
        mouse_pos -= Pos(
            self.game.screen.get_width() / 2, self.game.screen.get_height() / 2
        )
        mouse_pos /= Pos(16 * ZOOM, 16 * ZOOM)
        mouse_pos += self.game.camera_position
        return mouse_pos.to_int()

    def add_new_row(self, top: bool):
        """Adds a new row of None tiles to the top or bottom of the level"""
        if top:
            for _ in range(self.size.x):
                self.tiles.insert(0, None)
            self.size.y += 1
            # Move props
            for prop in self.props.values():
                prop["pos"].y += 1
        else:
            for _ in range(self.size.x):
                self.tiles.append(None)
            self.size.y += 1

    def add_new_col(self, left: bool):
        """Adds a new column of None tiles to the left or right of the level"""
        if left:
            for y in range(self.size.y):
                self.tiles.insert(y * (self.size.x + 1), None)
            self.size.x += 1
            # Move props
            for prop in self.props.values():
                prop["pos"].x += 1
        else:
            for y in range(self.size.y):
                self.tiles.insert((y + 1) * (self.size.x + 1), None)
            self.size.x += 1

    def reload_all_surfaces(self):
        """Reloads all tile surfaces"""
        print("Reloaded surfaces")
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile = self.get_tile(Pos(x, y))
                if tile is None:
                    continue
                tile.load_surfaces(
                    [
                        tile.type if tile else None
                        for tile in self.get_surrounding_tiles(Pos(x, y))
                    ]
                )

    def render(self, camera_position: Pos):
        """
        Render the level onto the screen, with the camera position taken into account
        (0, 0) camera position is the center of the screen, the level is initially drawn
        with the top left corner at (0, 0)
        """
        final_render = pygame.Surface((self.size * Pos(16, 16)).to_int_tuple())
        ghost_props: dict[str, PropData] = {}
        ghost_tiles: dict[str, TileData] = {}

        # Render tiles
        self.render_tiles(final_render, ghost_props, ghost_tiles)

        # Render props
        self.render_props(final_render)

        # Render ghost props
        self.render_ghost_props(final_render, ghost_props)

        # Render ghost tiles
        self.render_ghost_tiles(final_render, ghost_tiles)

        # Render players
        self.render_players(final_render, camera_position)

        # Apply zoom and blit to screen
        self.apply_zoom_and_blit(final_render, camera_position)

        # Render UI
        self.render_ui()

    def render_tiles(self, final_render, ghost_props, ghost_tiles):
        """Render all tiles onto the screen"""
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile = self.get_tile(Pos(x, y))
                if tile is None:
                    image = pygame.Surface((16, 16))
                else:
                    # Clone the surface
                    image = tile.render(Pos(x, y)).copy()
                # Check if mouse is over tile, counting for camera position

                mouse_coords = self.mouse_to_in_game_coordinates()

                if mouse_coords == Pos(x, y) and self.game.state == GameStates.PLAYING:
                    # Draw a red outline
                    pygame.draw.rect(
                        image,
                        (255, 0, 0),
                        pygame.Rect(0, 0, image.get_width(), image.get_height()),
                        1,
                    )

                    # If prop is selected, add props to ghost props
                    # If tile is selected, add tile to ghost mode
                    if self.edit_mode:
                        if self.map_editor_hotbar[self.selected_tile].z_index > 0:
                            # Is prop
                            chosen_uuid = str(uuid.uuid4())

                            ghost_props[chosen_uuid] = {
                                "pos": Pos(x, y),
                                "type": Tile(
                                    self.map_editor_hotbar[self.selected_tile]
                                ),
                            }

                            ghost_props[chosen_uuid]["type"].load_surfaces([])
                        elif self.map_editor_hotbar[self.selected_tile] is not None:
                            # Is tile
                            chosen_uuid = str(uuid.uuid4())

                            ghost_tiles[chosen_uuid] = {
                                "pos": Pos(x, y),
                                "type": Tile(
                                    self.map_editor_hotbar[self.selected_tile]
                                ),
                            }

                            ghost_tiles[chosen_uuid]["type"].load_surfaces([])

                    # Check for mouse clicks
                    if pygame.mouse.get_pressed()[0]:
                        # Only allow clicking once per second
                        if self.game.last_click + 500 > pygame.time.get_ticks():
                            continue
                        self.game.last_click = pygame.time.get_ticks()

                        if self.edit_mode:
                            if not isinstance(
                                self.map_editor_hotbar[self.selected_tile], TileType
                            ):
                                continue

                            if self.map_editor_hotbar[self.selected_tile].z_index > 0:
                                # Is prop
                                chosen_uuid = str(uuid.uuid4())

                                self.props[chosen_uuid] = {
                                    "pos": Pos(x, y),
                                    "type": Tile(
                                        self.map_editor_hotbar[self.selected_tile]
                                    ),
                                }

                                self.props[chosen_uuid]["type"].load_surfaces([])
                                continue
                            # Check if old tile was None
                            # If it was, add a new row or column of None tiles
                            # Tile list is stored as a 1D array, so we need to
                            # add a new row or column to the left or right
                            new_x = x
                            new_y = y

                            if tile is None:
                                if x == 0:
                                    self.add_new_col(True)
                                    new_x += 1
                                elif x == self.size.x - 1:
                                    self.add_new_col(False)
                                elif y == 0:
                                    self.add_new_row(True)
                                    new_y += 1
                                elif y == self.size.y - 1:
                                    self.add_new_row(False)

                            self.set_tile(
                                Pos(new_x, new_y),
                                Tile(self.map_editor_hotbar[self.selected_tile]),
                            )
                            self.reload_all_surfaces()
                        else:
                            # Left click
                            tile.type.on_interact(self.game, Pos(x, y))

                    if pygame.mouse.get_pressed()[2]:
                        # Right click
                        tile.type.on_attack(self.game, Pos(x, y))

                final_render.blit(image, (x * 16, y * 16))

    def render_props(self, final_render):
        """Render all props onto the screen"""
        # Render all props as an overlay
        for prop in self.props.values():
            render = prop["type"].render(prop["pos"])
            final_render.blit(
                render,
                (prop["pos"].x * 16, prop["pos"].y * 16),
            )

    def render_ghost_props(self, final_render, ghost_props):
        """Render all ghost props onto the screen"""
        for prop in ghost_props.values():
            render = prop["type"].render(prop["pos"])

            # Make transparent and lower brightness
            render.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)

            final_render.blit(
                render,
                (prop["pos"].x * 16, prop["pos"].y * 16),
            )

    def render_ghost_tiles(self, final_render, ghost_tiles):
        """Render all ghost tiles onto the screen"""
        # Render ghost tiles
        for tile in ghost_tiles.values():
            render = tile["type"].render(tile["pos"])

            # Make transparent and lower brightness
            render.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)

            final_render.blit(
                render,
                (tile["pos"].x * 16, tile["pos"].y * 16),
            )

    def render_players(self, final_render, camera_position):
        """Render all players onto the screen"""
        # Render player
        for player in self.players.values():
            player_surface = player["player"].render(camera_position)
            final_render.blit(
                player_surface,
                (
                    player["pos"].x * 16,
                    player["pos"].y * 16,
                ),
            )

    def apply_zoom_and_blit(self, final_render, camera_position):
        """Apply zoom and blit to screen"""
        # Apply zoom
        final_render = pygame.transform.scale(
            final_render,
            (
                int(final_render.get_width() * ZOOM),
                int(final_render.get_height() * ZOOM),
            ),
        )
        self.game.screen.blit(
            final_render,
            (
                self.game.screen.get_width() / 2 - camera_position.x * 16 * ZOOM,
                self.game.screen.get_height() / 2 - camera_position.y * 16 * ZOOM,
            ),
        )

    def render_ui(self):
        """Render UI"""
        # Render UI
        self.game.screen.blit(self.ui.render(), (0, 0))

    def save(self):
        """Save the level to a savefile"""
        data: dict[
            "tiles" : list[str],
            "size" : tuple[int, int],
            "camera_position" : tuple[int, int],
            "player":PlayerData,
        ] = {
            "tiles": [tile.type.name if tile else "" for tile in self.tiles],
            "size": (self.size.x, self.size.y),
            "camera_position": (
                self.game.camera_position.x,
                self.game.camera_position.y,
            ),
            "player": {
                "pos": self.players["0"]["pos"].to_tuple(),
                "health": self.players["0"]["health"],
            },
        }

        # If savefile doesnt exist, create it
        if not os.path.exists("saves"):
            os.makedirs("saves")

        with open("saves/save1.save", "w", encoding="utf-8") as save1:
            save1.write(json.dumps(data))

    def load(self):
        """Load the level from a savefile"""
        with open("saves/save1.save", "r", encoding="utf-8") as save1:
            data: dict[
                "tiles" : list[str],
                "size" : tuple[int, int],
                "camera_position" : tuple[int, int],
                "player":PlayerData,
            ] = json.loads(save1.read())

            self.tiles = []

            for tile in data["tiles"]:
                self.tiles.append(Tile(TileRegistry[tile]()) if tile else None)

            self.size = Pos(data["size"][0], data["size"][1])
            self.game.camera_position = Pos(
                data["camera_position"][0], data["camera_position"][1]
            )

            self.players["0"]["pos"] = Pos(
                data["player"]["pos"][0], data["player"]["pos"][1]
            )

            self.players["0"]["health"] = data["player"]["health"]

            # Load surfaces of tiles
            for x in range(self.size.x):
                for y in range(self.size.y):
                    tile = self.get_tile(Pos(x, y))
                    if tile is None:
                        continue
                    tile.load_surfaces(
                        [
                            tile.type if tile else None
                            for tile in self.get_surrounding_tiles(Pos(x, y))
                        ]
                    )
