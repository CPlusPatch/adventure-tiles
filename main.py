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

    is_walking: bool
    frame: int
    timer: int
    sprites: list[pygame.Surface]

    def __init__(self, pos: Pos):
        super().__init__(pos, Pos(1, 2))

        # Load animation sprites from a single image of 16x32 sprites stitched together
        spritesheet = pygame.image.load(
            "assets/character/char1_walking.png"
        ).convert_alpha()
        self.sprites = []
        for i in range(4):
            self.sprites.append(spritesheet.subsurface(pygame.Rect(i * 16, 0, 16, 32)))

        self.image = self.sprites[0]
        self.frame = 0
        self.timer = 0
        self.is_walking = False

    def set_direction(self, angle: int):
        """Set the direction of the player"""
        if angle == 0:
            spritesheet = pygame.image.load(
                "assets/character/char1_walking.png"
            ).convert_alpha()
        elif angle == 90:
            spritesheet = pygame.image.load(
                "assets/character/char1_walking_90.png"
            ).convert_alpha()
        elif angle == 180:
            spritesheet = pygame.image.load(
                "assets/character/char1_walking_180.png"
            ).convert_alpha()
        elif angle == 270:
            spritesheet = pygame.image.load(
                "assets/character/char1_walking_270.png"
            ).convert_alpha()

        self.sprites = []
        for i in range(4):
            self.sprites.append(spritesheet.subsurface(pygame.Rect(i * 16, 0, 16, 32)))

    def update(self):
        """Called every frame, at 60 frames a second"""
        if not self.is_walking:
            return

        self.timer += 1
        if self.timer == 10:
            self.frame += 1
            self.timer = 0
        if self.frame == 4:
            self.frame = 0
        self.image = self.sprites[self.frame]

        super().update()

    def render(self, _camera_pos: Pos):
        """Render the entity on the screen"""
        surface = pygame.Surface(
            (self.size * Pos(16, 16)).to_int_tuple(), pygame.SRCALPHA
        )
        surface.blit(self.image, (0, 0))
        return surface
