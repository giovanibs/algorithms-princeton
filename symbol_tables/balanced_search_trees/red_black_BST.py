try:
    from ..binary_search_trees.bst2 import BinarySearchTree as BST
except:
    import os
    import sys

    package_path = os.path.abspath("../")
    sys.path.append(package_path)
    from binary_search_trees.bst2 import BinarySearchTree as BST

class RedBlackBST(BST):
    """
    # Left-leaning red-black BST

    Implementation of a symbol table using a left-leaning
    red-black BST.

    The basic idea behind red-black BSTs is to encode 2-3 trees
    by starting with standard BSTs (which are made up of 2-nodes)
    and adding extra information to encode 3-nodes.

    We think of the links as being of two different types:
        - red links: bind together two 2-nodes to represent 3-nodes
        - black links: bind together the 2-3 tree.

    Specifically, we represent 3-nodes as two 2-nodes connected
    by a single red link that leans left. We refer to BSTs that
    represent 2-3 trees in this way as red-black BSTs.

    One advantage of using such a representation is that it allows us
    to use our get() code for standard BST search without modification.

    ### Color representation

    Since each node is pointed to by precisely one link (from its parent),
    we encode the color of links in nodes, by adding a boolean instance
    variable color to our Node data type, which is true if the link from
    the parent is red and false if it is black.

    By convention, null links are black.

    ### Rotations

    The implementation that we will consider might allow right-leaning
    red links or two red-links in a row during an operation, but it
    always corrects these conditions before completion, through
    judicious use of an operation called rotation that switches
    orientation of red links.

    First, suppose that we have a right-leaning red link that needs to be
    rotated to lean to the left. This operation is called a left rotation.

    Implementing a right rotation that converts a left-leaning red link
    to a right-leaning one amounts to the same code, with left and right
    interchanged.

    ### Flipping colors

    The implementation that we will consider might also allow a black
    parent to have two red children. The color flip operation flips the
    colors of the the two red children to black and the color of the
    black parent to red.
    """

    RED = True
    BLACK = False

    def __init__(self):
        super().__init__()

    class _Node:
        def __init__(self, key, val, size=1, color=None):
            self.assert_color(color)
            self.color = color or RedBlackBST.BLACK
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.size = size

        def assert_color(self, color):
            if color not in [None, RedBlackBST.BLACK, RedBlackBST.RED]:
                raise ValueError("Invalid color value.")

        def __repr__(self) -> str:
            return f"_Node(key={self.key}, val={self.val}, size={self.size}, color={'RED' if self.color else 'BLACK'})"
    # ------------------------------------------------
    #   New methods/properties.
    # ------------------------------------------------
    def is_red(self, node):
        """
        Is `node` RED?
        By default, null links are BLACK.
        """
        if node is None:
            return False

        return node.color

    def rotate_left(self, subtree):
        """
        Make a right-leaning link lean to the left.
        """
        raise NotImplementedError

    def rotate_right(self, subtree):
        """
        Make a left-leaning link lean to the right.
        """
        raise NotImplementedError

    def flip_colors(self, subtree):
        """
        Flip the colors of a node and its two children.
        `subtree` must have opposite color of its two children.
        """
        raise NotImplementedError

    def move_red_left(self, subtree):
        """
        Assuming that `subtree` is red and both `subtree.left`
        and `subtree.left.left` are black, make `subtree.left`
        or one of its children red.
        """
        raise NotImplementedError

    def move_red_right(self, subtree):
        """
        Assuming that `subtree` is red and both `subtree.right`
        and `subtree.right.left` are black, make `subtree.right`
        or one of its children red.
        """
        raise NotImplementedError

    def balance(self, subtree):
        """
        Restore red-black tree invariant.
        """
        raise NotImplementedError

    # ------------------------------------------------
    #   Check integrity of red-black tree data structure.
    # ------------------------------------------------
    def check(self):
        """
        Checks for:
        - symmetric order
        - subtree size consistency
        - 2-3 tree
        - balanced tree
        """
    
    @property
    def is_BST(self):
        """
        Does this binary tree satisfy symmetric order?
        Note: this test also ensures that data structure is a binary
        tree since order is strict.
        """
        return self._is_BST(self.root, None, None)
        
    def _is_BST(self, subtree, lo, hi):
        """
        Is the tree rooted at `subtree` a BST with all keys strictly
        between `lo` and `hi` (both inclusive)?
        If `lo` or `hi` is null, treat as empty constraint.
        """
        if subtree is None:
            return True
        
        this_key = subtree.key
        
        if (lo is not None) and (this_key <= lo):
            return False
        
        if (hi is not None) and (this_key >= hi):
            return False
        
        # key == 2
        return self._is_BST(subtree.left, lo=lo, hi=this_key) \
            and self._is_BST(subtree.right, lo=this_key, hi=hi)
    
    @property
    def is_size_consistent(self):
        """
        Returns true if the subtree count, i.e. its size, is
        consistent in the data structure rooted at that node,
        false otherwise.
        """
        return self._is_size_consistent(self.root)
    
    def _is_size_consistent(self, subtree):
        if subtree is None:
            return True
        
        subtree_size = self._size(subtree)

        expected = (
            1
            + self._size(subtree.left)
            + self._size(subtree.right)
        )
        if subtree_size != expected:
            return False
        
        return self._is_size_consistent(subtree.left) and \
            self._is_size_consistent(subtree.right)
    
    @property
    def is_23tree(self):
        """
        Checks whether the tree is a 2-2 tree:
        """
        return self._is_23tree(self.root)
    
    def _is_23tree(self, subtree):
        """
        - No right-leaning red link;
        - AND no node is connected to two red links.
        """
        if subtree is None:
            return True
        
        # no red right links
        if self.is_red(node=subtree.right):
            return False
        
        # no node is connected to two red links
        # PS.: exempt root because it should never be RED
        if (subtree is not self.root) and \
            self.is_red(subtree) and \
                self.is_red(subtree.left):
            return False
        
        return self._is_23tree(subtree.left) and self._is_23tree(subtree.right)
        
        
    # ------------------------------------------------
    #   Overridden BST methods/properties.
    # ------------------------------------------------
    def put(self, k, v):
        return super().put(k, v)
        # raise NotImplementedError

    def _put(self, k, v, subtree):
        return super()._put(k, v, subtree)
        # raise NotImplementedError

    def del_min(self):
        return super().del_min()
        # raise NotImplementedError

    def _del_min(self, subtree):
        return super()._del_min(subtree)
        # raise NotImplementedError

    def del_max(self):
        return super().del_max()
        # raise NotImplementedError

    def _del_max(self, subtree):
        return super()._del_max(subtree)
        # raise NotImplementedError

    def del_key(self, k):
        return super().del_key(k)
        # raise NotImplementedError

    def _del_key(self, k, subtree):
        return super()._del_key(k, subtree)
        # raise NotImplementedError

    # ------------------------------------------------
    #   Not overridden BST methods/properties
    # ------------------------------------------------
    @property
    def is_empty(self):
        return super().is_empty

    def size(self):
        return super().size()

    def _size(self, subtree):
        return super()._size(subtree)

    def get(self, k):
        return super().get(k)

    def _get(self, k, subtree):
        return super()._get(k, subtree)

    def min(self):
        return super().min()

    def _min(self, subtree):
        return super()._min(subtree)

    def max(self):
        return super().max()

    def _max(self, subtree):
        return super()._max(subtree)

    def floor(self, k):
        return super().floor(k)

    def _floor(self, k, subtree):
        return super()._floor(k, subtree)

    def ceiling(self, k):
        return super().ceiling(k)

    def _ceiling(self, k, subtree):
        return super()._ceiling(k, subtree)

    def select(self, r):
        return super().select(r)

    def _select(self, r, subtree):
        return super()._select(r, subtree)

    def rank(self, k):
        return super().rank(k)

    def _rank(self, k, subtree):
        return super()._rank(k, subtree)

    def keys(self, lo=None, hi=None):
        return super().keys(lo, hi)

    def _in_order(self, subtree, lo, hi, q):
        return super()._in_order(subtree, lo, hi, q)


# ------------------------------------------------
#   TESTS
# ------------------------------------------------
import unittest

try:
    from ..binary_search_trees.bst2 import TestsBST
except:
    import os
    import sys

    package_path = os.path.abspath("../")
    sys.path.append(package_path)
    from binary_search_trees.bst2 import TestsBST

class TestsRedBlackBST(TestsBST):
    def setUp(self):
        self.bst = RedBlackBST()
        
    def test_is_BST_empty_tree(self):
        self.assertTrue(self.bst.is_BST)
    
    def test_is_not_a_BST(self):
        # left subtree > root
        self.bst.root = self.bst._Node(1, 'a')
        self.bst.root.left = self.bst._Node(2, 'b')
        self.assertFalse(self.bst.is_BST)
        
        # right subtree < root
        self.bst.root = self.bst._Node(1, 'a')                # reset
        self.bst.root.right = self.bst._Node(0, 'c')          # not ok
        self.assertFalse(self.bst.is_BST)
        
        # deeper tree
        self.bst.root = self.bst._Node(1, 'a')                # reset
        self.bst.root.right = self.bst._Node(3, 'd')          # ok
        self.bst.root.right.right = self.bst._Node(2, 'b')    # not ok
        self.assertFalse(self.bst.is_BST)
             
    def test_is_BST(self):
        # left subtree < root
        self.bst.root = self.bst._Node(1, 'a')
        self.bst.root.left = self.bst._Node(0, 'b')
        self.assertTrue(self.bst.is_BST)
        
        # right subtree > root
        self.bst.root = self.bst._Node(1, 'a')                # reset
        self.bst.root.right = self.bst._Node(2, 'c')
        self.assertTrue(self.bst.is_BST)
        
        # deeper tree
        self.bst.root = self.bst._Node(1, 'a')                # reset
        self.bst.root.right = self.bst._Node(3, 'b')
        self.bst.root.right.right = self.bst._Node(4, 'c')
        self.bst.root.right.left = self.bst._Node(2, 'd')
        self.assertTrue(self.bst.is_BST)

    def test_is_size_consistent_empty_tree(self):
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_is_size_consistent_false(self):
        self.bst.root = self.bst._Node(3, 'a', size=2)
        self.assertFalse(self.bst.is_size_consistent)
        
        self.bst.root.left = self.bst._Node(2, 'b', size=2)     # nok
        self.bst.root.size = 2                                  # ok
        self.assertFalse(self.bst.is_size_consistent)
        
        self.bst.root.right = self.bst._Node(5, 'c', size=3)    # nok
        self.bst.root.right.left = self.bst._Node(4, 'e', size=1) # ok
        self.bst.root.size = 4
        self.assertFalse(self.bst.is_size_consistent)
        
    def test_is_size_consistent(self):
        self.bst.root = self.bst._Node(3, 'a')
        self.assertTrue(self.bst.is_size_consistent)
        
        self.bst.root.left = self.bst._Node(2, 'b')
        self.bst.root.size = 2
        self.assertTrue(self.bst.is_size_consistent)
        
        self.bst.root.right = self.bst._Node(5, 'c')
        self.bst.root.size = 3
        self.assertTrue(self.bst.is_size_consistent)
        
        self.bst.root.left.left = self.bst._Node(1, 'd')
        self.bst.root.left.size = 2
        self.bst.root.size = 4
        self.assertTrue(self.bst.is_size_consistent)
        
        self.bst.root.right.left = self.bst._Node(4, 'e')
        self.bst.root.right.size = 2
        self.bst.root.size = 5
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_is_red(self):
        # IS RED
        red_node = self.bst._Node(1, 'a', color=True)
        self.assertTrue(self.bst.is_red(red_node))
        # IS NOT RED
        black_node = self.bst._Node(1, 'a')
        self.assertFalse(self.bst.is_red(black_node))
        
    def test_is_23tree_empty_tree(self):
        self.assertTrue(self.bst.is_23tree)
        
    def test_is_not_23tree(self):
        # right-leaning red links
        self.bst.root = root = self.bst._Node(5, 'a')
        root.right = self.bst._Node(7, 'b', color=True)
        self.assertFalse(self.bst.is_23tree)
        
        # deeper right-leaning red link
        root.right = self.bst._Node(7, 'b') # reset color
        self.assertTrue(self.bst.is_23tree)
        root.left = self.bst._Node(2, 'c')
        root.left.right = self.bst._Node(4, 'd', color=True)
        
        # AND no node is connected to two red links
        root.left.right = self.bst._Node(4, 'd') # reset
        self.assertTrue(self.bst.is_23tree)
        root.right.left = self.bst._Node(6, 'b', color=True)
        root.right.right = self.bst._Node(8, 'b', color=True)
        self.assertFalse(self.bst.is_23tree)
    
    def test_is_23tree(self):
        # no right-leaning red links
        # AND no node is connected to two red links
        
        self.bst.root = root = self.bst._Node(5, 'a')
        self.assertTrue(self.bst.is_23tree)
        
        root.right = self.bst._Node(7, 'b')
        self.assertTrue(self.bst.is_23tree)
        
        root.left = self.bst._Node(3, 'c', color=True)
        self.assertTrue(self.bst.is_23tree)
        
        root.left = self.bst._Node(3, 'c')                    # reset
        root.left.left = self.bst._Node(2, 'd', color=True)
        root.left.right = self.bst._Node(4, 'e')
        self.assertTrue(self.bst.is_23tree)
        
        root.right.left = self.bst._Node(6, 'b', color=True)
        root.right.right = self.bst._Node(8, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        
if __name__ == "__main__":
    bst = RedBlackBST()
    bst.root = bst._Node(5, 'a')
    bst.root.right = bst._Node(7, 'b', color=True)
    
    print(f"{bst.root = }")
    print(f"{bst.root.left = }")
    print(f"{bst.root.right = }")
    
    print(bst.is_23tree)
