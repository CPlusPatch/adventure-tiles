from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game
import pygame
from variables import RESOLUTION, ZOOM, UI_ZOOM

HEART_100 = pygame.image.load("assets/ui/heart_100.png")
HEART_75 = pygame.image.load("assets/ui/heart_75.png")
HEART_50 = pygame.image.load("assets/ui/heart_50.png")
HEART_25 = pygame.image.load("assets/ui/heart_25.png")
HEART_0 = pygame.image.load("assets/ui/heart_0.png")

class UI:
    game: Game

    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
    
    def renderHealth(self):
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

        