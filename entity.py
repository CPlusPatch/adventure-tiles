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
from pos import Coords, Vector2


class Entity(pygame.sprite.Sprite):
    """An entity is an object that can be rendered on the screen"""

    coords: Coords
    velocity: Vector2
    size: Vector2
    image: pygame.Surface
    rect: pygame.Rect
    dead: bool

    def __init__(
        self, coords: Coords, size: Vector2, velocity: Vector2 = Vector2(0, 0)
    ):
        super().__init__()
        self.coords = coords
        self.size = size
        self.velocity = velocity
        self.image = pygame.Surface(size.to_int_tuple())
        self.rect = self.image.get_rect()
        self.rect.x = coords.pos.x
        self.rect.y = coords.pos.y
        self.dead = False

    def update(self):
        """Called every frame, at 60 frames a second"""
        self.rect.x = self.coords.pos.x
        self.rect.y = self.coords.pos.y

    def render(self):
        """Render the entity on the screen"""
        surface = pygame.Surface(self.size.to_int_tuple())
        surface.blit(self.image, (0, 0))

    def move(self, pos: Vector2):
        """Move the entity by the given position"""
        self.coords.pos += pos


class Player(Entity):
    """The player entity"""

    throttle_on: bool
    frame: int
    timer: int
    sprites: list[pygame.Surface]

    def __init__(self, coords: Coords):
        super().__init__(coords, Vector2(43, 47))

        # Load animation sprites from a single image of 16x32 sprites stitched together
        spritesheet = pygame.image.load(
            "assets/spaceship/greenships.png"
        ).convert_alpha()
        self.sprites = [spritesheet.subsurface(pygame.Rect(0, 0, 43, 47))]

        self.image = self.sprites[0]
        self.frame = 0
        self.timer = 0
        self.throttle_on = False

    def shoot(self):
        """Shoot a bullet"""
        OFFSET_RIGHT = 10
        OFFSET_LEFT = 6

        right_side_pos = self.coords.pos + self.coords.right() * OFFSET_RIGHT
        left_side_pos = self.coords.pos + self.coords.left() * OFFSET_LEFT

        # Play shooting sound
        sound = pygame.mixer.Sound("assets/sounds/laser.wav")
        sound.set_volume(0.4)
        sound.play()

        return [
            Bullet(Coords(right_side_pos, self.coords.rotation)),
            Bullet(Coords(left_side_pos, self.coords.rotation)),
        ]

    def update(self):
        """Called every frame, at 60 frames a second"""
        # Clamp velocity
        MAX_VELOCITY = 3
        self.velocity.x = max(-MAX_VELOCITY, min(MAX_VELOCITY, self.velocity.x))
        self.velocity.y = max(-MAX_VELOCITY, min(MAX_VELOCITY, self.velocity.y))

        self.coords.pos += self.velocity

        # Decrease velocity gradually if player is not pushing throttle
        if not self.throttle_on:
            self.velocity *= 0.95

        super().update()

    def render(self):
        """Render the entity on the screen"""
        image = pygame.transform.rotate(self.image, self.coords.rotation.to_degrees())
        return image.copy()


class Bullet(Entity):
    """
    A Bullet entity that is shot by the player, leaving
    behind a bullet trail and moving forwards for 10 secs
    """

    coords: Coords
    sprite: pygame.Surface
    time_created: float

    def __init__(self, coords: Coords):
        super().__init__(coords, Vector2(1, 1))
        self.sprite = pygame.image.load("assets/ammo/ammo.png").convert_alpha()
        self.time_created = pygame.time.get_ticks()

    def update(self):
        """Called every frame, at 60 frames a second"""
        # Destroy bullets after 5 seconds
        if pygame.time.get_ticks() - self.time_created > 5000:
            self.dead = True
            return

        BULLET_SPEED = 25
        self.coords.pos -= self.coords.forward() * BULLET_SPEED
        super().update()

    def render(self):
        """Render the entity on the screen"""
        # Image is a small red rectangle with a bullet trail
        image = pygame.transform.scale(self.sprite, (3, 8))

        # Draw bullet trail
        # pygame.draw.line(image, (255, 0, 0), (1, 0), (1, 50))

        # Draw bullet
        # pygame.draw.rect(ima ge, (255, 0, 0), pygame.Rect(0, 0, 3, 8))

        # Rotate bullet
        image = pygame.transform.rotate(image, self.coords.rotation.to_degrees())
        return image.copy()
