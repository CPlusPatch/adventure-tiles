"""
This file contains the Level class, which is used to store the
map of tiles and render them to the screen
"""
from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import random
import pygame
from pos import Pos
from tile import Tile, TileType
from ui import UI
from variables import ZOOM
from main import Player

if TYPE_CHECKING:
    from game import Game


def clamp(n, smallest, largest):
    """Clamps a number between two values"""
    return max(smallest, min(n, largest))


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
    players: dict[str, PlayerData]

    def __init__(self, size: Pos, game: Game):
        self.size = size
        self.game = game

        self.ui = UI(self.game, self)
        self.props = {}

        self.players = {}

        # Get center position
        center_pos = self.game.camera_position
        # Load player 1
        self.players["0"] = {
            "pos": center_pos,
            "health": 100,
            "player": Player(center_pos),
        }

    def mouse_to_in_game_coordinates(self):
        """Returns the mouse position in in-game coordinates"""
        mouse_pos = Pos(*pygame.mouse.get_pos())
        mouse_pos -= Pos(
            self.game.screen.get_width() / 2, self.game.screen.get_height() / 2
        )
        mouse_pos /= Pos(16 * ZOOM, 16 * ZOOM)
        mouse_pos += self.game.camera_position
        return mouse_pos.to_int()

    def render(self, camera_position: Pos):
        """
        Render the level onto the screen, with the camera position taken into account
        (0, 0) camera position is the center of the screen, the level is initially drawn
        with the top left corner at (0, 0)
        """
        final_render = pygame.Surface(
            (self.game.screen.get_width() / ZOOM, self.game.screen.get_height() / ZOOM),
            pygame.SRCALPHA,
        )

        self.render_stars()

        # Render players
        self.render_players(final_render, camera_position)

        # Apply zoom and blit to screen
        self.apply_zoom_and_blit(final_render)

        # Render UI
        self.render_ui()

    def render_stars(self):
        """
        Renders white circles of varying small sizes on the screen,
        with a parallax effect relative to the player
        Parallax effect is done depending on player's distance from 0,0
        """

        # Draw a random amount of white circles in random uniform positions across
        # a surface the size of the screen

        STAR_SIZE_MIN = 2
        STAR_SIZE_MAX = 5
        STAR_COUNT_MIN = 10 * 8
        STAR_COUNT_MAX = 30 * 8

        random.seed(10000)
        star_count = random.randint(STAR_COUNT_MIN, STAR_COUNT_MAX)

        star_surface = pygame.Surface(
            (self.game.screen.get_width() * 4, self.game.screen.get_height() * 4)
        )

        for _ in range(star_count):
            # Draw a white circle
            star_size = random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX)
            star_pos = Pos(
                random.randint(0, star_surface.get_width()),
                random.randint(0, star_surface.get_height()),
            )

            pygame.draw.circle(
                star_surface,
                (255, 255, 255),
                star_pos.to_int_tuple(),
                star_size,
            )

        # Offset the star surface by the player's position in reverse, slower than the player
        self.game.screen.blit(
            star_surface,
            (
                -self.game.camera_position.x * 16 * ZOOM / 1,
                -self.game.camera_position.y * 16 * ZOOM / 1,
            ),
        )

    def render_players(self, final_render, camera_position):
        """Render all players onto the screen"""
        # Render player
        for player in self.players.values():
            player_surface = player["player"].render(camera_position)
            final_render.blit(
                player_surface,
                (
                    # Center player surface at center of screen
                    final_render.get_width() / 2 - player_surface.get_width() / 2,
                    final_render.get_height() / 2 - player_surface.get_height() / 2,
                ),
            )

    def apply_zoom_and_blit(self, final_render):
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
                0,
                0,
            ),
        )

    def render_ui(self):
        """Render UI"""
        # Render UI
        self.game.screen.blit(self.ui.render(), (0, 0))

    def save(self):
        """Save the level to a savefile"""
        """ data: dict[
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
            save1.write(json.dumps(data)) """

    def load(self):
        """Load the level from a savefile"""
        """ with open("saves/save1.save", "r", encoding="utf-8") as save1:
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
                    ) """
