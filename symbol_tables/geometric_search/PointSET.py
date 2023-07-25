from Point2D import Point2D, TestsPoint2D
from RectHV import RectHV, TestsRectHV
from typing import Set

class PointSET:
    
    def __init__(self):
        self.point_set: Set[Point2D] = set()
        
    @property
    def is_empty(self):
        return self.size == 0
    
    @property
    def size(self):
        return len(self.point_set)
    
    def insert(self, p: Point2D):
        if not isinstance(p, Point2D):
            raise TypeError
        
        self.point_set.add(p)
        
    def contains(self, p: Point2D):
        if not isinstance(p, Point2D):
            raise TypeError
        
        return p in self.point_set
    
    def range(self, r: RectHV):
        if not isinstance(r, RectHV):
            raise TypeError
        
        points = set()
        for p in self.point_set:
            if r.contains(p):
                points.add(p)
        
        return points

    def nearest(self, p: Point2D) -> Point2D:
        """a nearest neighbor in the set to point p; null if the set is empty"""
        if not isinstance(p, Point2D):
            raise TypeError
        
        if self.is_empty:
            return None
        
        closest_distance = float('inf')
        nearest = None
        
        for point in self.point_set:
            distance = p.distance_squared(point)
            
            if distance < closest_distance:
                closest_distance = distance
                nearest = point
                
        return nearest
    
# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
import unittest

class TestsPointSET(unittest.TestCase):
    def setUp(self) -> None:
        self.point_set = PointSET()
        
    def test_set_is_empty(self):
        self.assertTrue(self.point_set.is_empty)
    
    def test_set_is_not_empty(self):
        self.point_set.insert(Point2D(1, 1))
        self.assertFalse(self.point_set.is_empty)
        
    def test_size(self):
        # empty
        self.assertEqual(self.point_set.size, 0)
        
        # 1 element
        self.point_set.insert(Point2D(1, 1))
        self.assertEqual(self.point_set.size, 1)
        
        # many elements
        self.point_set.insert(Point2D(2, 2))
        self.point_set.insert(Point2D(3, 3))
        self.assertEqual(self.point_set.size, 3)
    
    def test_insert(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(2, 2)
        
        self.point_set.insert(p1)
        self.assertTrue(self.point_set.contains(p1))
        self.assertEqual(self.point_set.size, 1)
        
        self.point_set.insert(p2)
        self.assertTrue(self.point_set.contains(p2))
        self.assertEqual(self.point_set.size, 2)
        
    def test_insert_existing_element(self):
        p = Point2D(1, 1)
        self.point_set.insert(p)
        self.assertTrue(self.point_set.contains(p))
        self.point_set.insert(p)
        self.assertTrue(self.point_set.contains(p))
        self.assertEqual(self.point_set.size, 1)
        
    def test_insert_type_error(self):
        p = 1
        with self.assertRaises(TypeError):
            self.point_set.insert(p)
            
    def test_contains(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(2, 2)
        
        self.point_set.insert(p1)
        # contains
        self.assertTrue(self.point_set.contains(p1))
        # does not contain
        self.assertFalse(self.point_set.contains(p2))
    
    def test_contains_type_error(self):
        p = 1
        with self.assertRaises(TypeError):
            self.point_set.contains(p)
            
    def test_range(self):
        rect = RectHV(1, 2, 5, 5)

        point_inside = Point2D(3, 3)
        point_on_boundary = Point2D(1, 2)
        point_outside = Point2D(6, 6)
        
        self.point_set.insert(point_inside)
        self.point_set.insert(point_on_boundary)
        self.point_set.insert(point_outside)

        contained_points = self.point_set.range(rect)
        
        self.assertTrue(point_inside in contained_points)
        self.assertTrue(point_on_boundary in contained_points)
        self.assertFalse(point_outside in contained_points)

    def test_range_not_a_rectHV(self):
        rect = 1
        with self.assertRaises(TypeError):
            self.point_set.range(rect)

    def test_nearest_not_a_point2d(self):
        self.point_set.insert(Point2D(1, 1))
        p = (1, 1)
        with self.assertRaises(TypeError):
            self.point_set.nearest(p)
    
    def test_nearest_empty_set(self):
        self.assertIsNone(self.point_set.nearest(Point2D(1, 1)))
        
    def test_nearest_single_point(self):
        p1 = Point2D(1, 1)
        self.point_set.insert(p1)

        p2 = Point2D(2, 2)
        result = self.point_set.nearest(p2)
        self.assertEqual(result, p1)

    def test_nearest_multiple_points(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(2, 2)
        p3 = Point2D(3, 3)
        self.point_set.insert(p1)
        self.point_set.insert(p2)
        self.point_set.insert(p3)

        # The nearest point to a point in the set is the point iself
        result = self.point_set.nearest(p1)
        self.assertEqual(result, p1)
        result = self.point_set.nearest(p2)
        self.assertEqual(result, p2)
        result = self.point_set.nearest(p3)
        self.assertEqual(result, p3)
        
        p4 = Point2D(0, 0)
        result = self.point_set.nearest(p4)
        self.assertEqual(result, p1)
        
        p5 = Point2D(2.2, 1.8)
        result = self.point_set.nearest(p5)
        self.assertEqual(result, p2)
        
        p6 = Point2D(5, 5)
        result = self.point_set.nearest(p6)
        self.assertEqual(result, p3)

    