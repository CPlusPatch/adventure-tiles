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
        self.image = pygame.Surface((size * Pos(16, 16)).to_int_tuple())
        self.rect = self.image.get_rect()
        self.rect.x = pos.x
        self.rect.y = pos.y

    def update(self):
        """Called every frame, at 60 frames a second"""
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def render(self, _camera_pos: Pos):
        """Render the entity on the screen"""
        surface = pygame.Surface((self.size * Pos(16, 16)).to_int_tuple())
        surface.blit(self.image, (0, 0))

    def move(self, pos: Pos):
        """Move the entity by the given position"""
        self.pos += pos


class Player(Entity):
    """The player entity"""

    throttle_on: bool
    frame: int
    timer: int
    sprites: list[pygame.Surface]
    rotation: float

    def __init__(self, pos: Pos):
        super().__init__(pos, Pos(43, 47))

        # Load animation sprites from a single image of 16x32 sprites stitched together
        spritesheet = pygame.image.load(
            "assets/spaceship/greenships.png"
        ).convert_alpha()
        self.sprites = [spritesheet.subsurface(pygame.Rect(0, 0, 43, 47))]

        self.image = self.sprites[0]
        self.frame = 0
        self.timer = 0
        self.throttle_on = False
        self.rotation = 180

    def rotate(self, angle: float):
        """Rotate the player by the given angle"""
        self.rotation += angle

    def update(self):
        """Called every frame, at 60 frames a second"""
        if not self.throttle_on:
            return

        self.timer += 1
        if self.timer == 10:
            self.frame += 1
            self.timer = 0
        if self.frame == 1:
            self.frame = 0
        self.image = self.sprites[self.frame]

        super().update()

    def render(self, _camera_pos: Pos):
        """Render the entity on the screen"""
        image = pygame.transform.rotate(self.image, self.rotation)
        return image.copy()
