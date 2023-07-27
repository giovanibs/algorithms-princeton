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
    X_MIN = Y_MIN = 0
    X_MAX = Y_MAX = 1
    UNIT_SQUARE = RectHV(X_MIN, Y_MIN, X_MAX, Y_MAX)
    SPLIT_V = True  # split plane vertically
    SPLIT_H = False # split plane horizontally
    
    def __init__(self):
        self.root: Union[None, '_Node'] = None
    
    @dataclass
    class _Node:
        point: Point2D
        parent: '_Node' = None
        outer_rect: RectHV = None
        rect: RectHV   = None
        lb: '_Node' = None     # the left/bottom subtree
        rt: '_Node' = None     # the right/top subtree
        size: int   = 1
        split: bool = True     # spliting vertically(True) or horizontally
        
        def __post_init__(self):
            if not KDTree.UNIT_SQUARE.contains(self.point):
                raise ValueError(f"Point `{self.point}` is out of the unit square.")
            
            # initiate root
            if self.parent is None:
                self.parent = self
            if self.outer_rect is None:
                self.outer_rect = KDTree.UNIT_SQUARE
                
            self._set_rectHV()
                
        def _set_rectHV(self):
            """This method defines the RectHV object associated
            with the node. That is, it space-partitions the plane.
            
            1) VERTICALLY SPLIT:
            
                x_min: subtree.x
                x_max: outer_rectect.x_max
                y_min: outer_rectect.y_min
                    
                1.1) enclosed by its parent
                
                    y_max: outer_rectect.y_max
                
                1.2) not enclosed by its parent
                    
                    y_max: parent.y
            
            2) HORIZONTALLY SPLIT:
                
                x_min: outer_rect.x_min
                y_min: subtree.y
                y_max: outer_rectect.y_max
                
                2.2.1) enclosed by its parent (parent.rect.contains(p))
                
                    x_max: outer_rect.x_max
                    
                2.2.1) not enclosed by its parent
                
                    x_max: parent.x
            """
            # 1) VERTICALLY SPLIT:
            if self.split:
                x_min = self.point.x
                y_min = self.outer_rect.y_min
                x_max = self.outer_rect.x_max
                
                # root or not enclosed by its own parent
                if self.parent is None or self.outer_rect is not self.parent.rect:
                    y_max = self.outer_rect.y_max
                
                # not root, enclosed by its parent
                elif self.outer_rect is self.parent.rect:
                    y_max = self.parent.outer_rect.y_max
                
            # 2) HORIZONTALLY SPLIT:
            else:
                x_min = self.outer_rect.x_min
                y_min = self.point.y
                y_max = self.outer_rect.y_max
                
                # enclosed by its parent
                if self.outer_rect is self.parent.rect:
                    x_max = self.outer_rect.x_max
                
                else: # not enclosed by its parent
                    x_max = KDTree.X_MAX if self.parent is None else self.parent.point.x
            
            # finally set the RectHV
            self.rect = RectHV(x_min, y_min, x_max, y_max)
                  
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
            if p == subtree.point:
                return True
            
            subtree_coord = subtree.point.x if x_y else subtree.point.y
            p_coord = p.x if x_y else p.y
            
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
        
        # takes care of inserting the root
        if self.is_empty:
            self.root = self._Node(p)
            return
        
        if self.contains(p):
            return
        
        self.root = self._insert(p, self.root, self.root)
        
    def _insert(self, p: Point2D, subtree, subtree_parent=None, outer_rect=None):
        """
        """
        x_y = not subtree_parent.split
        
        # 1) hit a leaf
        if subtree is None:
            return self._Node(
                point       = p,
                parent      = subtree_parent,
                outer_rect  = outer_rect,
                split       = x_y
            )
        # 2) p.x/y >= parent.point.x/y 
        if subtree.rect.contains(p):
            subtree.rt = self._insert(
                p               = p,
                subtree         = subtree.rt,
                subtree_parent  = subtree,
                outer_rect      = subtree.rect
            )
        # 3) p.x/y < parent.point.x/y
        else:
            subtree.lb = self._insert(
                p               = p,
                subtree         = subtree.lb,
                subtree_parent  = subtree,
                outer_rect      = subtree.outer_rect
            )
        
        subtree.size = 1 + self._size(subtree.lb) + self._size(subtree.rt)
        return subtree
            
    def range(self, r: RectHV):
        """To find all points contained in a given query rectangle:
        
        1) start at the root
        
        2) recursively search for points in both subtrees using the
        following pruning rule:
                - if the query rectangle does not intersect the
                rectangle corresponding to a node, there is no
                need to explore that node (or its subtrees).
                
        A subtree is searched only if it might contain a point 
        contained in the query rectangle.
        """
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
        self.kd_tree.insert(Point2D(1, 1))
        self.assertFalse(self.kd_tree.is_empty)
        
    def test_size(self):
        # empty
        self.assertEqual(self.kd_tree.size, 0)
        
        # 1 element
        self.kd_tree.insert(Point2D(1, 1))
        self.assertEqual(self.kd_tree.size, 1)
        
        # many elements
        self.kd_tree.insert(Point2D(0.2, 0.2))
        self.kd_tree.insert(Point2D(0.3, 0.3))
        self.assertEqual(self.kd_tree.size, 3)

    def test_search_empty_tree(self):
        self.assertFalse(self.kd_tree.search(Point2D(1, 1)))
    
    def test_search_type_error(self):
        with self.assertRaises(TypeError):
            self.kd_tree.search(1)
    
    def test_search_not_in_tree(self):
        self.kd_tree.insert(Point2D(1, 1))
        self.assertFalse(self.kd_tree.search(Point2D(1, 2)))
    
    def test_search(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(1, 0.2)
        p3 = Point2D(0, 0.2)
        
        # at root
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.search(p1))
        
        # deeper to the right
        self.kd_tree.insert(p2)
        self.assertTrue(self.kd_tree.search(p2))
    
        # deeper to the left
        self.kd_tree.insert(p3)
        self.assertTrue(self.kd_tree.search(p3))
        
    def test_contains_empty_tree(self):
        self.assertFalse(self.kd_tree.contains(Point2D(1, 1)))
        
    def test_contains_type_error(self):
        with self.assertRaises(TypeError):
            self.kd_tree.contains(1)
    
    def test_contains_not_in_tree(self):
        p1 = Point2D(1, 1)
        self.kd_tree.insert(p1)
        p2 = Point2D(1, 0.2)
        self.assertFalse(self.kd_tree.contains(p2))
    
    def test_contains(self):
        p1 = Point2D(1, 1)
        p2 = Point2D(1, 0.2)
        p3 = Point2D(0, 0.2)
        
        # at root
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        
        # deeper to the right
        self.kd_tree.insert(p2)
        self.assertTrue(self.kd_tree.contains(p2))
    
        # deeper to the left
        self.kd_tree.insert(p3)
        self.assertTrue(self.kd_tree.contains(p3))
        
    def test_insert_empty_tree(self):
        p1 = Point2D(1, 1)
        
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertEqual(self.kd_tree.size, 1)
        self.assertIs(self.kd_tree.root.point, p1)
        
    def test_insert(self):
        p1 = Point2D(0.5, 0.5)
        p2 = Point2D(0.2, 0.2)
        p3 = Point2D(0.7, 0.7)
        
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
            
    def test_insert_point_not_in_the_unit_square(self):
        p = Point2D(1, 2)
        with self.assertRaises(ValueError):
            self.kd_tree.insert(p)
        
        self.assertFalse(self.kd_tree.contains(p))

    def test_insert_many_points(self):
        tree = self.kd_tree
        
        p01 = Point2D(0.45, 0.45)
        p02 = Point2D(0.7, 0.4)
        p03 = Point2D(0.3, 0.6)
        p04 = Point2D(0.2, 0.1)
        p05 = Point2D(0.1, 0.5)
        p06 = Point2D(0.4, 0.7)
        p07 = Point2D(0.5, 0.3)
        p08 = Point2D(0.9, 0.9)
        p09 = Point2D(0.8, 0.8)
        p10 = Point2D(0.6, 0.2)
        
        tree.insert(p01)
        tree.insert(p02)
        tree.insert(p03)
        tree.insert(p04)
        tree.insert(p05)
        tree.insert(p06)
        tree.insert(p07)
        tree.insert(p08)
        tree.insert(p09)
        tree.insert(p10)

        # p01
        node01 = tree.root
        self.assertEqual(node01.point, p01)
        self.assertEqual(node01.lb.point, p03)
        self.assertEqual(node01.rt.point, p02)
        expected_outer_rect = KDTree.UNIT_SQUARE
        self.assertEqual(node01.outer_rect, expected_outer_rect)
        
        # p02
        node02 = node01.rt
        self.assertEqual(node02.point, p02)
        self.assertEqual(node02.lb.point, p07)
        self.assertEqual(node02.rt.point, p08)
        expected_outer_rect = node01.rect
        self.assertEqual(node02.outer_rect, expected_outer_rect)
        
        # p03
        node03 = node01.lb
        self.assertEqual(node03.point, p03)
        self.assertEqual(node03.lb.point, p04)
        self.assertEqual(node03.rt.point, p06)
        expected_outer_rect = node01.outer_rect
        self.assertEqual(node03.outer_rect, expected_outer_rect)
        
        # p04
        node04 = node03.lb
        self.assertEqual(node04.point, p04)
        self.assertEqual(node04.lb.point, p05)
        self.assertIsNone(node04.rt)
        expected_outer_rect = node03.outer_rect
        self.assertEqual(node04.outer_rect, expected_outer_rect)
        
        # p05
        node05 = node04.lb
        self.assertEqual(node05.point, p05)
        self.assertIsNone(node05.lb)
        self.assertIsNone(node05.rt)
        expected_outer_rect = node04.outer_rect
        self.assertEqual(node05.outer_rect, expected_outer_rect)
        
        # p06
        node06 = node03.rt
        self.assertEqual(node06.point, p06)
        self.assertIsNone(node06.lb)
        self.assertIsNone(node06.rt)
        expected_outer_rect = node03.rect
        self.assertEqual(node06.outer_rect, expected_outer_rect)
        
        # p07
        node07 = node02.lb
        self.assertEqual(node07.point, p07)
        self.assertIsNone(node07.lb)
        self.assertEqual(node07.rt.point, p10)
        expected_outer_rect = node02.outer_rect
        self.assertEqual(node07.outer_rect, expected_outer_rect)
        
        # p08
        node08 = node02.rt
        self.assertEqual(node08.point, p08)
        self.assertEqual(node08.lb.point, p09)
        self.assertIsNone(node08.rt)
        expected_outer_rect = node02.rect
        self.assertEqual(node08.outer_rect, expected_outer_rect)
        
        # p09
        node09 = node08.lb
        self.assertEqual(node09.point, p09)
        self.assertIsNone(node09.lb)
        self.assertIsNone(node09.rt)
        expected_outer_rect = node08.outer_rect
        self.assertEqual(node09.outer_rect, expected_outer_rect)
        
        # p10
        node10 = node07.rt
        self.assertEqual(node10.point, p10)
        self.assertIsNone(node10.lb)
        self.assertIsNone(node10.rt)
        expected_outer_rect = node07.rect
        self.assertEqual(node10.outer_rect, expected_outer_rect)
        
        
from pprint import pp
if __name__ == "__main__":
    tree = KDTree()
