from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from Point2D import Point2D, TestsPoint2D
from RectHV import RectHV, TestsRectHV

class KDTree:
    """Mutable data type to represent a set of points in
    the unit square (all points have x- and y-coordinates
    between 0 and 1).
    
    We use an implementation of a 2d-tree for efficient
    range search (find all of the points contained in a
    query rectangle) and nearest-neighbor search (find
    a closest point to a query point)."""
    
    @dataclass
    class _Node:
        p: Point2D
        r: RectHV   = None
        lb: '_Node' = None     # the left/bottom subtree
        rt: '_Node' = None     # the right/top subtree
        size: int   = 1
    
    def __init__(self):
        self.root: Union[None, '_Node'] = None
        
    @property
    def is_empty(self):
        return self.root is None
    
    @property
    def size(self):
        return self._size(self.root)
    
    def _size(self, subtree):
        if subtree is None:
            return 0
        
        return subtree.size
    
    def insert(self, p: Point2D):
        if not isinstance(p, Point2D):
            raise TypeError
        
    def contains(self, p: Point2D):
        if not isinstance(p, Point2D):
            raise TypeError
        
    def range(self, r: RectHV):
        if not isinstance(r, RectHV):
            raise TypeError
        
    def nearest(self, p: Point2D) -> Point2D:
        """a nearest neighbor in the set to point p; null if the set is empty"""
        if not isinstance(p, Point2D):
            raise TypeError
        
        if self.is_empty:
            return None
        
# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
import unittest

class TestsKDTree(unittest.TestCase):
    def setUp(self) -> None:
        self.kd_tree = KDTree()
        
    def test_tree_is_empty(self):
        self.assertTrue(self.kd_tree.is_empty)
    
    def test_tree_is_not_empty(self):
        self.kd_tree.root = Point2D(1, 1)
        self.assertFalse(self.kd_tree.is_empty)
        
    def test_size(self):
        # empty
        self.assertEqual(self.kd_tree.size, 0)
        
        # # 1 element
        self.kd_tree.root = self.kd_tree._Node(Point2D(1, 1))
        self.assertEqual(self.kd_tree.size, 1)
        
        # # many elements
        self.kd_tree.root.size = 3
        self.assertEqual(self.kd_tree.size, 3)
