"""Test the pos module"""

import unittest
import math
from pos import Vector2, Rotation, Coords


class TestVector2(unittest.TestCase):
    """Test the Vector2 class"""

    def test_addition(self):
        """Test the addition operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        v3 = v1 + v2
        self.assertEqual(v3, Vector2(4, 6))

    def test_subtraction(self):
        """Test the subtraction operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        v3 = v1 - v2
        self.assertEqual(v3, Vector2(-2, -2))

    def test_multiplication(self):
        """Test the multiplication operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        v3 = v1 * v2
        self.assertEqual(v3, Vector2(3, 8))

    def test_division(self):
        """Test the division operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        v3 = v1 / v2
        self.assertEqual(v3, Vector2(1 / 3, 1 / 2))

    def test_floor_division(self):
        """Test the floor division operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        v3 = v1 // v2
        self.assertEqual(v3, Vector2(0, 0))

    def test_equality(self):
        """Test the equality operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(1, 2)
        self.assertEqual(v1, v2)

    def test_inequality(self):
        """Test the inequality operator"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        self.assertNotEqual(v1, v2)

    def test_to_int(self):
        """Test the to_int method"""
        v1 = Vector2(1.5, 2.7)
        v2 = v1.to_int()
        self.assertEqual(v2, Vector2(1, 2))

    def test_to_int_tuple(self):
        """Test the to_int_tuple method""" ""
        v1 = Vector2(1.5, 2.7)
        v2 = v1.to_int_tuple()
        self.assertEqual(v2, (1, 2))

    def test_to_tuple(self):
        """Test the to_tuple method"""
        v1 = Vector2(1.5, 2.7)
        v2 = v1.to_tuple()
        self.assertEqual(v2, (1.5, 2.7))


class TestRotation(unittest.TestCase):
    """Test the Rotation class"""

    def test_addition(self):
        """Test the addition operator""" ""
        r1 = Rotation(0.5)
        r2 = Rotation(1.2)
        r3 = r1 + r2
        self.assertEqual(r3, Rotation(1.7))

    def test_subtraction(self):
        """Test the subtraction operator"""
        r1 = Rotation(0.5)
        r2 = Rotation(1.2)
        r3 = r1 - r2
        self.assertEqual(r3, Rotation(-0.7))

    def test_multiplication(self):
        """Test the multiplication operator"""
        r1 = Rotation(0.5)
        r2 = Rotation(1.2)
        r3 = r1 * r2
        self.assertEqual(r3, Rotation(0.6))

    def test_division(self):
        """Test the division operator""" ""
        r1 = Rotation(0.5)
        r2 = Rotation(1.2)
        r3 = r1 / r2
        self.assertEqual(r3, Rotation(0.4166666666666667))

    def test_floor_division(self):
        """Test the floor division operator"""
        r1 = Rotation(0.5)
        r2 = Rotation(1.2)
        r3 = r1 // r2
        self.assertEqual(r3, Rotation(0.0))

    def test_equality(self):
        """Test the equality operator""" ""
        r1 = Rotation(0.5)
        r2 = Rotation(0.5)
        self.assertEqual(r1, r2)

    def test_inequality(self):
        """Test the inequality operator"""
        r1 = Rotation(0.5)
        r2 = Rotation(1.2)
        self.assertNotEqual(r1, r2)

    def test_to_degrees(self):
        """Test the to_degrees method"""
        r1 = Rotation(math.pi)
        self.assertEqual(r1.to_degrees(), 180.0)


class TestCoords(unittest.TestCase):
    """Test the Coords class"""

    def test_addition(self):
        """Test the addition operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(3, 4), Rotation(1.2))
        c3 = c1 + c2
        self.assertEqual(c3, Coords(Vector2(4, 6), Rotation(1.7)))

    def test_subtraction(self):
        """Test the subtraction operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(3, 4), Rotation(1.2))
        c3 = c1 - c2
        self.assertEqual(c3, Coords(Vector2(-2, -2), Rotation(-0.7)))

    def test_multiplication(self):
        """Test the multiplication operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(3, 4), Rotation(1.2))
        c3 = c1 * c2
        self.assertEqual(c3, Coords(Vector2(3, 8), Rotation(0.6)))

    def test_division(self):
        """Test the division operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(3, 4), Rotation(1.2))
        c3 = c1 / c2
        self.assertEqual(
            c3, Coords(Vector2(1 / 3, 1 / 2), Rotation(0.4166666666666667))
        )

    def test_floor_division(self):
        """Test the floor division operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(3, 4), Rotation(1.2))
        c3 = c1 // c2
        self.assertEqual(c3, Coords(Vector2(0, 0), Rotation(0.0)))

    def test_equality(self):
        """Test the equality operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(1, 2), Rotation(0.5))
        self.assertEqual(c1, c2)

    def test_inequality(self):
        """Test the inequality operator"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        c2 = Coords(Vector2(3, 4), Rotation(1.2))
        self.assertNotEqual(c1, c2)

    def test_right(self):
        """Test the right method"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        self.assertEqual(c1.right(), Vector2(0.8775825618903728, -0.479425538604203))

    def test_left(self):
        """Test the left method"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        self.assertEqual(c1.left(), Vector2(-0.8775825618903728, 0.479425538604203))

    def test_forward(self):
        """Test the forward method"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        self.assertEqual(c1.forward(), Vector2(0.479425538604203, 0.8775825618903728))

    def test_backward(self):
        """Test the backward method"""
        c1 = Coords(Vector2(1, 2), Rotation(0.5))
        self.assertEqual(
            c1.backward(), Vector2(-0.479425538604203, -0.8775825618903728)
        )


if __name__ == "__main__":
    unittest.main()
