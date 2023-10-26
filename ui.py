from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game
    from level import Level
import pygame
from variables import RESOLUTION, ZOOM, UI_ZOOM

HEART_100 = pygame.image.load("assets/ui/heart_100.png")
HEART_75 = pygame.image.load("assets/ui/heart_75.png")
HEART_50 = pygame.image.load("assets/ui/heart_50.png")
HEART_25 = pygame.image.load("assets/ui/heart_25.png")
HEART_0 = pygame.image.load("assets/ui/heart_0.png")

class UI:
    game: Game
    level: Level

    def __init__(self, game: Game, level: Level):
        self.game = game
        self.level = level
        self.surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
    
    def render(self):
        """
        Renders the UI
        """
        self.surface.fill((0, 0, 0, 0))
        self.render_health()
        self.render_map_mode_toolbar()
        return self.surface
    
    def render_health(self):
        """
        Draws 5 hearts in the top left of the surface, with margins
        """
        health = 13 # 1 full heart is 4 health
        full_hearts = health // 4
        half_heart = health % 4
        empty_hearts = 5 - full_hearts - (1 if half_heart > 0 else 0)

        heart_size = 20 * UI_ZOOM
        margin = 10 * UI_ZOOM

        for i in range(full_hearts):
            heart_pos = (i * heart_size + margin, margin)
            heart_image = pygame.transform.scale(HEART_100, (heart_size, heart_size))
            self.surface.blit(heart_image, heart_pos)

        if half_heart > 0:
            heart_pos = (full_hearts * heart_size + margin, margin)
            if half_heart == 1:
                heart_image = pygame.transform.scale(HEART_25, (heart_size, heart_size))
            elif half_heart == 2:
                heart_image = pygame.transform.scale(HEART_50, (heart_size, heart_size))
            elif half_heart == 3:
                heart_image = pygame.transform.scale(HEART_75, (heart_size, heart_size))
            self.surface.blit(heart_image, heart_pos)

        for i in range(empty_hearts):
            heart_pos = ((full_hearts + (1 if half_heart > 0 else 0) + i) * heart_size + margin, margin)
            heart_image = pygame.transform.scale(HEART_0, (heart_size, heart_size))
            self.surface.blit(heart_image, heart_pos)
        
        return self.surface

    def render_map_mode_toolbar(self):
        """
        Draws the map mode toolbar in the bottom center of the screen
        """
        if not self.level.edit_mode:
            return

        # Use self.level.map_editor_hotbar and render each tile inside it in a gold square

        tile_size = 32 * UI_ZOOM

        print(self.level.selected_tile)

        for i in range(len(self.level.map_editor_hotbar)):
            tile = self.level.map_editor_hotbar[i]
            if tile is None:
                continue
            tile_surface = pygame.transform.scale(pygame.image.load(tile.images[0]), (tile_size, tile_size))
            # Add gold frame to tile
            pygame.draw.rect(tile_surface, (255, 215, 0), pygame.Rect(0, 0, tile_size, tile_size), 2)
            self.surface.blit(tile_surface, (RESOLUTION[0] / 2 - len(self.level.map_editor_hotbar) / 2 * tile_size + i * tile_size, RESOLUTION[1] - tile_size))

            # Add a number to the top left of the hotbar tile
            font_renderer = FontRenderer(str(i + 1))
            font_surface = font_renderer.render()

            print(font_surface.get_height())

            self.surface.blit(font_surface, (RESOLUTION[0] / 2 - len(self.level.map_editor_hotbar) / 2 * tile_size + i * tile_size + 4, RESOLUTION[1] - tile_size + 4))


class FontRenderer:
    """ Renders font using the font sprites """
    text: str

    def __init__(self, text: str):
        self.text = text
    
    def render(self):
        """ Returns a surface with the rendered text """
        allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+%#&)(.!,_/) "

        text = self.text.lower()

        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)

        # Render each character of text with kerning -1 and UI_ZOOM applied onto the surface
        # Font is NOT monospace
        # Spaces are just 4-pixel spaces and not a character
        # Font height is 8
        
        x = 0
        y = 0

        for char in text:
            if char not in allowed_characters:
                continue
            if char == " ":
                x += 4 * UI_ZOOM
                continue
            char_surface = pygame.image.load(f"assets/font/font_{char}.png")
            surface.blit(char_surface, (x, y))
            x += char_surface.get_width()
        
        # Crop surface to text
        surface = surface.subsurface(pygame.Rect(0, 0, x, 8))

        # Scale surface by UI_ZOOM
        surface = pygame.transform.scale(surface, (int(surface.get_width() * UI_ZOOM), int(surface.get_height() * UI_ZOOM)))


        return surface