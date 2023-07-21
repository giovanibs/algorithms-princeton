try:
    from ..binary_search_trees.bst2 import BinarySearchTree as BST
except:
    import os
    import sys

    package_path = os.path.abspath("../")
    sys.path.append(package_path)
    from binary_search_trees.bst2 import BinarySearchTree as BST
import graphviz
from random import random

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
    NOT_BST = "Not in symmetric order"
    NOT_23TREE = "Not a 2-3 tree"
    NOT_BALANCED = "Not balanced"
    NOT_SIZE_CONSISTENT = "Subtree counts not consistent"

    def __init__(self):
        super().__init__()

    class _Node:
        def __init__(self, key, val, size=1, color=None):
            self.assert_color(color)
            self.color = RedBlackBST.RED if color is None else color
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
    
        def __eq__(self, other):
            if isinstance(other, RedBlackBST._Node):
                return self.key == other.key \
                    and self.val == other.val \
                    and self.size == other.size \
                    and self.color == other.color
            else:
                raise TypeError
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

    def _rotate_left(self, subtree):
        """
        Orient a (temporarily) right-leaning red link to lean left.
        
        (a) save `red_right` node;
        
        (b) move nodes between `root` and `red_right`,
        i.e. `red_right.left`, to `subtree.right`;
        
        (c) set `red_right` left link to node at `root`
        
        (d) update colors
        
        (e) update sizes
        
        (f) return the new subtree root
        """
        right_node = subtree.right           # (a)
        subtree.right = right_node.left      # (b)
        right_node.left = subtree            # (c)
        # (d)
        right_node.color = subtree.color
        subtree.color = RedBlackBST.RED
        # (e)
        right_node.size = subtree.size
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        # (f)
        return right_node

    def _rotate_right(self, subtree):
        """
        Orient a left-leaning link to the left.
        
        (a) save `left_node` node;
        
        (b) move nodes between `left_node` and `subtree`,
        i.e. `left_node.right`, to `subtree.left`;
        
        (c) set `left_node`'s right link to node at `root`
        
        (d) update colors
        
        (e) update sizes
        
        (f) return the new subtree root
        
                        (subtree)
                       /         \
            (left_node)
        """
        left_node = subtree.left            # (a)
        subtree.left = left_node.right      # (b)
        left_node.right = subtree           # (c)
        # (d)
        left_node.color = subtree.color
        subtree.color = RedBlackBST.RED
        # (e)
        left_node.size = subtree.size
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        # (f)
        return left_node

    def _flip_colors(self, subtree):
        """
        Flip the colors of a node and its two children.
        `subtree` must have opposite color of its two children.
        """
        if subtree is None or subtree.left is None or subtree.right is None:
            return
        
        if (subtree.left.color != subtree.right.color) or \
            (subtree.color == subtree.left.color):
            return        
        
        subtree.color       = not subtree.color
        subtree.left.color  = not subtree.left.color
        subtree.right.color = not subtree.right.color
        
        return True

    def _move_red_left(self, subtree):
        """
        Assuming that `subtree` is red and both `subtree.left`
        and `subtree.left.left` are black, make `subtree.left`
        or one of its children red.
        """
        if subtree is None:
            return subtree
        
        if not subtree.color:
            return subtree
        
        if self.is_red(subtree.left) \
                and self.is_red(subtree.left.left):
            return subtree
        
        self._flip_colors(subtree)
        
        # right subtree is red now, gotta fix it
        if self.is_red(subtree.right.left):
            subtree.right = self._rotate_right(subtree.right)
            subtree = self._rotate_left(subtree)
            self._flip_colors(subtree)
        
        return subtree

    def _move_red_right(self, subtree):
        """
        Assuming that `subtree` is red and both `subtree.right`
        and `subtree.right.left` are black, make `subtree.right`
        or one of its children red.
        """
        raise NotImplementedError

    def restore_balance(self, subtree):
        # right-leaning red link
        if self.is_red(subtree.right) and not self.is_red(subtree.left):
            subtree = self._rotate_left(subtree)
        
        # two consecutives left-leaning red links
        if self.is_red(subtree.left) and self.is_red(subtree.left.left):
            subtree = self._rotate_right(subtree)
        
        # two red children
        if self.is_red(subtree.left) and self.is_red(subtree.right):
            self._flip_colors(subtree)
        
        # update sizes
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        
        return subtree
        
    # ------------------------------------------------
    #   Check integrity of red-black tree data structure.
    # ------------------------------------------------
    def assert_integrity(self):
        """
        Checks for:
        - symmetric order
        - 2-3 tree
        - balanced tree
        - subtree size consistency
        """
        assert self.is_BST,             RedBlackBST.NOT_BST
        assert self.is_23tree,          RedBlackBST.NOT_23TREE
        assert self.is_balanced,        RedBlackBST.NOT_BALANCED
        assert self.is_size_consistent, RedBlackBST.NOT_SIZE_CONSISTENT
        
        return True
        
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
        Checks whether the tree is a 2-3 tree:
        - No right-leaning red link;
        - AND no node is connected to two red links.
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
    
    @property
    def is_balanced(self):
        """
        A perfectly balanced red-black-tree is one whose
        null links are all the same distance from the root,
        as any 2-3-tree.
        """
        black = 0 # number of black links on path from root to min
        subtree = self.root
        
        # min path as reference for number of black links
        while subtree is not None:
            if not self.is_red(subtree):
                black += 1
            subtree = subtree.left
        
        # check starting from root
        return self._is_balanced(self.root, black)
    
    def _is_balanced(self, subtree, black):
        """
        - Every path from root to null link has same number
        of black links.
        - Never two red links in-a-row.
        """
        # hit a leaf, aka null link
        if subtree is None:
            return black == 0
        
        # decrease reference count
        if not self.is_red(subtree):
            black -= 1
        
        # recursively check left and right subtree
        return self._is_balanced(subtree.left, black) and \
            self._is_balanced(subtree.right, black)
        
    # ------------------------------------------------
    #   Overridden BST methods/properties.
    # ------------------------------------------------
    
    # ---------------------------------------
    # keeping these here until implementation
    # is finished bc of the inherited tests
    def put(self, k, v):
        return super().put(k, v)

    def _put(self, k, v, subtree):
        return super()._put(k, v, subtree)
    # ---------------------------------------
    
    def put2(self, k, v):
        self.root = self._put2(k, v, self.root)
        self.root.color = RedBlackBST.BLACK

    def _put2(self, k, v, subtree):
        # -------------------------------------------------
        # (1) puts new node just like a normal BST
        if subtree is None:
            return self._Node(k, v)
        
        if k == subtree.key:
            subtree.val = v
        
        elif k < subtree.key:
            subtree.left = self._put2(k, v, subtree.left)
        
        else: # k > subtree.key
            subtree.right = self._put2(k, v, subtree.right)
        
        # -------------------------------------------------
        # (2) fix-up color links if necessary
        return self.restore_balance(subtree)

    def del_min(self):
        """
        Removes the smallest key from the BST.
        """
        if self.is_empty:
            raise KeyError("BST is empty.")
        
        # if both children of root are black, set root to red to
        # move_red_left in the future
        if not self.is_red(self.root.left) \
                and not self.is_red(self.root.right):
            self.root.color = RedBlackBST.RED

        self.root = self._del_min(self.root);
        
        if not self.is_empty:
            # restore root BACK to BLACK
            self.root.color = RedBlackBST.BLACK;
        
    def _del_min(self, subtree):
        """
        """
        # if given node is the smallest
        if subtree.left is None:
            # replace the node with its right link
            return None
        
        if not self.is_red(subtree.left) and not self.is_red(subtree.left.left):
            subtree = self._move_red_left(subtree)
        
        subtree.left = self._del_min(subtree.left)
        
        return self.restore_balance(subtree)
    
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

    def display(self):
        """
        Display tree by rendering it with Graphviz.
        """
        dot = graphviz.Digraph()
        root = self.root
        if root is None:
            dot.node("", shape="point")
            dot.render('img/red_black_bst', view=True, format='png')
            return
        
        root_color = "red" if root.color else "black"
        dot.node(str(root.key), color=root_color)

        def add_nodes_edges(node):
            
            ### LEFT NODE
            # LINK: Node or null
            if node.left:
                left_node = str(node.left.key)
                shape = "ellipse"
                weight = "1"
            else:
                left_node = "None" + str(random())
                shape = "point"
                weight = "2"
            
            # EDGE: RED or BLACK
            if self.is_red(node.left):
                color = "red"
                penwidth = "2"
            else:
                color = "black"
                penwidth = "1"
                
            dot.node(left_node, shape=shape, color=color)
            dot.edge(
                str(node.key),  # node from
                left_node,      # node to
                color=color,
                penwidth=penwidth,
                weight=weight,
                )
            
            # recursively add more nodes
            if node.left:
                add_nodes_edges(node.left)
            
            ### RIGHT NODE
            # LINK: Node or null
            if node.right:
                right_node = str(node.right.key)
                shape = "ellipse"
                weight = "1"
            else:
                right_node = "None" + str(random())
                shape = "point"
                weight = "2"
            
            # EDGE: RED or BLACK
            if self.is_red(node.right):
                color = "red"
                penwidth = "2"
            else:
                color = "black"
                penwidth = "1"
                
            dot.node(right_node, shape=shape, color=color)
            dot.edge(
                str(node.key),  # node from
                right_node,      # node to
                color=color,
                penwidth=penwidth,
                weight=weight,
                )
            # recursively add more nodes
            if node.right:
                add_nodes_edges(node.right)
            
        add_nodes_edges(root)
        dot.render('img/red_black_bst', view=True, format='png')
    
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
        self.bst.root = root = self.bst._Node(1, 'a')
        root.left = self.bst._Node(2, 'b')
        self.assertFalse(self.bst.is_BST)
        
        # right subtree < root
        root.left = None
        root.right = self.bst._Node(0, 'c')          # not ok
        self.assertFalse(self.bst.is_BST)
        
        # deeper tree
        root.right = self.bst._Node(3, 'd')          # ok
        root.right.right = self.bst._Node(2, 'b')    # not ok
        self.assertFalse(self.bst.is_BST)
             
    def test_is_BST(self):
        # left subtree < root
        root = self.bst.root = self.bst._Node(1, 'a')
        root.left = self.bst._Node(0, 'b')
        self.assertTrue(self.bst.is_BST)
        
        # right subtree > root
        root.left = None
        root.right = self.bst._Node(2, 'c')
        self.assertTrue(self.bst.is_BST)
        
        # deeper tree
        root.right = self.bst._Node(3, 'b')
        root.right.right = self.bst._Node(4, 'c')
        root.right.left = self.bst._Node(2, 'd')
        self.assertTrue(self.bst.is_BST)

    def test_is_size_consistent_empty_tree(self):
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_is_size_consistent_false(self):
        root = self.bst.root = self.bst._Node(3, 'a', size=2)
        self.assertFalse(self.bst.is_size_consistent)
        
        root.left = self.bst._Node(2, 'b', size=2)     # nok
        root.size = 2                                  # ok
        self.assertFalse(self.bst.is_size_consistent)
        
        root.right = self.bst._Node(5, 'c', size=3)    # nok
        root.right.left = self.bst._Node(4, 'e', size=1) # ok
        root.size = 4
        self.assertFalse(self.bst.is_size_consistent)
        
    def test_is_size_consistent(self):
        root = self.bst.root = self.bst._Node(3, 'a')
        self.assertTrue(self.bst.is_size_consistent)
        
        root.left = self.bst._Node(2, 'b')
        root.size = 2
        self.assertTrue(self.bst.is_size_consistent)
        
        root.right = self.bst._Node(5, 'c')
        root.size = 3
        self.assertTrue(self.bst.is_size_consistent)
        
        root.left.left = self.bst._Node(1, 'd')
        root.left.size = 2
        root.size = 4
        self.assertTrue(self.bst.is_size_consistent)
        
        root.right.left = self.bst._Node(4, 'e')
        root.right.size = 2
        root.size = 5
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_is_red(self):
        # IS RED
        red_node = self.bst._Node(1, 'a', color=True)
        self.assertTrue(self.bst.is_red(red_node))
        
        # IS NOT RED
        black_node = self.bst._Node(1, 'a', color=False)
        self.assertFalse(self.bst.is_red(black_node))
        
        # DEFAULT COLOR IS RED!
        new_node = self.bst._Node(1, 'a')
        self.assertTrue(self.bst.is_red(new_node))
        
    def test_is_23tree_empty_tree(self):
        self.assertTrue(self.bst.is_23tree)
        
    def test_is_23tree_right_red_link(self):
        # right-leaning red link
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=True)
        self.assertFalse(self.bst.is_23tree)
        
        # deeper right-leaning red link
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        root.left = self.bst._Node(2, 'c', color=True)
        self.assertTrue(self.bst.is_23tree)
        root.left.color = False
        root.left.right = self.bst._Node(4, 'd', color=True)
        self.assertFalse(self.bst.is_23tree)
        
    def test_is_23tree_two_red_link(self):
        # node connected to two red links, aka 4-node
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        root.right.left = self.bst._Node(6, 'b', color=True)
        root.right.right = self.bst._Node(8, 'b', color=True)
        self.assertFalse(self.bst.is_23tree)
    
    def test_is_23tree(self):
        # no right-leaning red links
        # AND no node is connected to two red links
        self.bst.root = root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        
        root.left = self.bst._Node(3, 'c', color=True)
        self.assertTrue(self.bst.is_23tree)
        
        root.left.left = self.bst._Node(2, 'd', color=True)
        root.left.color = False
        root.left.right = self.bst._Node(4, 'e', color=False)
        self.assertTrue(self.bst.is_23tree)
        
        root.right.left = self.bst._Node(6, 'b', color=True)
        root.right.right = self.bst._Node(8, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
    
    def test_is_balanced_empty_tree(self):
        self.assertTrue(self.bst.is_balanced)
    
    def test_is_NOT_balanced(self):
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
        # not balanced, must rotate left
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        # fix
        root.right.left = root
        root = self.bst.root = root.right
        root.left.right = None
        root.left.color = True
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
    def test_is_NOT_balanced_4node(self):
        # not balanced bc 4-link-node
        root = self.bst.root = self.bst._Node(7, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        root.left = self.bst._Node(5, 'b', color=True)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        # 4th link coming up
        root.right = self.bst._Node(9, 'c', color=False)
        root.color = True
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        
    def test_is_balanced(self):
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        # rotate left
        root.right.left = root
        root = self.bst.root = root.right
        root.left.right = None
        root.left.color = True
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
        root.right = self.bst._Node(9, 'c', color=False)
        # not balanced bc 4-node
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        # split 4-node
        root.left.color = False
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
    
    def test_assert_integrity_empty_tree(self):
        self.bst.assert_integrity()
        
    def test_assert_integrity_NOT_BST(self):
        self.bst.root = self.bst._Node(1, 'a', color=False)
        self.bst.root.left = self.bst._Node(2, 'a', color=True)
        
        with self.assertRaisesRegex(AssertionError, RedBlackBST.NOT_BST):
            self.bst.assert_integrity()
        
    def test_assert_integrity_NOT_23TREE(self):
        self.bst.root = self.bst._Node(5, 'a', color=False)
        self.bst.root.right = self.bst._Node(7, 'b', color=True)
        
        with self.assertRaisesRegex(AssertionError, RedBlackBST.NOT_23TREE):
            self.bst.assert_integrity()
            
    def test_assert_integrity_NOT_BALANCED(self):
        self.bst.root = self.bst._Node(5, 'a', color=False)
        self.bst.root.right = self.bst._Node(7, 'b', color=False)

        with self.assertRaisesRegex(AssertionError, RedBlackBST.NOT_BALANCED):
            self.bst.assert_integrity()
            
    def test_assert_integrity_NOT_SIZE_CONSISTENT(self):
        self.bst.root = self.bst._Node(3, 'a', size=2)

        with self.assertRaisesRegex(AssertionError,
                                    RedBlackBST.NOT_SIZE_CONSISTENT):
            self.bst.assert_integrity()
            
    def test_rotate_left(self):
        previous_root = self.bst.root = self.bst._Node(5, 'a', size=2, color=False)
        previous_right = previous_root.right = self.bst._Node(7, 'c', size=1, color=True)
        #   (5)
        #  /  \\
        #     (7)
        self.assertFalse(self.bst.is_23tree)
        self.bst.root = self.bst._rotate_left(previous_root)
        #   (7)
        #  //  \
        # (5)
        self.assertEqual(self.bst.root, previous_right)
        self.assertEqual(self.bst.root.left.key, 5)
        self.assertTrue(previous_root.color)
        self.bst.assert_integrity()
    
    def test_rotate_left_more_nodes(self):
        # very HYPOTHETICAL case for testing purposes
        root = self.bst.root = self.bst._Node(5, 'a', size=4, color=False)
        root.left = self.bst._Node(4, 'b', size=1, color=False)
        root.right = self.bst._Node(7, 'c', size=2, color=True)
        root.right.left = self.bst._Node(6, 'd', size=1, color=False)
        #       (5)
        #      /   \\
        #    (4)   (7)
        #          /
        #       (6)
        self.assertFalse(self.bst.is_23tree)
        
        self.bst.root = self.bst._rotate_left(root)
        #        (7)
        #      //   \
        #    (5)
        #   /   \
        # (4)    (6)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_size_consistent)
        
    def test_rotate_right_simple(self):
        previous_root = self.bst.root = self.bst._Node(7, 'a', size=2, color=False)
        previous_left_node = self.bst.root.left = self.bst._Node(5, 'c', size=1, color=True)
        #   (7)
        #  //  \
        # (5)
        self.bst.root = self.bst._rotate_right(self.bst.root)
        #    (5)
        #   /  \\
        #      (7)
        self.assertEqual(self.bst.root, previous_left_node)
        self.assertEqual(self.bst.root.right, previous_root)
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_rotate_right_more_nodes(self):
        # highly HYPOTHETICAL case for testing purposes
        previous_root = self.bst.root = self.bst._Node(7, 'a', size=5, color=False)
        self.bst.root.right = self.bst._Node(8, 'e', size=1, color=False)
        previous_left_node = self.bst.root.left = self.bst._Node(5, 'b', size=3, color=True)
        previous_between = self.bst.root.left.right = self.bst._Node(6, 'c', size=1, color=False)
        previous_left_node.left = self.bst._Node(4, 'd', size=1, color=False)
        #      (7)
        #     //  \
        #    (5)   (8)
        #   /   \
        # (4)   (6)
        self.bst.root = self.bst._rotate_right(self.bst.root)
        #      (5)
        #      / \
        #   (4)   (7)
        #         / \
        #      (6)   (8)
        self.assertEqual(self.bst.root, previous_left_node)
        self.assertEqual(self.bst.root.right, previous_root)
        self.assertEqual(self.bst.root.right.left, previous_between)
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_flip_colors_empty_tree(self):
        self.assertFalse(self.bst._flip_colors(self.bst.root))
    
    def test_flip_colors_one_null_child(self):
        # left child is None
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertFalse(self.bst._flip_colors(self.bst.root))
        
        # right child is None
        root.right = None
        root.left = self.bst._Node(3, 'c', color=True)
        self.assertFalse(self.bst._flip_colors(self.bst.root))
        
    def test_flip_colors_same_color_parent_child(self):
        # all black
        self.bst.root = root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=False)
        root.left = self.bst._Node(3, 'c', color=False)
        self.assertFalse(self.bst._flip_colors(self.bst.root))
        # all red
        root.color = True
        root.right.color = True
        root.left.color = True
        self.assertFalse(self.bst._flip_colors(self.bst.root))

    def test_flip_colors(self):
        # black parent
        self.bst.root = root = self.bst._Node(5, 'a', color=False)
        left_child =root.left = self.bst._Node(3, 'c', color=True)
        right_child =root.right = self.bst._Node(7, 'b', color=True)
        
        self.assertTrue(self.bst._flip_colors(root))
        self.assertTrue(root.color)
        self.assertFalse(left_child.color)
        self.assertFalse(right_child.color)
        
        # flip again (red parent)
        self.assertTrue(self.bst._flip_colors(root))
        self.assertFalse(root.color)
        self.assertTrue(left_child.color)
        self.assertTrue(right_child.color)
        
    def test_put_empty_tree(self):
        bst = self.bst
        bst.put2(5, 5)
        self.assertEqual(bst.root.key, 5)
        
    def test_put_existing_key(self):
        bst = self.bst
        bst.put2(5, 5)
        bst.put2(5, 10)
        self.assertEqual(bst.root.key, 5)
        self.assertEqual(bst.root.val, 10)
        
    def test_put_left(self):
        bst = self.bst
        bst.put2(5, 5)
        bst.put2(3, 3)
        bst.assert_integrity()
        expected_node = bst._Node(3, 3, color=True, size=1)
        self.assertEqual(expected_node, bst.root.left)
        
    def test_put_right(self):
        bst = self.bst
        bst.put2(5, 5)
        bst.put2(7, 7)
        bst.assert_integrity()
        expected_root = bst._Node(7, 7, color=False, size=2)
        expected_left = bst._Node(5, 5, color=True, size=1)
        self.assertEqual(expected_root, bst.root)
        self.assertEqual(expected_left, bst.root.left)
        
    def test_put2(self):
        bst = self.bst
        bst.put2(5, "apple")
        bst.put2(2, "banana")
        bst.put2(7, "cherry")
        bst.put2(4, "date")
        bst.assert_integrity()
        
from time import sleep
if __name__ == "__main__":
    bst = RedBlackBST()
    bst.put2(5, "apple")
    bst.put2(2, "banana")
    bst.put2(4, "date")
    bst.put2(3, "hibiscus")
    bst.put2(1, "fig")
    bst.put2(8, "cherry")
    bst.put2(6, "eggplant")
    bst.put2(7, "guava")
    bst.display()
    sleep(3)
    bst.root.color = True
    bst._move_red_left(bst.root)
    bst.display()
    # bst.assert_integrity()
    # bst.del_min()
