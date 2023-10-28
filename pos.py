""" This file contains the Pos class, which is used to represent a 2D position in the game """

from variables import RESOLUTION, ZOOM


class Pos:
    """A 2D position, inside the game (center is 0,0)"""

    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Pos(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Pos(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Pos(self.x // other.x, self.y // other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self.__eq__(other)

    def to_int(self):
        """Convert the position to integers"""
        return Pos(int(self.x), int(self.y))

    def to_int_tuple(self):
        """Convert the position to integers, and then to a tuple"""
        return (int(self.x), int(self.y))

    def to_tuple(self):
        """Convert the position to a tuple"""
        return (self.x, self.y)

    def to_window_coords(self):
        """Convert the position to window coordinates, counting for zoom"""
        return Pos(
            self.x * 16 * ZOOM + RESOLUTION[0] / 2,
            self.y * 16 * ZOOM + RESOLUTION[1] / 2,
        )
