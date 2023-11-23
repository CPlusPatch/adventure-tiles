"""
This module contains the StarfieldRenderer class,
which is used to render a starfield onto a surface
"""

import random
import pygame
from variables import RESOLUTION

STAR_SIZE_MIN = 2
STAR_SIZE_MAX = 5
STAR_COUNT_MIN = 20 * 8
STAR_COUNT_MAX = 30 * 8


class StarfieldRenderer:
    """This class is used to render a starfield onto a surface"""

    seed: int

    def __init__(self, seed: int):
        self.seed = seed

        # Generate a star texture that covers the entire screen
        self.star_texture = pygame.image.load("assets/starfield.png").convert_alpha()

        # Convert black to transparent
        self.star_texture.set_colorkey((0, 0, 0))

    def render(self, surface: pygame.Surface, camera_position: pygame.Vector2):
        """Render the starfield onto the surface as a tiled texture from the world center"""

        # camera_position is the center of the screen, and the offset from 0,0
        # Render the starfield as a tiled texture from the world center

        # One quadrant is a star_texture size block, 0,0 being the quadrant in the center
        quadrant_x = int(camera_position.x / self.star_texture.get_width())
        quadrant_y = int(camera_position.y / self.star_texture.get_height())

        # Render the starfield with 8 more starfields around it
        for x in range(-1, 2):
            for y in range(-1, 2):
                surface.blit(
                    self.star_texture,
                    (
                        -camera_position.x
                        + ((quadrant_x + x) * self.star_texture.get_width()),
                        -camera_position.y
                        + ((quadrant_y + y) * self.star_texture.get_height()),
                    ),
                )

        random.seed(self.seed)

    def generate_stars(self):
        """Generate stars based on the camera position"""

        # Seed the random generator
        random.seed(self.seed)

        # Generate stars
        for _ in range(100):
            yield (
                random.randint(0, RESOLUTION[0]),
                random.randint(0, RESOLUTION[1]),
                random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX),
            )

        # Unseed the random generator
        random.seed(None)
