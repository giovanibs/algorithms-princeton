from typing import Union, ClassVar
from Point2D import Point2D, TestsPoint2D
from RectHV import RectHV, TestsRectHV
from Node import Node, TestsNode
        
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
    UNIT_SQUARE_NODE = Node(Point2D(0,0), None, UNIT_SQUARE)
    
    def __init__(self):
        # virtual node to contain the root point
        self.root: Union[None, Node] = None
    
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
        Inserts point `p` into the plane.
        """
        if not isinstance(p, Point2D):
            raise TypeError
        
        # inserts the root
        if self.is_empty:
            self.root = Node(p)
            return
        
        if self.contains(p):
            return
        
        self.root = self._insert(p, self.root, self.root)
        
    def _insert(self, p: Point2D, subtree, parent=None):
        """The algorithms for insert is similar to those for BSTs,
        but:
        
        1) at the root we use the x-coordinate, then:
                - if the point to be inserted has a smaller
                x-coordinate than the point at the root, go left;
                - otherwise go right.
        
        2) then at the next level, we use the y-coordinate:
                - if the point to be inserted has a smaller
                y-coordinate than the point in the node, go left;
                - otherwise go right.
            
        3) then at the next level, we use the x-coordinate again,
        and so forth.
        
        PS.: Here, to check if the point `p` has a greater
        x-/y-coordinate, we check if the subplane of the parent
        node contains `p`.
        """
        x_y = not parent.split
        
        # hit a leaf --> return the new node
        if subtree is None:
            return Node(p, parent, x_y)
        
        # x- (vert. split) or y-coord (horiz. split) GREATER than parent
        if subtree.rect.contains(p):
            subtree.rt = self._insert(p, subtree.rt, subtree)
        
        else:
            subtree.lb = self._insert(p, subtree.lb, subtree)
        
        # update sizes
        subtree.size = 1 + self._size(subtree.lb) + self._size(subtree.rt)
        return subtree
            
    def range(self, r: RectHV) -> set:
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
        
        points = set()
        
        if self.root is None:
            return points
        
        self._range(r, self.root, points)
        
        return points
            
    def _range(self, r: RectHV, subtree: Node, points: set):
        if subtree is None:
            return points
        
        if r.intersects(subtree.rect):
            if r.contains(subtree.point):
                points.add(subtree.point)
                
            self._range(r, subtree.lb, points)
            self._range(r, subtree.rt, points)
            
        return points
        
    def nearest(self, query_point: Point2D) -> Point2D:
        """To find a closest point to a given query point,
        start at the root and recursively search in both
        subtrees using the following pruning rule:
        
            - if the closest point discovered so far is
            closer than the distance between the query
            point and the rectangle corresponding to a node,
            there is no need to explore that node (or its
            subtrees). That is, search a node only if it
            might contain a point that is closer than the
            best one found so far.
        
        The effectiveness of the pruning rule depends on quickly
        finding a nearby point. To do this, organize the recursive
        method so that when there are two possible subtrees to go
        down, you always choose the subtree that is on the same
        side of the splitting line as the query point as the first
        subtree to explore — the closest point found while exploring
        the first subtree may enable pruning of the second subtree.
        """
        if not isinstance(query_point, Point2D):
            raise TypeError
        
        if self.is_empty:
            return None
        
        nearest = {'point': None, 'dist': float('inf')}
        return self._nearest(query_point, self.root, nearest)['point']
        
    def _nearest(self, query_point: Point2D, subtree: Node, nearest: dict):
        """
        (1) Check distance from point in node to query point.
        (2) Recursively search left/bottom (if it could contain a closer point).
        (3) Recursively search right/top (if it could contain a closer point).
        (4) Organize method so that it begins by searching for query point
        """
        if subtree is None:
            return nearest
        
        # (1)
        subtree_dist = subtree.point.distance_squared(query_point)
        
        if subtree_dist < nearest['dist']:
            nearest['point'] = subtree.point
            nearest['dist'] = subtree_dist
        
        # (2)
        nearest = self._nearest(query_point, subtree.lb, nearest)
        # (3)
        nearest = self._nearest(query_point, subtree.rt, nearest)
        
        return nearest
        
        
# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
import unittest

class TestsKDTree(unittest.TestCase):
    def setUp(self) -> None:
        self.kd_tree = KDTree()
        
    def test_000_tree_is_empty(self):
        self.assertTrue(self.kd_tree.is_empty)
    
    def test_001_tree_is_not_empty(self):
        self.kd_tree.insert(Point2D(1, 1))
        self.assertFalse(self.kd_tree.is_empty)
        
    def test_002_size(self):
        # empty
        self.assertEqual(self.kd_tree.size, 0)
        
        # 1 element
        self.kd_tree.insert(Point2D(1, 1))
        self.assertEqual(self.kd_tree.size, 1)
        
        # many elements
        self.kd_tree.insert(Point2D(0.2, 0.2))
        self.kd_tree.insert(Point2D(0.3, 0.3))
        self.assertEqual(self.kd_tree.size, 3)

    def test_003_search_empty_tree(self):
        self.assertFalse(self.kd_tree.search(Point2D(1, 1)))
    
    def test_004_search_type_error(self):
        with self.assertRaises(TypeError):
            self.kd_tree.search(1)
    
    def test_005_search_not_in_tree(self):
        self.kd_tree.insert(Point2D(1, 1))
        self.assertFalse(self.kd_tree.search(Point2D(1, 2)))
    
    def test_006_search(self):
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
        
    def test_007_contains_empty_tree(self):
        self.assertFalse(self.kd_tree.contains(Point2D(1, 1)))
        
    def test_008_contains_type_error(self):
        with self.assertRaises(TypeError):
            self.kd_tree.contains(1)
    
    def test_009_contains_not_in_tree(self):
        p1 = Point2D(1, 1)
        self.kd_tree.insert(p1)
        p2 = Point2D(1, 0.2)
        self.assertFalse(self.kd_tree.contains(p2))
    
    def test_010_contains(self):
        p1 = Point2D(0.5, 0.5)
        p2 = Point2D(0.7, 0.7)
        p3 = Point2D(0.2, 0.2)
        
        # at root
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        
        # deeper to the right
        self.kd_tree.insert(p2)
        self.assertTrue(self.kd_tree.contains(p2))
    
        # deeper to the left
        self.kd_tree.insert(p3)
        self.assertTrue(self.kd_tree.contains(p3))
        
    def test_011_insert_empty_tree(self):
        p1 = Point2D(1, 1)
        
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertEqual(self.kd_tree.size, 1)
        self.assertIs(self.kd_tree.root.point, p1)
        
    def test_012_insert_existing_element(self):
        p1 = Point2D(1, 1)
        self.kd_tree.insert(p1)
        self.assertTrue(self.kd_tree.contains(p1))
        self.assertEqual(self.kd_tree.size, 1)
        
        p2 = Point2D(1, 1)
        self.kd_tree.insert(p2)
        self.assertTrue(self.kd_tree.contains(p2))
        self.assertIsNot(self.kd_tree.root, p2)
        self.assertEqual(self.kd_tree.size, 1)
        
    def test_013_insert_type_error(self):
        p = 1
        with self.assertRaises(TypeError):
            self.kd_tree.insert(p)
            
    def test_014_insert_point_not_in_the_unit_square(self):
        p = Point2D(1, 2)
        with self.assertRaises(ValueError):
            self.kd_tree.insert(p)
        
        self.assertFalse(self.kd_tree.contains(p))

    def test_015_insert_many_points(self):
        tree = self.kd_tree
        UQ = RectHV(0, 0, 1, 1)
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
        
        # --------- LEVEL 0 / ROOT ---------
        # p01
        tree.insert(p01)
        node01 = tree.root
        self.assertEqual(node01.point, p01)
        expected_rect = RectHV(p01.x, UQ.y_min, UQ.x_max, UQ.y_max)
        self.assertEqual(expected_rect, node01.rect)
        self.assertTrue(node01.split)
        
        # --------- LEVEL 01 ---------
        # p02 
        tree.insert(p02)
        node02 = node01.rt
        self.assertEqual(node02.point, p02)
        expected_rect = RectHV(p01.x, p02.y, UQ.x_max, UQ.y_max)
        self.assertEqual(expected_rect, node02.rect)
        self.assertFalse(node02.split)
        
        # p03
        tree.insert(p03)
        node03 = node01.lb
        self.assertEqual(node03.point, p03)
        expected_rect = RectHV(0, p03.y, p01.x, 1)
        self.assertEqual(expected_rect, node03.rect)
        self.assertFalse(node03.split)
        
        # --------- DEEPER LEVEL ---------
        #  p04
        tree.insert(p04)
        node04 = node03.lb
        self.assertEqual(node04.point, p04)
        expected_rect = RectHV(p04.x, 0, p01.x, p03.y)
        self.assertEqual(expected_rect, node04.rect)
        self.assertTrue(node04.split)
        
        # p05
        tree.insert(p05)
        node05 = node04.lb
        self.assertEqual(node05.point, p05)
        expected_rect = RectHV(0, p05.y, p04.x, p03.y)
        self.assertEqual(expected_rect, node05.rect)
        self.assertFalse(node05.split)
        
        # p06
        tree.insert(p06)
        node06 = node03.rt
        self.assertEqual(node06.point, p06)
        expected_rect = RectHV(p06.x, p03.y, p01.x, 1)
        self.assertEqual(expected_rect, node06.rect)
        self.assertTrue(node06.split)
        
        # p07
        tree.insert(p07)
        node07 = node02.lb
        self.assertEqual(node07.point, p07)
        expected_rect = RectHV(p07.x, 0, 1, p02.y)
        self.assertEqual(expected_rect, node07.rect)
        self.assertTrue(node07.split)
        
        # p08
        tree.insert(p08)
        node08 = node02.rt
        self.assertEqual(node08.point, p08)
        expected_rect = RectHV(p08.x, p02.y, 1, 1)
        self.assertEqual(expected_rect, node08.rect)
        self.assertTrue(node08.split)
        
        # p09
        tree.insert(p09)
        node09 = node08.lb
        self.assertEqual(node09.point, p09)
        expected_rect = RectHV(p01.x, p09.y, p08.x, 1)
        self.assertEqual(expected_rect, node09.rect)
        self.assertFalse(node09.split)
        
        # p10
        tree.insert(p10)
        # self.assertEqual(node07.rt.point, p10)
        node10 = node07.rt
        self.assertEqual(node10.point, p10)
        expected_rect = RectHV(p07.x, p10.y, 1, p02.y)
        self.assertEqual(expected_rect, node10.rect)
        self.assertFalse(node10.split)
        
    def test_016_range_empty_tree(self):
        query_rect = self.kd_tree.UNIT_SQUARE
        points = self.kd_tree.range(query_rect)
        self.assertEqual(points, set())
        
    def test_017_range_type_error(self):
        query_rect = Point2D(.3, .4)
        with self.assertRaises(TypeError):
            self.kd_tree.range(query_rect)
        
    def test_018_range_many_points(self):
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
        
        query_rect = tree.UNIT_SQUARE
        points = tree.range(query_rect)
        expected_points = {
            p01,
            p02,
            p03,
            p04,
            p05,
            p06,
            p07,
            p08,
            p09,
            p10,
        }
        self.assertEqual(expected_points, points)

        # p01
        query_rect = tree.root.rect
        points = tree.range(query_rect)
        expected_points = {
            p01,
            p02,
            p07,
            p08,
            p09,
            p10,
        }
        self.assertEqual(expected_points, points)
        
        # p02
        query_rect = tree.root.rt.rect
        points = tree.range(query_rect)
        expected_points = {
            p01,
            p02,
            p08,
            p09,
        }
        self.assertEqual(expected_points, points)
        
        # p03
        query_rect = tree.root.lb.rect
        points = tree.range(query_rect)
        expected_points = {
            p03,
            p06,
        }
        self.assertEqual(expected_points, points)
        
        # p04
        query_rect = tree.root.lb.lb.rect
        points = tree.range(query_rect)
        expected_points = {
            p01,
            p03,
            p04,
        }
        self.assertEqual(expected_points, points)

    def test_020_nearest_empty_tree(self):
        p = Point2D(.2, .3)
        self.assertIsNone(self.kd_tree.nearest(p))
        
    def test_021_nearest_type_error(self):
        p = (.2, .3)
        with self.assertRaises(TypeError):
            self.kd_tree.nearest(p)
    
    def test_022_nearest_to_itself(self):
        p01 = Point2D(.4, .3)
        p02 = Point2D(.7, .1)
        p03 = Point2D(.2, .5)
        self.kd_tree.insert(p01)
        self.kd_tree.insert(p02)
        self.kd_tree.insert(p03)
        
        nearest = self.kd_tree.nearest(p01)
        self.assertEqual(nearest, p01)
        
        nearest = self.kd_tree.nearest(p02)
        self.assertEqual(nearest, p02)
        
        nearest = self.kd_tree.nearest(p03)
        self.assertEqual(nearest, p03)
        
    def test_023_nearest(self):
        p01 = Point2D(.4, .3)
        p02 = Point2D(.7, .1)
        p03 = Point2D(.2, .5)
        self.kd_tree.insert(p01)
        self.kd_tree.insert(p02)
        self.kd_tree.insert(p03)
        
        query_point = Point2D(.5, .5)
        nearest = self.kd_tree.nearest(query_point)
        self.assertEqual(nearest, p01)
        
        query_point = Point2D(.9, .2)
        nearest = self.kd_tree.nearest(query_point)
        self.assertEqual(nearest, p02)
        
        query_point = Point2D(.1, .3)
        nearest = self.kd_tree.nearest(query_point)
        self.assertEqual(nearest, p03)
        