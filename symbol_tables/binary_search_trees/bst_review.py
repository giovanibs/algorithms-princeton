class BinarySearchTree:
    """
    A binary search tree (BST) is a binary tree where each node has a key
    (and an associated value) and satisfies the following restrictions:
        - the key in any node is larger than all the keys in the
        node's left subtree;
        - the key in any node is smaller than all the keys in the
        node's right subtree.
        
    We define a inner private class to define nodes in BST. Each node
    contains a key, a value, a left link, a right link, and a node count:
        - The left link points to a BST for items with smaller keys;
        - and the right link points to a BST for items with larger keys.
    """
    def __init__(self):
        self.root = None
        
    class _Node:
        def __init__(self, key, val):
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.size = 1
    
    @property
    def is_empty(self):
        return self.root is None
    
    def contains(self, k):
        """
        Does this BST contain the given key?
        """
        return self.get(k) is not None
        
    def get(self, k):
        if self.is_empty:
            return None
        
        return self._get(k, self.root)
    
    def _get(self, k, subtree):
        """
        A recursive algorithm to search for a key in a BST and return
        its value `val`.
        
        For a given key, `k`, and a given root of a subtree, `subtree`:
        
        1) If the subtree is empty, we have a search miss.
        
        2) If not, starting from the `subtree`, we compare `k`
        with the `subtree`'s key: 
            
            - If `k == subtree.key`, we have a search hit;
            
            - Otherwise, we search (recursively) in the appropriate
            subtree until `k` is found or we hit an empty subtree:
                
                - `k < subtree.key`: search in the left subtree
                
                - `k > subtree.key`: search in the right subtree
        """
        if subtree is None:
            return None
        
        if k == subtree.key:
            return subtree.val
        
        if k < subtree.key:
            return self._get(k, subtree.left)
        
        if k > subtree.key:
            return self._get(k, subtree.right)
        
import unittest

class TestsBST(unittest.TestCase):
    def setUp(self) -> None:
        self.bst = BinarySearchTree()

    def test_tree_is_empty(self):
        self.assertTrue(self.bst.is_empty)
        self.bst.root = self.bst._Node(1, 'ace')
        self.assertFalse(self.bst.is_empty)
    
    def test_ordering_property_empty_tree(self):
        self.assertTrue(self.assertOrderingProperty(self.bst.root))
    
    def test_ordering_property(self):
        # TREE IN SYMMETRIC ORDER
        root = self.bst.root = self.bst._Node(5, 'apple')
        root.left = self.bst._Node(2, "banana")
        root.right = self.bst._Node(7, "cherry")
        #     (5)
        #    /   \
        #  (2)    (7)
        self.assertTrue(self.assertOrderingProperty(root))
        
        # LEFT SUBTREE OUT OF ORDER
        root.left = self.bst._Node(6, "eggplant")
        with self.assertRaises(AssertionError):
            self.assertOrderingProperty(root)
    
        # RIGHT SUBTREE OUT OF ORDER
        root.left = None
        root.right = self.bst._Node(3, "fig")
        
        with self.assertRaises(AssertionError):
            self.assertOrderingProperty(root)
    
    def test_ordering_property_deeper_tree(self):
        # TREE IN SYMMETRIC ORDER
        root = self.bst.root = self.bst._Node(5, 'apple')
        root.left = self.bst._Node(2, "banana")
        root.left.right = self.bst._Node(3, "fig")
        root.right = self.bst._Node(7, "cherry")
        root.right.left = self.bst._Node(6, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)
        self.assertTrue(self.assertOrderingProperty(root))
        
        # A DEEPER LEFT NODE OUT OF ORDER
        root.right.left = self.bst._Node(8, "eggplant")
         #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (8)
        with self.assertRaises(AssertionError):
            self.assertOrderingProperty(root)
    
        # A DEEPER RIGHT NODE OUT OF ORDER
        root.right.left = self.bst._Node(6, "eggplant") # reset
        root.left.right = self.bst._Node(1, "fig")
         #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (1) (6)
        with self.assertRaises(AssertionError):
            self.assertOrderingProperty(root)
    
    def assertOrderingProperty(self, node):
        """
        Asserts that the binary tree is in symmetric order.
        """
        if node is None:
            return True

        left_subtree = node.left
        right_subtree = node.right

        if left_subtree is not None:
            self.assertLess(left_subtree.key, node.key)
            self.assertOrderingProperty(left_subtree)

        if right_subtree is not None:
            self.assertGreater(right_subtree.key, node.key)
            self.assertOrderingProperty(right_subtree)
            
        return True

    def test_get_existing_key(self):
        root = self.bst.root = self.bst._Node(5, 'apple')
        root.left = self.bst._Node(2, "banana")
        root.left.right = self.bst._Node(3, "fig")
        root.right = self.bst._Node(7, "cherry")
        root.right.left = self.bst._Node(6, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)
        self.assertOrderingProperty(self.bst.root)

        result = self.bst.get(6)
        self.assertEqual(result, "eggplant")

    def test_get_nonexistent_key(self):
        root = self.bst.root = self.bst._Node(5, 'apple')
        root.left = self.bst._Node(2, "banana")
        root.left.right = self.bst._Node(3, "fig")
        root.right = self.bst._Node(7, "cherry")
        root.right.left = self.bst._Node(6, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)

        result = self.bst.get(9)
        self.assertEqual(result, None)

    def test_get_empty_tree(self):
        result = self.bst.get(5)
        self.assertEqual(result, None)

    def test_does_not_contain(self):
        # EMPTY TREE
        self.assertFalse(self.bst.contains(1))
        
        # NOT EMPTY TREE
        root = self.bst.root = self.bst._Node(5, 'apple')
        root.left = self.bst._Node(2, "banana")
        root.right = self.bst._Node(7, "cherry")
        #     (5)
        #    /   \
        #  (2)    (7)
        self.assertFalse(self.bst.contains(1))
        
    def test_contains(self):
        root = self.bst.root = self.bst._Node(5, 'apple')
        root.left = self.bst._Node(2, "banana")
        root.right = self.bst._Node(7, "cherry")
        #     (5)
        #    /   \
        #  (2)    (7)
        self.assertTrue(self.bst.contains(5))
        self.assertTrue(self.bst.contains(2))
        self.assertTrue(self.bst.contains(7))
        