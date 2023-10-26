###########################################################
# GAME: A 2D tile-based game made with Pygame             #
# Gaspard WIERZBINSKI, 2023                               #
# Licensed under MIT                                      #
###########################################################

"""
This file contains the Entity class, which represents an object
that can be rendered on the screen
"""

import pygame
from pos import Pos


class Entity(pygame.sprite.Sprite):
    """An entity is an object that can be rendered on the screen"""

    pos: Pos
    size: Pos
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, pos: Pos, size: Pos):
        super().__init__()
        self.pos = pos
        self.size = size
        self.image = pygame.Surface(size.to_int_tuple())
        self.rect = self.image.get_rect()
        self.rect.x = pos.x
        self.rect.y = pos.y

    def update(self):
        """Called every frame, at 60 frames a second"""
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
