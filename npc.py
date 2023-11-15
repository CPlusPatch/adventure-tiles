""" NPC class """
from main import Entity


class NPC(Entity):
    """
    NPC class
    """

    def __init__(self, name, pos):
        super().__init__(pos, (1, 2))
        self.name = name
        self.is_walking = False
        self.frame = 0
        self.timer = 0
        self.sprites = []
        self.image = self.sprites[0]
