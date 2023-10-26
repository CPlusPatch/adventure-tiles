from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
if TYPE_CHECKING:
    from game import Game
from tile import Tile, TileType
from pos import Pos
from tile_types import Grass, Water
from variables import ZOOM
from ui import UI
import struct
import os
import json

test_level = [
    None, None, None, None, None, None, None, None, None, None,
    None, Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Water()), Tile(Water()), Tile(Water()), Tile(Water()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Water()), Tile(Water()), Tile(Water()), Tile(Water()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Grass()), Tile(Water()), Tile(Water()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Grass()), Tile(Water()), Tile(Water()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Grass()), Tile(Water()), Tile(Water()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), Tile(Grass()), None,
    None, None, None, None, None, None, None, None, None, None,
]

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Level:
    """ Each level is its own map of 2D tiles """
    size: Pos
    tiles: list[Tile | None]
    game: Game
    ui: UI
    edit_mode: bool
    map_editor_hotbar: list[TileType | None]
    selected_tile: int # Index of selected tile in tile hotbar

    def __init__(self, size: Pos, game: Game):
        self.size = size
        self.tiles: list[Tile | None] = test_level
        self.game = game

        self.edit_mode = True
        self.map_editor_hotbar = [Grass(), Water(), None, None, None, None]
        self.selected_tile = 0

        self.ui = UI(self.game, self)

        # Load surfaces of tiles
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile = self.get_tile(Pos(x, y))
                if tile is None:
                    continue
                tile.load_surfaces([ tile.type if tile else None for tile in self.get_surrounding_tiles(Pos(x, y))])
    
    def get_surrounding_tiles(self, pos: Pos) -> list[Tile | None]:
        """ Returns a list of the 8 tiles surrounding the given position, starting from the top left and going clockwise """
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
        # Check if out of range
        if pos.x < 0 or pos.x >= self.size.x or pos.y < 0 or pos.y >= self.size.y:
            return None
        return self.tiles[pos.x + pos.y * self.size.x]

    def set_tile(self, pos: Pos, tile: Tile):
        self.tiles[pos.x + pos.y * self.size.x] = tile

        # Reload all tile surfaces
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile = self.get_tile(Pos(x, y))
                if tile is None:
                    continue
                tile.load_surfaces([ tile.type if tile else None for tile in self.get_surrounding_tiles(Pos(x, y))])
        
        print("Reloaded surfaces!")
    
    def mouse_to_in_game_coordinates(self):
        """ Returns the mouse position in in-game coordinates """
        mouse_pos = Pos(*pygame.mouse.get_pos())
        mouse_pos -= Pos(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2)
        mouse_pos /= Pos(16 * ZOOM, 16 * ZOOM)
        mouse_pos += self.game.camera_position
        return mouse_pos.to_int()

    def render(self, camera_position: Pos):
        """
        Render the level onto the screen, with the camera position taken into account
        (0, 0) camera position is the center of the screen, the level is initially drawn with the top left corner at (0, 0)
        """
        final_render = pygame.Surface((self.size * Pos(16, 16)).to_int_tuple())
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile = self.get_tile(Pos(x, y))
                if tile is None:
                    continue

                # Clone the surface
                image = tile.render(Pos(x, y)).copy()
                # Check if mouse is over tile, counting for camera position

                mouse_coords = self.mouse_to_in_game_coordinates()

                if mouse_coords == Pos(x, y):
                    # Draw a red outline
                    pygame.draw.rect(image, (255, 0, 0), pygame.Rect(0, 0, image.get_width(), image.get_height()), 1)
                    # Check for mouse clicks
                    if pygame.mouse.get_pressed()[0]:
                        # Only allow clicking once per second
                        if self.game.last_click + 500 > pygame.time.get_ticks():
                            continue
                        self.game.last_click = pygame.time.get_ticks()

                        if self.edit_mode:
                            if not isinstance(self.map_editor_hotbar[self.selected_tile], TileType):
                                continue
                            self.set_tile(Pos(x, y), Tile(self.map_editor_hotbar[self.selected_tile]))
                        else:
                            # Left click
                            tile.type.on_interact(self.game, Pos(x, y))
                        
                    if pygame.mouse.get_pressed()[2]:

                        # Right click
                        tile.type.on_attack(self.game, Pos(x, y))
                else:
                    image = tile.render(Pos(x, y))            
                
                final_render.blit(image, (x * 16, y * 16))

        # Apply zoom
        final_render = pygame.transform.scale(final_render, (int(final_render.get_width() * ZOOM), int(final_render.get_height() * ZOOM)))
        self.game.screen.blit(final_render, (self.game.screen.get_width() / 2 - camera_position.x * 16 * ZOOM, self.game.screen.get_height() / 2 - camera_position.y * 16 * ZOOM))

        # Render UI
        self.game.screen.blit(self.ui.render(), (0, 0))
    
    def save(self):
        data: dict[
            "tiles": list[str],
            "size": tuple[int, int],
            "camera_position": tuple[int, int]
        ] = {
            "tiles": [tile.type.name for tile in self.tiles],
            "size": (self.size.x, self.size.y),
            "camera_position": (self.game.camera_position.x, self.game.camera_position.y)
        }

        # If savefile doesnt exist, create it
        if not os.path.exists('saves'):
            os.makedirs('saves')

        with open('saves/save1.save', 'w') as save1:  
            save1.write(json.dumps(data))
    
    def load(self):
        with open('saves/save1.save', 'r') as save1:
            data: dict[
                "tiles": list[str],
                "size": tuple[int, int],
                "camera_position": tuple[int, int]
            ] = json.loads(save1.read())

            self.tiles = []

            for tile in data["tiles"]:
                if tile == "base:grass":
                    self.tiles.append(Tile(Grass()))
                elif tile == "base:water":
                    self.tiles.append(Tile(Water()))
            
            
            self.size = Pos(data["size"][0], data["size"][1])
            self.game.camera_position = Pos(data["camera_position"][0], data["camera_position"][1])

            # Load surfaces of tiles
            for x in range(self.size.x):
                for y in range(self.size.y):
                    tile = self.get_tile(Pos(x, y))
                    if tile is None:
                        continue
                    tile.load_surfaces([ tile.type if tile else None for tile in self.get_surrounding_tiles(Pos(x, y))])

