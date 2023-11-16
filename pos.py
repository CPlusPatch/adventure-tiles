""" This file contains the Pos class, which is used to represent a 2D position in the game """

import math


class Vector2:
    """A 2D vector"""

    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def length(self):
        """Get the length of the vector"""
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        """Get the normalized vector"""
        length = self.length()
        return Vector2(self.x / length, self.y / length)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Multiply the vector by another vector or a scalar"""
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        """Divide the vector by another vector or a scalar"""
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        """Divide the vector by another vector or a scalar (floor)"""
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        else:
            return Vector2(self.x // other, self.y // other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self.__eq__(other)

    def to_int(self):
        """Convert the vector to integers"""
        return Vector2(int(self.x), int(self.y))

    def to_int_tuple(self):
        """Convert the vector to integers, and then to a tuple"""
        return (int(self.x), int(self.y))

    def to_tuple(self):
        """Convert the vector to a tuple"""
        return (self.x, self.y)

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"


class Rotation:
    """A rotation, in radians (clamped to 2pi)"""

    rotation: float

    def __init__(self, rotation: float):
        self.rotation = rotation

    @staticmethod
    def from_degrees(degrees: float):
        """Create a rotation from degrees"""
        return Rotation(math.radians(degrees))

    def to_degrees(self):
        """Convert the rotation to degrees"""
        return math.degrees(self.rotation)

    def __add__(self, other):
        """Adds two rotations together"""
        return Rotation(self.rotation + other.rotation)

    def __sub__(self, other):
        """Subtracts two rotations together"""
        return Rotation(self.rotation - other.rotation)

    def __mul__(self, other):
        """Multiplies two rotations together"""
        return Rotation(self.rotation * other.rotation)

    def __truediv__(self, other):
        """Divides two rotations together"""
        return Rotation(self.rotation / other.rotation)

    def __floordiv__(self, other):
        """Divides two rotations together (floor)"""
        return Rotation(self.rotation // other.rotation)

    def __eq__(self, other):
        return self.rotation == other.rotation

    def __neq__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"Rotation({self.rotation})"


class Coords:
    """Holds Position and Rotation data"""

    pos: Vector2
    rotation: Rotation

    def __init__(self, pos: Vector2, rotation: Rotation | None = None):
        self.pos = pos
        self.rotation = rotation if rotation is not None else Rotation(0)

    def __add__(self, other):
        """Adds two coordinates together"""
        return Coords(self.pos + other.pos, self.rotation + other.rotation)

    def __sub__(self, other):
        """Subtracts two coordinates together"""
        return Coords(self.pos - other.pos, self.rotation - other.rotation)

    def __mul__(self, other):
        """Multiplies two coordinates together"""
        return Coords(self.pos * other.pos, self.rotation * other.rotation)

    def __truediv__(self, other):
        """Divides two coordinates together"""
        return Coords(self.pos / other.pos, self.rotation / other.rotation)

    def __floordiv__(self, other):
        """Divides two coordinates together (floor)"""
        return Coords(self.pos // other.pos, self.rotation // other.rotation)

    def __eq__(self, other):
        return self.pos == other.pos and self.rotation == other.rotation

    def __neq__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"Coords({self.pos}, {self.rotation})"

    def right(self):
        """
        Get the right vector of the coordinates, based on
        internal position and rotation (in radians)
        """
        return Vector2(
            math.cos(self.rotation.rotation),
            -math.sin(self.rotation.rotation),
        )

    def left(self):
        """
        Get the left vector of the coordinates, based on
        internal position and rotation (in radians)
        """
        return Vector2(
            -math.cos(self.rotation.rotation),
            math.sin(self.rotation.rotation),
        )

    def forward(self):
        """
        Get the forward vector of the coordinates, based on
        internal position and rotation (in radians)
        """
        return Vector2(
            math.sin(self.rotation.rotation),
            math.cos(self.rotation.rotation),
        )

    def backward(self):
        """
        Get the backward vector of the coordinates, based on
        internal position and rotation (in radians)
        """
        return Vector2(
            -math.sin(self.rotation.rotation),
            -math.cos(self.rotation.rotation),
        )

    def __repr__(self):
        return self.__str__()
