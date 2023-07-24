from dataclasses import dataclass, FrozenInstanceError
import math

@dataclass(frozen=True)
class Point2D:
    """
    Immutable point data type for points in a plane.
    """
    
    x: float
    y: float
    
    def __post_init__(self):
        # Runtime type-checking to ensure x and y are both
        # float or convertible to float.
        try:
            # using `super().__setattr__` as workaround
            # to the frozen flag
            super().__setattr__('x', float(self.x))
            super().__setattr__('y', float(self.y))
            
        except ValueError:
            raise TypeError("x and y must be numeric.")
        
    def distance(self, other: 'Point2D') -> float:
        """
        Returns the Euclidean distance between this point and
        `other` point.
        """
        return math.sqrt(self.distance_squared(other))
    
    def distance_squared(self, other: 'Point2D') -> float:
        """
        Returns the square of the Euclidean distance between
        this point and `other` point.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return dx*dx + dy*dy

# ------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------
import unittest

class TestsPoint2D(unittest.TestCase):
    def test_create_point2D(self):
        # floats
        p1 = Point2D(x:=1.0, y:=2.0)
        self.assertEqual(p1.x, float(x))
        self.assertEqual(p1.y, float(y))
        
        # int
        p2 = Point2D(x:=1, y:=2)
        self.assertEqual(p1.x, float(x))
        self.assertEqual(p1.y, float(y))
        
        # numeric string
        p3 = Point2D(x:="1.0", y:="2")
        self.assertEqual(p2.x, float(x))
        self.assertEqual(p2.y, float(y))
    
    def test_create_point2d_type_error(self):
        # non-numeric string
        with self.assertRaises(TypeError):
            Point2D('not a float', 2)
        
        with self.assertRaises(TypeError):
            Point2D("1.0", "not a float 2")
        
        # other objects type
        with self.assertRaises(TypeError):
            Point2D([1], 2)
            
    def test_distance(self):
        # Test distance between two points
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertEqual(p1.distance(p2), 5.0)
    
    def test_distance_squared(self):
        # Test squared distance between two points
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertEqual(p1.distance_squared(p2), 25.0)
    
    def test_immutable(self):
        # Test if the object is immutable
        p = Point2D(2.2, 3.3)
        with self.assertRaises(AttributeError):
            p.x = 4.4
        with self.assertRaises(AttributeError):
            p.y = 5.5
