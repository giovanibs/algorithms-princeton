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
    
    def min(self):
        """
        Returns the smallest key in the BST.
        """
        return self._min(self.root)
        
    def _min(self, subtree):
        """
        If the subtree is None, then there is no smallest key.
        
        If the left link of the subtree is null, the smallest
        key in this subtree is the key at the subtree root;
        
        Otherwise, the smallest key in the subtree is the
        smallest key in the subtree rooted at the left link.
        """
        if subtree is None:
            return None
        
        if subtree.left is None:
            return subtree.key
        else:
            return self._min(subtree.left)
        
    def max(self):
        """
        Returns the LARGEST key in the BST.
        """
        return self._max(self.root)
        
    def _max(self, subtree):
        """
        If the subtree is None, then there is no largest key.
        
        If the right link of the subtree is null, the largest
        key in this subtree is the key at the subtree root;
        
        Otherwise, the largest key in the subtree is the
        largest key in the subtree rooted at the right link.
        """
        if subtree is None:
            return None
        
        if subtree.right is None:
            return subtree.key
        else:
            return self._max(subtree.right)

    def floor(self, k):
        """
        Returns the LARGEST key in the BST that is equal to or
        smaller than the given key.
        """
        return self._floor(k, self.root)
        
    def _floor(self, k, subtree):
        """
        Compare `k` with key of the root of the `subtree`:
        
        (a) If subtree is empty, return None.
        
        (b) If `k == subtree.key`, then `k` is the floor.
        
        (c) If `k < subtree.key`, then the floor of key **MUST**
        be in the left subtree.
        
        (d) If `k > subtree.key`, then the floor of key **COULD**
        be in the right subtree. That is, is there a key smaller
        than or equal to `k` in the right subtree?
            - if yes, recursively find and return it;
            - if not, or if `k` is equal to the key at the root,
            then `subtree.key` is the floor of `k`.
        """
        # (a)
        if (subtree is None) or (k < self._min(subtree)):
            return None
        
        # (b)
        if k == subtree.key:
            return subtree.key
        
        # (c) MUST be in the left subtree
        if k < subtree.key:
            return self._floor(k, subtree.left)
        
        # (d) COULD be in the right subtree
        if k > subtree.key:
            floor = self._floor(k, subtree.right)
            
            # if not
            if floor is None:
                return subtree.key
            else:
                return floor
    
    def ceiling(self, k):
        """
        Returns the SMALLEST key in the BST that is greater than
        or equal to the given key `k`.
        """
        return self._ceiling(k, self.root)
        
    def _ceiling(self, k, subtree):
        """
        Compare `k` with key of the root of the `subtree`:
        
        (a) If subtree is empty, return None.
        
        (b) If `k == subtree.key`, then `k` is the ceiling.
        
        (c) If `k > subtree.key`, then the ceiling of `k` **MUST**
        be in the right subtree: recursively look for it.
        
        (d) If `k < subtree.key`, then the ceiling of key **COULD**
        be in the left subtree. That is, is there a key larger
        than or equal to `k` in the left subtree?
            - if yes, recursively find and return it;
            - if not, or if `k` is equal to the key at the root,
            then `subtree.key` is the ceiling of `k`.
        """
        # (a)
        if (subtree is None) or (k > self._max(subtree)):
            return None
        
        # (b)
        if k == subtree.key:
            return subtree.key
        
        # (c) MUST be in the right subtree. Find and return it.
        if k > subtree.key:
            return self._ceiling(k, subtree.right)
        
        # (d) COULD be in the left subtree
        if k < subtree.key:
            ceiling = self._ceiling(k, subtree.left)
            
            # if it is not in the left subtree
            if ceiling is None:
                return subtree.key
            else:
                return ceiling

    def select(self, r):
        """
        Returns the key of rank `r`, i.e. the key such that
        precisely `r` other keys in the BST are smaller.
        
        0 <= r < size(BST)
        """
        if r < 0 or r >= self.size():
            raise ValueError
        
        return self._select(r, self.root)
    
    def _select(self, r, subtree):
        """
        For the given rank `r` (0<= r < subtree size) and a
        subtree root `subtree`:
        
        (a) If `r == size(subtree.left)`, we return the key
        at the subtree root;
        
        (b) If `r < size(subtree.left)`, we look (recursively)
        for the key of rank `r` in the left subtree;
        
        (c) If `r > size(subtree.left)`, we look (recursively)
        for the key of rank (r - size(subtree.left) - 1)
        in the right subtree.
        """
        left_size = self._size(subtree.left)
        # (a)
        if r == left_size:
            return subtree.key
        # (b)
        elif r < left_size:
            return self._select(r, subtree.left)
        # (c)
        else: # r > left_size:
            new_r = r - left_size - 1
            return self._select(new_r, subtree.right)

    def rank(self, k):
        """
        Returns the rank (0 <= rank < BST size) of the given key `k`.
        In other words, the number of keys in the symbol table
        strictly less than `k`.
        """
        if not self.contains(k):
            raise KeyError(f"`{k}` not in the BST!")
        
        return self._rank(k, self.root)
        
    def _rank(self, k, subtree):
        """
        If `k == subtree.key`, we return the number of keys in the
        left subtree;
        
        if `k < subtree.key`, we recursively look for the rank of
        the key in the left subtree;
        
        if `k > subtree.key`, we return the sum of:
            + `1` (to count the key at the root)
            + left subtree size
            + (recursively) the rank of the key in the right subtree.
        """
        if k == subtree.key:
            return self._size(subtree.left)
        
        elif k < subtree.key:
            return self._rank(k, subtree.left)
        
        else:   # k > subtree.key
            return 1 + self._size(subtree.left) + self._rank(k, subtree.right)

    def del_min(self):
        """
        Removes the smallest key from the BST.
        """
        if self.is_empty:
            raise KeyError("BST is empty.")
        
        self.root = self._del_min(self.root)
        
    def _del_min(self, subtree):
        """
        We go left (recursively) until we find a node that
        that has a null left link and then replace the link
        to that node by its right link.
        """
        # if given node is the smallest
        if subtree.left is None:
            # replace the node with its right link
            return subtree.right
        else:
            # recursively look for next smaller node
            subtree.left = self._del_min(subtree.left)
        
        # update subtree size
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        return subtree
            
    def del_max(self):
        """
        Removes the LARGEST key from the BST.
        """
        if self.is_empty:
            raise KeyError("BST is empty.")
        
        self.root = self._del_max(self.root)
        
    def _del_max(self, subtree):
        """
        We go right (recursively) until we find a node that
        that has a null right link and then replace the link
        to that node by its left link.
        """
        # if given node is the largest
        if subtree.right is None:
            # replace the node with its left link
            return subtree.left
        else:
            # recursively look for next greater node in the right subtree
            subtree.right = self._del_max(subtree.right)
        
        # update subtree size
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        return subtree
            

#################
###   TESTS   ###
#################
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
    
    def test_min_empty_tree(self):
        self.assertIsNone(self.bst.min())
        
    def test_min(self):
        self.bst.put(5, "apple")
        self.assertEqual(5, self.bst.min())
        
        self.bst.put(2, "banana")
        self.assertEqual(2, self.bst.min())
        
        self.bst.put(7, "cherry")
        self.assertEqual(2, self.bst.min())
        
        self.bst.put(6, "date")
        self.assertEqual(2, self.bst.min())
        
        self.bst.put(1, "eggplant")
        self.assertEqual(1, self.bst.min())
        
    def test_max_empty_tree(self):
        self.assertIsNone(self.bst.max())
        
    def test_max(self):
        self.bst.put(5, "apple")
        self.assertEqual(5, self.bst.max())
        
        self.bst.put(2, "banana")
        self.assertEqual(5, self.bst.max())
        
        self.bst.put(7, "cherry")
        self.assertEqual(7, self.bst.max())
        
        self.bst.put(6, "date")
        self.assertEqual(7, self.bst.max())
        
        self.bst.put(9, "eggplant")
        self.assertEqual(9, self.bst.max())
    
    def test_floor_empty_tree(self):
        self.assertIsNone(self.bst.floor(1))
    
    def test_floor(self):
        self.bst.put(50, 50)
        self.bst.put(70, 70)
        self.bst.put(30, 20)
        self.bst.put(10, 10)
        self.bst.put(80, 80)
        self.bst.put(40, 40)

        # floor == root
        self.assertEqual(self.bst.floor(50), 50)
        self.assertEqual(self.bst.floor(70), 70)
        self.assertEqual(self.bst.floor(30), 30)
        self.assertEqual(self.bst.floor(10), 10)
        self.assertEqual(self.bst.floor(80), 80)
        self.assertEqual(self.bst.floor(40), 40)

        # other
        self.assertIsNone(self.bst.floor(1))
        self.assertIsNone(self.bst.floor(5))
        self.assertEqual(self.bst.floor(15), 10)
        self.assertEqual(self.bst.floor(25), 10)
        self.assertEqual(self.bst.floor(35), 30)
        self.assertEqual(self.bst.floor(45), 40)
        self.assertEqual(self.bst.floor(69), 50)
        self.assertEqual(self.bst.floor(99), 80)
        self.assertEqual(self.bst.floor(88), 80)
        self.assertEqual(self.bst.floor(77), 70)
    
    def test_ceiling_empty_tree(self):
        self.assertIsNone(self.bst.ceiling(1))
    
    def test_ceiling(self):
        self.bst.put(50, 50)
        self.bst.put(70, 70)
        self.bst.put(30, 20)
        self.bst.put(10, 10)
        self.bst.put(80, 80)
        self.bst.put(40, 40)

        # ceiling == root
        self.assertEqual(self.bst.ceiling(50), 50)
        self.assertEqual(self.bst.ceiling(70), 70)
        self.assertEqual(self.bst.ceiling(30), 30)
        self.assertEqual(self.bst.ceiling(10), 10)
        self.assertEqual(self.bst.ceiling(80), 80)
        self.assertEqual(self.bst.ceiling(40), 40)

        # other
        self.assertEqual(self.bst.ceiling(1), 10)
        self.assertEqual(self.bst.ceiling(5), 10)
        self.assertEqual(self.bst.ceiling(15), 30)
        self.assertEqual(self.bst.ceiling(25), 30)
        self.assertEqual(self.bst.ceiling(35), 40)
        self.assertEqual(self.bst.ceiling(45), 50)
        self.assertEqual(self.bst.ceiling(69), 70)
        self.assertEqual(self.bst.ceiling(99), None)
        self.assertEqual(self.bst.ceiling(88), None)
        self.assertEqual(self.bst.ceiling(77), 80)

    def test_select_empty_tree(self):
        with self.assertRaises(ValueError):
            self.bst.select(0)
        
    def test_select_out_of_range(self):
        self.bst.put(5, "apple")
        
        with self.assertRaises(ValueError):
            self.assertIsNone(self.bst.select(-1))
        
        with self.assertRaises(ValueError):
            self.assertIsNone(self.bst.select(1))
        
    def test_select(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(6, "date")
        self.bst.put(3, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)
        self.assertEqual(2, self.bst.select(0))
        self.assertEqual(3, self.bst.select(1))
        self.assertEqual(5, self.bst.select(2))
        self.assertEqual(6, self.bst.select(3))
        self.assertEqual(7, self.bst.select(4))
    
    def test_rank_empty_tree(self):
        with self.assertRaises(KeyError):
            self.bst.rank(1)
        
    def test_rank_key_not_in_BST(self):
        self.bst.put(5, "apple")
        
        with self.assertRaises(KeyError):
            self.bst.rank(2)
        
    def test_rank(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(6, "date")
        self.bst.put(3, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)
        self.assertEqual(0, self.bst.rank(2))
        self.assertEqual(1, self.bst.rank(3))
        self.assertEqual(2, self.bst.rank(5))
        self.assertEqual(3, self.bst.rank(6))
        self.assertEqual(4, self.bst.rank(7))

    def test_del_min_empty_tree(self):
        with self.assertRaises(KeyError):
            self.bst.del_min()
            
    def test_del_min(self):
        bst = self.bst
        
        bst.put(5, "apple")
        bst.del_min()
        self.assertTrue(bst.is_empty)
        
        bst.put(5, "apple")
        bst.put(2, "banana")
        bst.put(7, "cherry")
        bst.put(6, "date")
        bst.put(3, "eggplant")
        
        bst.del_min() # 2
        self.assertFalse(bst.contains(2))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertEqual(3, bst.root.left.key)
        
        bst.del_min() # 3
        self.assertFalse(bst.contains(3))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertIsNone(bst.root.left)
        
        bst.del_min() # 5
        self.assertFalse(bst.contains(5))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertEqual(7, bst.root.key)
        
        bst.del_min() # 6
        self.assertFalse(bst.contains(6))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertEqual(7, bst.root.key)
        
        bst.del_min() # 7
        self.assertTrue(bst.is_empty)        
        
    def test_del_max_empty_tree(self):
        with self.assertRaises(KeyError):
            self.bst.del_max()
            
    def test_del_max(self):
        bst = self.bst
        
        bst.put(5, "apple")
        bst.del_max()
        self.assertTrue(bst.is_empty)
        
        bst.put(5, "apple")
        bst.put(2, "banana")
        bst.put(7, "cherry")
        bst.put(6, "date")
        bst.put(3, "eggplant")
        
        bst.del_max() # 7
        self.assertFalse(bst.contains(7))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertEqual(6, bst.root.right.key)
        
        bst.del_max() # 6
        self.assertFalse(bst.contains(6))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertIsNone(bst.root.right)
        
        bst.del_max() # 5
        self.assertFalse(bst.contains(5))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertEqual(2, bst.root.key)
        
        bst.del_max() # 3
        self.assertFalse(bst.contains(3))
        self.assertOrderingProperty(bst.root)
        self.assertSizeConsistency(bst.root)
        self.assertEqual(2, bst.root.key)
        
        bst.del_max() # 2
        self.assertTrue(bst.is_empty)        
        