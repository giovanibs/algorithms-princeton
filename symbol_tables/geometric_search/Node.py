from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from Point2D import Point2D, TestsPoint2D
from RectHV import RectHV, TestsRectHV

@dataclass
class Node:
    point       : Point2D
    parent      : Node      = None
    container   : RectHV    = None
    rect        : RectHV    = None
    lb          : Node      = None     # the left/bottom subtree
    rt          : Node      = None     # the right/top subtree
    size        : int       = 1
    split       : bool      = True     # spliting vertically(True) or horizontally
    
    UNIT_SQUARE: ClassVar[RectHV] = RectHV(0, 0, 1, 1)
    
    def __post_init__(self):
        if not Node.UNIT_SQUARE.contains(self.point):
            raise ValueError(f"Point `{self.point}` is out of the unit square.")
        
        # --------- root ---------
        if self.parent is None:
            self.parent = self
            self.container = Node.UNIT_SQUARE
            self.rect = self.container.split_at(self.point, self.split)[1]
            return
        
        # set split based on parent's (except for root)
        self.split = not self.parent.split
        
        # --------- right/top node ---------
        if self.parent.rect.contains(self.point):
            self.container = self.parent.rect
        
        # --------- left/bot node ---------
        else:
            self.container = self.parent.container - self.parent.rect
            
        self.rect = self.container.split_at(self.point, self.split)[1]

# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
import unittest

class TestsNode(unittest.TestCase):
    """Tests for the `Node` class"""
    
    def test_000_init_point_not_in_unit_square(self):
        p01 = Point2D(3, .7)
        p02 = Point2D(.3, 7)
        p03 = Point2D(3, 7)
        
        with self.assertRaises(ValueError):
            Node(p01)
        with self.assertRaises(ValueError):
            Node(p02)
        with self.assertRaises(ValueError):
            Node(p03)
        
    def test_001_init_root(self):
        p = Point2D(.3, .7)
        root = Node(p)
        
        self.assertEqual(root.point, p)
        self.assertEqual(root.parent, root)
        self.assertTrue(root.split)
        expected_rect = RectHV(.3, 0, 1, 1)
        self.assertEqual(root.rect, expected_rect)
        
    def test_002_init_left_bot(self):
        p01 = Point2D(.4, .6)
        root = Node(p01)
        # RectHV(x_min=0.4, y_min=0.0, x_max=1.0, y_max=1.0)
        
        # level 01
        p02 = Point2D(.3, .3)
        node02 = Node(p02, root)
        root.lb = node02
        self.assertEqual(node02.point, p02)
        self.assertEqual(node02.parent, root)
        self.assertFalse(node02.split)
        expected_rect = RectHV(0, p02.y, p01.x, 1)
        self.assertEqual(node02.rect, expected_rect)
        
        # level 02
        p03 = Point2D(.2, .2)
        node03 = Node(p03, node02)
        node02.lb = node03
        self.assertEqual(node03.point, p03)
        self.assertEqual(node03.parent, node02)
        self.assertTrue(node03.split)
        expected_rect = RectHV(p03.x, 0, p01.x, p02.y)
        self.assertEqual(node03.rect, expected_rect)
        
    def test_003_init_right_top(self):
        p01 = Point2D(.4, .6)
        root = Node(p01)
        
        # level 01
        p02 = Point2D(.6, .4)
        node02 = Node(p02, root)
        root.rt = node02
        self.assertEqual(node02.point, p02)
        self.assertEqual(node02.parent, root)
        self.assertFalse(node02.split)
        expected_rect = RectHV(p01.x, p02.y, 1, 1)
        self.assertEqual(node02.rect, expected_rect)
        
        # level 02
        p03 = Point2D(.5, .7)
        node03 = Node(p03, node02)
        node02.rt = node03
        self.assertEqual(node03.point, p03)
        self.assertEqual(node03.parent, node02)
        self.assertTrue(node03.split)
        expected_rect = RectHV(p03.x, p02.y, 1, 1)
        self.assertEqual(node03.rect, expected_rect)
        