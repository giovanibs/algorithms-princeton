from dataclasses import dataclass
import math
from Point2D import Point2D, TestsPoint2D

@dataclass(frozen=True)
class RectHV:
    """
    The RectHV class is an immutable data type to encapsulate a
    two-dimensional axis-aligned rectangle with real-value coordinates.
    The rectangle is closed — it includes the points on the boundary.
    """
    
    x_min: float    # x-coordinate of the lower-left endpoint
    y_min: float    # y-coordinate of the lower-left endpoint
    x_max: float    # x-coordinate of the upper-right endpoint
    y_max: float    # y-coordinate of the upper-right endpoint
    
    def __post_init__(self):
        """
        Perform post-initialization checks and conversions.

        Raises:
            TypeError: If the coordinates are not numeric.
            ValueError: If x_min > x_max or y_min > y_max.
        """
        try:
            super().__setattr__('x_min', float(self.x_min))
            super().__setattr__('x_max', float(self.x_max))
            super().__setattr__('y_min', float(self.y_min))
            super().__setattr__('y_max', float(self.y_max))
        except ValueError:
            raise TypeError("Coordinates must be numeric.")
        
        # Check for x/y_max < x/y_min (after conversion to float)
        if self.x_min > self.x_max:
            raise ValueError("x_min > x_max")
        
        if self.y_min > self.y_max:
            raise ValueError("y_min > y_max")
    
    @property
    def width(self) -> float:
        """
        Get the width of the rectangle.

        Returns:
            float: The width of the rectangle.
        """
        return self.x_max - self.x_min
    
    @property
    def height(self) -> float:
        """
        Get the height of the rectangle.

        Returns:
            float: The height of the rectangle.
        """
        return self.y_max - self.y_min
    
    def intersects(self, other: 'RectHV') -> bool:
        """
        Check if this rectangle intersects with another rectangle.

        Args:
            other (RectHV): The other rectangle to check for intersection.

        Returns:
            bool: True if the rectangles intersect; otherwise, False.
        """
        return self.x_max >= other.x_min \
                and self.y_max >= other.y_min \
                    and self.x_min <= other.x_max \
                        and self.y_min <= other.y_max
    
    def contains(self, p: Point2D) -> bool:
        """
        Check if this rectangle contains a point.

        Args:
            p (Point2D): Point2D object with x- and y-coordinates.

        Returns:
            bool: True if the point is inside or on the boundary of the
            rectangle; otherwise, False.
        """
        return p.x >= self.x_min \
                and p.x <= self.x_max \
                    and p.y >= self.y_min \
                        and p.y <= self.y_max
    
    def distance(self, p: Point2D) -> float:
        """
        Calculate the Euclidean distance from a point to the closest point
        in the rectangle.

        Args:
            p (Point2D): Point2D object with x- and y-coordinates.

        Returns:
            float: The Euclidean distance from the point to the rectangle.
        """
        return math.sqrt(self.distance_squared(p))
        
    def distance_squared(self, p: Point2D) -> float:
        """
        Calculate the square of the Euclidean distance from a point to the
        closest point in the rectangle.

        Args:
            p (Point2D): Point2D object with x- and y-coordinates.

        Returns:
            float: The squared Euclidean distance from the point to the
            rectangle.
        """
        dx = 0.0
        dy = 0.0
        
        if p.x < self.x_min:
            dx = p.x - self.x_min
        elif p.x > self.x_max:
            dx = p.x - self.x_max
            
        if p.y < self.y_min:
            dy = p.y - self.y_min
        elif p.y > self.y_max:
            dy = p.y - self.y_max
        
        return dx*dx + dy*dy
    
    def __sub__(self, other: 'RectHV') -> 'RectHV':
        """
        Subtract one rectangle from another, assuming that `other`
        is the RIGHT/TOP SUBPLANE resulting from splitting `self`
        by either a VERTICAL or a HORIZONTAL line.

        Args:
            other (RectHV): The rectangle to be subtracted.

        Returns:
            RectHV: A new rectangle representing the subtraction result.
        """
        # left/botton corner is kept the same
        x_min = self.x_min
        y_min = self.y_min
        
        # top/right corner
        x_max = other.x_min if (other.x_min - self.x_min) else self.x_max
        y_max = other.y_min if (other.y_min - self.y_min) else self.y_max
        
        return RectHV(x_min, y_min, x_max, y_max)

    def split_at(self, point: Point2D, vertically: bool):
        """Splits the rectangle into 2 subplanes by either the
        vertical/horizontal line containing `point` and returns
        a tuple containing both subplanes (left/bot and right/top
        respectively).
        
        We assume `point` is INSIDE the rectangle (not on the border).
        """
        
        if vertically:
            rt = RectHV(point.x, self.y_min, self.x_max, self.y_max)
        else:
            rt = RectHV(self.x_min, point.y, self.x_max, self.y_max)
        
        return self - rt, rt
        
# ------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------
import unittest

class TestsRectHV(unittest.TestCase):
    
    def test_init(self):
        # floats
        rect1 = RectHV(-1.0, 2.0, 3.0, 5.0)
        self.assertIsInstance(rect1, RectHV)

        # integers
        rect2 = RectHV(1, -2, 4, 6)
        self.assertIsInstance(rect2, RectHV)

        # numeric strings
        rect3 = RectHV("-1.5", "-3.5", "1.5", "0")
        self.assertIsInstance(rect3, RectHV)

    def test_init_wrong_type(self):
        # non-numeric coordinates
        with self.assertRaises(TypeError):
            RectHV(1.0, "two", 3.0, 5.0)

        with self.assertRaises(TypeError):
            RectHV(1.0, 2.0, 3, [5])

    def test_init_wrong_coordinate(self):
        # x_min > x_max
        with self.assertRaises(ValueError):
            RectHV(5, 2, 3, 5)

        # y_min > y_max
        with self.assertRaises(ValueError):
            RectHV(1, 2, 3, 1)

    def test_width(self):
        rect = RectHV(1, 2, 3, 5)
        self.assertEqual(rect.width, 2)

    def test_height(self):
        rect = RectHV(1, 2, 3, 5)
        self.assertEqual(rect.height, 3)

    def test_intersects(self):
        rect1 = RectHV(1, 2, 5, 5)
        rect2 = RectHV(3, 1, 6, 4)
        rect3 = RectHV(6, 6, 8, 8)

        self.assertTrue(rect1.intersects(rect2))
        self.assertTrue(rect2.intersects(rect1))
        self.assertFalse(rect1.intersects(rect3))
        self.assertFalse(rect2.intersects(rect3))

    def test_contains(self):
        rect = RectHV(1, 2, 5, 5)

        point_inside = Point2D(3, 3)
        point_on_boundary = Point2D(1, 2)
        point_outside = Point2D(6, 6)

        self.assertTrue(rect.contains(point_inside))
        self.assertTrue(rect.contains(point_on_boundary))
        self.assertFalse(rect.contains(point_outside))

    def test_distance(self):
        rect = RectHV(1, 2, 5, 5)

        point_inside = Point2D(3, 3)
        point_outside1 = Point2D(6, 6)
        point_outside2 = Point2D(0, 1) # p.x < x_min && p.y < self.y_min
        self.assertAlmostEqual(rect.distance(point_inside), 0)
        self.assertAlmostEqual(rect.distance(point_outside1), 1.414, places=3)
        self.assertAlmostEqual(rect.distance(point_outside2), 1.414, places=3)

    def test_distance_squared(self):
        rect = RectHV(1, 2, 5, 5)

        point_inside = Point2D(3, 3)
        point_outside1 = Point2D(6, 6)
        point_outside2 = Point2D(0, 1) # p.x < x_min && p.y < self.y_min

        self.assertAlmostEqual(rect.distance_squared(point_inside), 0)
        self.assertAlmostEqual(rect.distance_squared(point_outside1), 2)
        self.assertAlmostEqual(rect.distance_squared(point_outside2), 2)

    def test_subtraction(self):
        # subtract left/bot subplane (from vertical split)
        r1 = RectHV(0, 0, 1, 1)
        r2 = RectHV(.3, 0, 1, 1)
        expected = RectHV(0, 0, .3, 1)
        result = r1 - r2
        self.assertEqual(expected, result)
        
        # subtract right/top subplane (from horizontal split)
        r3 = RectHV(0, .3, 1, 1)
        expected = RectHV(0, 0, 1, .3)
        result = r1 - r3
        self.assertEqual(expected, result)
        
    def test_split_vertically(self):
        vertically = True
        p = Point2D(0.4, 0.6)
        
        # split unit square
        r = RectHV(0, 0, 1, 1)
        expected_lb = RectHV(0, 0, .4, 1)
        expected_rt = RectHV(.4, 0, 1, 1)
        lb, rt = r.split_at(p, vertically)
        self.assertEqual(expected_lb, lb)
        self.assertEqual(expected_rt, rt)
        
        # split other
        r = RectHV(.2, .3, .7, .8)
        expected_lb = RectHV(.2, .3, .4, .8)
        expected_rt = RectHV(.4, .3, .7, .8)
        lb, rt = r.split_at(p, vertically)
        self.assertEqual(expected_lb, lb)
        self.assertEqual(expected_rt, rt)
        
    def test_split_horizontally(self):
        horizontally = False
        p = Point2D(0.4, 0.6)
        
        # split unit square
        r = RectHV(0, 0, 1, 1)
        expected_lb = RectHV(0, 0, 1, .6)
        expected_rt = RectHV(0, .6, 1, 1)
        lb, rt = r.split_at(p, horizontally)
        self.assertEqual(expected_lb, lb)
        self.assertEqual(expected_rt, rt)
        
        # split other
        r = RectHV(.2, .3, .7, .8)
        expected_lb = RectHV(.2, .3, .7, .6)
        expected_rt = RectHV(.2, .6, .7, .8)
        lb, rt = r.split_at(p, horizontally)
        self.assertEqual(expected_lb, lb)
        self.assertEqual(expected_rt, rt)
