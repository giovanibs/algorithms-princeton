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
        
    def size(self):
        """
        Returns the size of the BST.
        """
        return self._size(self.root)
            
    def _size(self, subtree):
        """
        Returns the size of the BST rooted at `subtree`.
        """
        if subtree is None:
            return 0
        else:
            return subtree.size
 
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
    
    def put(self, k, v):
        self.root = self._put(k, v, self.root)
        
    def _put(self, k, v, subtree):
        """
        Searches for a null link (i.e. None) in the given subtree
        to insert the new key and value pair.
        
        (a) If the tree is empty, we return a new node containing
        the key and value;
        
        (b) If the search key `k` is equal to the key at the subtree
        root, update that Node's value with `v`.
        
        (c) If `k` is less than the key at the subtree root, we set
        the subtree left link to the result of inserting the key into
        the left subtree;
        
        (d) If `k` is greater than the key at the subtree root, we set
        the subtree right link to the result of inserting the key into
        the right subtree.
        """
        # (a)
        if subtree is None:
            return self._Node(k, v)
        
        # (b)
        if k == subtree.key:
            subtree.val = v
        
        # (c)
        elif k < subtree.key:
            subtree.left = self._put(k, v, subtree.left)
        
        # (d)
        else: # k > subtree.key
            subtree.right = self._put(k, v, subtree.right)

        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        return subtree
    
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
        
    def test_put_new_key(self):
        self.bst.put(5, "apple")

        result = self.bst.get(5)
        self.assertEqual(result, "apple")
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)

    def test_put_duplicate_key(self):
        self.bst.put(5, "apple")
        self.bst.put(5, "banana")

        result = self.bst.get(5)
        self.assertEqual(result, "banana")
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)

    def test_put_multiple_keys(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")

        result = self.bst.get(4)
        self.assertEqual(result, "date")
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)

    def test_put_and_get_large_tree(self):
        for i in range(1, 101):
            self.bst.put(i, str(i))

        result = self.bst.get(77)
        self.assertEqual(result, "77")
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
    
    def test_size_empty_tree(self):
        """
        Tests `size` method.
        """
        result = self.bst.size()
        expected = 0
        self.assertEqual(expected, result)
        
    def test_size_not_empty_tree(self):
        """
        Tests `size` method.
        """
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")
        result = self.bst.size()
        expected = 4
        self.assertEqual(expected, result)
        
    def test_subtree_size(self):
        """
        Tests the `_size` method.
        """
        ### INSERT (5)
        self.bst.put(5, "apple")
        # CHECK ROOT
        root = self.bst.root
        result = self.bst._size(root)
        expected = 1
        self.assertEqual(expected, result)
        
        ### INSERT (2)
        self.bst.put(2, "banana")
        
        # CHECK ROOT
        result = self.bst._size(root)
        expected = 2
        self.assertEqual(expected, result)
        
        # CHECK SUBTREE (2)
        subtree = root.left
        result = self.bst._size(subtree)
        expected = 1
        self.assertEqual(expected, result)
        
        ### INSERT (3)
        self.bst.put(3, "cherry")
        
        # CHECK ROOT
        result = self.bst._size(root)
        expected = 3
        self.assertEqual(expected, result)
        
        # CHECK SUBTREE (2)
        subtree = root.left
        result = self.bst._size(subtree)
        expected = 2
        self.assertEqual(expected, result)
        
        # CHECK SUBTREE (3)
        subtree = root.left.right
        result = self.bst._size(subtree)
        expected = 1
        self.assertEqual(expected, result)
        
        ### INSERT (7)
        self.bst.put(7, "daisy")
        
        # CHECK ROOT
        result = self.bst._size(root)
        expected = 4
        self.assertEqual(expected, result)
        
        # CHECK SUBTREE (2)
        subtree = root.left
        result = self.bst._size(subtree)
        expected = 2
        self.assertEqual(expected, result)
        
        # CHECK SUBTREE (3)
        subtree = root.left.right
        result = self.bst._size(subtree)
        expected = 1
        self.assertEqual(expected, result)
        
        # CHECK SUBTREE (7)
        subtree = root.right
        result = self.bst._size(subtree)
        expected = 1
        self.assertEqual(expected, result)
        
    def assertSizeConsistency(self, subtree):
        """
        Returns true if the subtree count, i.e. its size, is
        consistent in the data structure rooted at that node,
        raises assertion error otherwise.
        """
        if subtree is None:
            return True
        
        subtree_size = self.bst._size(subtree)
        left_size = self.bst._size(subtree.left)
        right_size = self.bst._size(subtree.right)
        expected_size = 1 + left_size + right_size
        self.assertTrue( subtree_size == expected_size)
                
        self.assertSizeConsistency(subtree.left)
        self.assertSizeConsistency(subtree.right)
        
        return True
        