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
    
    def search(self, p: Point2D):
        """
        The algorithms for search is similar to those for BSTs,
        but:
        
        1) at the root we use the x-coordinate, then:
                - if the `p` has a smaller than the point at the
                root, go left;
                - otherwise go right.
        
        2) then at the next level, we use the y-coordinate:
                - if `p` gas a smaller y-coordinate than the point
                in the node, go left;
                - otherwise go right.
            
        3) then at the next level, we use the x-coordinate again,
        and so forth. 
        """
        if not isinstance(p, Point2D):
            raise TypeError
        
        subtree = self.root
        x_y = True  # x_y == True: use x-coordinate; y- otherwise
        
        while subtree is not None:
            if p == subtree.p:
                return True
            
            subtree_coord = (x_y and subtree.p.x) or (not x_y and subtree.p.y)
            p_coord = (x_y and p.x) or (not x_y and p.y)
            
            if p_coord < subtree_coord:
                subtree = subtree.lb
        
            elif p_coord >= subtree_coord:
                subtree = subtree.rt
                
            x_y = not x_y
            
        return False
    
    def contains(self, p: Point2D):
        if not isinstance(p, Point2D):
            raise TypeError
        
        return self.search(p)
        
    def insert(self, p: Point2D):
        """
        The algorithms for insert is similar to those for BSTs,
        but:
        
        1) at the root we use the x-coordinate, then:
                - if the point to be inserted has a smaller
                x-coordinate than the point at the root, go left;
                - otherwise go right.
        
        2) then at the next level, we use the y-coordinate:
                - if the point to be inserted has a smallery-coordinate
                than the point in the node, go left;
                - otherwise go right.
            
        3) then at the next level, we use the x-coordinate again,
        and so forth. 
        """
        if not isinstance(p, Point2D):
            raise TypeError
        
        if self.contains(p):
            return
        
        self.root = self._insert(p, self.root)
        
    def _insert(self, p: Point2D, subtree: _Node, x_y: bool = True):
        # hit a leaf
        if subtree is None:
            return self._Node(p)
        
        subtree_coord = (x_y and subtree.p.x) or (not x_y and subtree.p.y)
        p_coord = (x_y and p.x) or (not x_y and p.y)
        
        if p_coord < subtree_coord:
            subtree.lb = self._insert(p, subtree.lb, not x_y)
    
        else: # p_coord >= subtree_coord:
            subtree.rt = self._insert(p, subtree.rt, not x_y)
        
        subtree.size = 1 + self._size(subtree.lb) + self._size(subtree.rt)
        return subtree
        
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

    def test_search_empty_tree(self):
        self.assertFalse(self.kd_tree.search(Point2D(1, 1)))
    
    def test_search_type_error(self):
        with self.assertRaises(TypeError):
            self.kd_tree.search(1)
    
    def test_search_not_in_tree(self):
        self.kd_tree.root = KDTree._Node(Point2D(1, 1))
        self.assertFalse(self.kd_tree.search(Point2D(1, 2)))
    
    def test_search(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(1, 2)
        p3 = Point2D(0, 2)
        
        # at root
        self.kd_tree.root = KDTree._Node(p1)
        self.assertTrue(self.kd_tree.search(p1))
        
        # deeper to the right
        self.kd_tree.root.rt = KDTree._Node(p2)
        self.assertTrue(self.kd_tree.search(p2))
    
        # deeper to the left
        self.kd_tree.root.lb = KDTree._Node(p3)
        self.assertTrue(self.kd_tree.search(p3))
        
    def test_contains_empty_tree(self):
        self.assertFalse(self.kd_tree.contains(Point2D(1, 1)))
        
    def test_contains_type_error(self):
        with self.assertRaises(TypeError):
            self.kd_tree.contains(1)
    
    def test_contains_not_in_tree(self):
        self.kd_tree.root = KDTree._Node(Point2D(1, 1))
        self.assertFalse(self.kd_tree.contains(Point2D(1, 2)))
    
    def test_contains(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(1, 2)
        p3 = Point2D(0, 2)
        
        # at root
        self.kd_tree.root = KDTree._Node(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        
        # deeper to the right
        self.kd_tree.root.rt = KDTree._Node(p2)
        self.assertTrue(self.kd_tree.contains(p2))
    
        # deeper to the left
        self.kd_tree.root.lb = KDTree._Node(p3)
        self.assertTrue(self.kd_tree.contains(p3))
        
    def test_insert_empty_tree(self):
        p1 = Point2D(1, 1)
        
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertEqual(self.kd_tree.size, 1)
        self.assertIs(self.kd_tree.root.p, p1)
        
    def test_insert(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(2, 2)
        p3 = Point2D(0, 0)
        
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertEqual(self.kd_tree.size, 1)
        
        self.kd_tree.insert(p2)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertTrue(self.kd_tree.contains(p2))
        self.assertEqual(self.kd_tree.size, 2)
        
        self.kd_tree.insert(p3)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertTrue(self.kd_tree.contains(p2))
        self.assertTrue(self.kd_tree.contains(p3))
        self.assertEqual(self.kd_tree.size, 3)
        
    def test_insert_existing_element(self):
        p1 = Point2D(1, 1)
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertEqual(self.kd_tree.size, 1)
        
        p2 = Point2D(1, 1)
        self.kd_tree.insert(p2)
        self.assertTrue(self.kd_tree.contains(p2))
        self.assertIsNot(self.kd_tree.root, p2)
        self.assertEqual(self.kd_tree.size, 1)
        
    def test_insert_type_error(self):
        p = 1
        with self.assertRaises(TypeError):
            self.kd_tree.insert(p)
          