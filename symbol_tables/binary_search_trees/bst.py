class BST:
    """
    Definition: a Binary Search Tree (BST) is a binary tree in symmetric order.

    ## A binary tree is either
    
        - empty
        - two disjoint binary trees (left and right)
        
    ## Symmetric order
    
    Each node has a key and every key is:

        - larger than ALL KEYS in its left subtree
        - smaller than ALL KEYS in its right subtree
    
    - E.G.: 
    
    |--------------|          .            |--------------|
    | keys smaller |  <-----  . ----->     | keys greater |
    | than `S`     |        ( S )          | than `S`     |
    |--------------|       /  .  \         |--------------|
                          /   .   \
                         /    .    \
                      (E)     .    (X)
                     /   \    . 
                    /     \   . 
                  (A)    (R)  . 
                  / \    / \  . 
                    (C) (H)   . 
    
    ## Searching BST
    
    Search for a `key`:
    1) Starting at the root, compare `key` and node's key:
        - if less, go left (keys to the left are < current key).
        - if larger, go right (keys to the right are > current key).
        - if equal, search hit.
        
    2) Repeat until key is found or hit a null link
    
    ## Insertion (put)
    
    Associate a `value` with a `key`:
    
    - Search for key, then two cases:
        - `key` in tree: update value
        - `key` NOT in tree: add new node
        
    ## BST Operations
    
    Minimum     : largest 
    Maximum     : smallest
    Floor       : largest key that is less than a given key
    Ceiling     : smallest key that is greater than a given key
    Size        : subtree counts, i.e. Node count
    Rank        : how many keys are less than a given key
    Delete      : lazy deletion, del the minimum, Hibbard deletion
    Ordered iteration :
    """

    def __init__(self):
        self.root = None

    class _Node:
        def __init__(self, key, value, left=None, right=None, parent=None):
            self.key = key
            self.val = value
            self.left = left
            self.right = right
            self.size = 1  # subtree size with this node as root
            self.parent = parent

        def __repr__(self) -> str:
            return str(self.key)

    @property
    def is_empty(self):
        """
        Returns `True` if the BST is empty, `False` otherwise.
        """
        return self._size(self.root) == 0

    def size(self, k=None):
        """
        Returns the size of _Node at `k`.
        If `k` is not given, returns size of the root, i.e. entire tree size.
        """
        if k is None:
            return self._size(self.root)

        node = self._get_node_at(k)
        return self._size(node)

    def _size(self, node):
        """
        Returns the size of the subtree rooted at given _Node `node`.
        """
        if node is None:
            return 0

        return node.size

    def _get_node_at(self, k):
        """
        Returns the _Node object at the given key `k`.

        If the BST does not contain `k`, returns `None`.
        """
        node = self.root

        while node is not None:
            if k < node.key:
                node = node.left
            elif k > node.key:
                node = node.right
            else:
                return node

        return None

    def get(self, k):
        """
        Returns the value associated with the given key `k`.

        If `k` is not in the BST, return None.
        """
        node = self._get_node_at(k)

        if node is None:
            return None
        else:
            return node.val

    def contains(self, k):
        """
        Returns `True` if given key `k` is in the BST.
        `False` otherwise.
        """
        return self.get(k) is not None

    def _get_parent_node(self, k):
        """
        Returns the parent _Node object of the _Node at `k`.
        """
        node = self._get_node_at(k)

        if node is None:
            raise KeyError("Given key is not in the tree.")

        return node.parent

    def put(self, k, v):
        """
        Inserts the specified key-value pair into the BST.
        If the BST contains `k`, overwrites the old value with `v`.
        """
        self.root = self._put(self.root, k, v)

    def _put(self, node, k, v, parent=None):
        if node is None:
            return self._Node(k, v, parent=parent)

        if k < node.key:
            # insert to the left
            node.left = self._put(node.left, k, v, parent=node)

        elif k > node.key:
            # insert to the right
            node.right = self._put(node.right, k, v, parent=node)

        else:  # just update node's value, no subtree resizing
            node.val = v

        # update node size based on its children
        node.size = 1 + self._size(node.left) + self._size(node.right)

        return node

    def get_max_key(self):
        max_node = self._get_max_node(self.root)

        if max_node == None:
            return None

        return max_node.key

    def _get_max_node(self, subtree):
        if subtree == None:
            return None

        if subtree.right == None:
            return subtree

        return self._get_max_node(subtree.right)

    def get_min_key(self):
        min_node = self._get_min_node(self.root)

        if min_node == None:
            return None

        return min_node.key

    def _get_min_node(self, subtree):
        if subtree == None:
            return None

        if subtree.left == None:
            return subtree

        return self._get_min_node(subtree.left)

    def get_floor(self, k):
        """
        Returns LARGEST key that is less than `k`.

        Steps:
        1) Starting from the root element of a subtree, compare `k` and the key:

            - if `k` is the root, then it is the floor

            - `k` < key at this root: must look in the left subtree for a key
            less than `k`.

            - `k` > key at root: this root could be the floor, but we must check
            for another potential floor in the right subtree. That is, we
            recursively call get_floor with right subtree as root to find a
            larger floor for `k`.
        """
        floor_node = self._get_floor(self.root, k)

        if floor_node == None:
            return None

        return floor_node.key

    def _get_floor(self, subtree, k):
        if subtree is None:
            return None

        # the root is the floor itself
        if k == subtree.key:
            return subtree

        if k < subtree.key:
            # floor must be in left subtree
            left_subtree = subtree.left
            return self._get_floor(left_subtree, k)

        # ELSE: floor must be in right subtree
        right_subtree = subtree.right
        larger_floor = self._get_floor(right_subtree, k)

        if larger_floor is None:
            # if no larger floor is found, than this floor is the one
            return subtree
        else:
            return larger_floor

    def get_ceiling(self, k):
        """
        Returns smallest entry that is greater than `k`.

        Steps:

        1) starting from the subtree `root` element
            - if `k` == `root`, then `root` is the ceiling.

            - if `k` > `root`, then the the ceiling is in the right subtree and
            the root node has nothing to do whatsaoever with it. So, we recurse
            with the right subtree as `root`. If, by any chance, the right
            subtree is `None`, the recursive call will return `None`.

            - if `k` < `root`, then `root` may be the ceiling or the ceiling is
            in the left subtree. then:
                    - recursively call get_ceiling. when the returned value is
                    None, we've found the ceiling
        """
        ceiling_node = self._get_ceiling(self.root, k)

        if ceiling_node == None:
            return None

        return ceiling_node.key

    def _get_ceiling(self, subtree, k):
        if subtree is None:
            return None

        if k == subtree.key:
            return subtree

        if k > subtree.key:
            # ceiling must be in right subtree
            right_subtree = subtree.right
            return self._get_ceiling(right_subtree, k)

        # ELSE: ceiling could be this subtree's root or be in its left subtree
        left_subtree = subtree.left

        # recurse to look for a smaller ceiling in the left subtree
        smaller_ceiling = self._get_ceiling(left_subtree, k)

        # check if smaller ceiling found
        if smaller_ceiling is None:
            return subtree
        else:
            return smaller_ceiling

    def get_rank(self, k):
        """
        In a binary search tree (BST), the "rank" of a node refers to its
        position within the BST when the nodes are arranged in ascending
        order. In other words, the rank of a node represents the number
        of nodes that are less than or equal to that node.
        """
        return self._rank(k, self.root)

    def _rank(self, k, subtree_root):
        """
        Returns the rank of the `_Node` object at given key `k`
        in a given subtree with root `subtree_root`:

        1) If the _Node for the given key is the same as the given
        `subtree_root`, the rank of `k` is the rank of the `subtree_root`,
        which is all elements to the left of it.

        2) If `k < subtree_node.key`, `k` is in the left subtree,
        i.e. `subtree_root = subtree_root.left`.

        3) If `k > subtree_node.key`, then `k` is in the right subtree.
        Here, the rank of `k` will be the sum of:
                - `1` (to count the key at the subtree_root).
                - keys in the left subtree (i.e. size of `subtree_root.left`).
                - rank of `k` in the right subtree (i.e. recursive call to `_rank`).
        """
        if subtree_root is None:
            return 0

        if k == subtree_root.key:
            return 1 + self._size(subtree_root.left)

        if k < subtree_root.key:
            return self._rank(k, subtree_root.left)

        if k > subtree_root.key:
            right_subtree = subtree_root.right
            return 1 + self._size(subtree_root.left) + self._rank(k, right_subtree)

    def del_max(self):
        """
        Removes the largest key from the BST (if not empty):

        1) finds the maximum node
        2) replace the link to that node by its left link
        """
        if self.is_empty:
            raise KeyError("BST is empty.")

        self.root = self._del_max(self.root)

    def _del_max(self, node):
        # if the given node is the maximum
        if node.right is None:
            # replace the node with its left link
            return node.left

        # recurse
        node.right = self._del_max(node.right)

        # update size: self + left + right
        node.size = 1 + self._size(node.left) + self._size(node.right)
        return node

    def del_min(self):
        """
        Removes the smallest key from the BST:
        1) finds the minimum node
        2) replace the link to that node by its right link
        """
        if self.is_empty:
            raise KeyError("BST is empty.")

        self.root = self._del_min(self.root)
        
    def _del_min(self, node):
        # if given node is the smallest
        if node.left is None:
            # replace the node with its right link
            return node.right
        
        # ELSE: recurse for next smaller node
        node.left = self._del_min(node.left)
        
         # update size: 1 (self) + size(left) + size(right)
        node.size = 1 + self._size(node.left) + self._size(node.right)
        return node

    def del_key(self, k):
        """
        Removes _Node at the given key `k`.
        """
        if not self.contains(k):
            raise KeyError(f"This BST does not contain `{k}`.")
        
        self.root = self._del_key(k, self.root)

    def _del_key(self, k, node):
        """
        Deleted node replacement:
        
        ### CASE 1: node has only 1 child
            Replace the deleted node with its child.
        
        ### CASE 2: node has both children -> apply Hibbard's:
            
            Delete a node by replacing it with its successor. The successor
            is the node with the smallest key in its right subtree.
            
            Steps:
            
            1) Save a link to the node to be deleted (aux_node)
            
            2) Set node to point to its successor _min(aux_node.right).
            
            3) Set the right link of node (which is supposed to point to
            the BST containing all the keys larger than node.key) to
            del_min(aux_node.right), the link to the BST containing all
            the keys that are larger than node.key after the deletion.

            4) Set the left link of node (which was None) to aux_node.left
            (all the keys that are less than both the deleted key and its
            successor).
        """
        if node is None:
            return None
        
        if k < node.key:
            node.left = self._del_key(k, node.left)
        
        elif k > node.key:
            node.right = self._del_key(k, node.right)
        
        else: # k == node.key
            
            ### CASE 1: node has 1 or no child:
            # 1.1
            if node.right is None:
                return node.left
            # 1.2
            if node.left is None:
                return node.right
            
            ### CASE 2
            
            # 1) save object reference
            deleted_node = node
            
            # 2) pick its sucessor. `node` now is the successor.
            node = self._get_min_node(deleted_node.right)
            
            # 3) Set the right link of the new node to the link to the BST
            # containing all the keys that are larger than node.key
            # after the deletion
            node.right = self._del_min(deleted_node.right)
            
            # 4) Set the left link of the NEW NODE (which was None)
            # to aux_node.left
            node.left = deleted_node.left
        
        # update size
        node.size = 1 + self._size(node.left) + self._size(node.right)
        return node

import unittest
from random import randint, randrange


class TestsBST(unittest.TestCase):
    def setUp(self) -> None:
        self.bst = BST()

    def test_size(self):
        # tree is empty
        self.assertTrue(self.bst.is_empty)
        self.assertEqual(self.bst.size(), 0)

        self.bst.put(50, 50)
        self.assertEqual(self.bst.size(50), 1)
        self.bst.put(70, 70)
        self.assertEqual(self.bst.size(50), 2)
        self.assertEqual(self.bst.size(70), 1)
        self.bst.put(30, 30)
        self.assertEqual(self.bst.size(50), 3)
        self.assertEqual(self.bst.size(70), 1)
        self.assertEqual(self.bst.size(30), 1)
        self.bst.put(10, 10)
        self.assertEqual(self.bst.size(50), 4)
        self.assertEqual(self.bst.size(70), 1)
        self.assertEqual(self.bst.size(30), 2)
        self.assertEqual(self.bst.size(10), 1)
        self.bst.put(80, 80)
        self.assertEqual(self.bst.size(50), 5)
        self.assertEqual(self.bst.size(70), 2)
        self.assertEqual(self.bst.size(30), 2)
        self.assertEqual(self.bst.size(10), 1)
        self.assertEqual(self.bst.size(80), 1)
        self.bst.put(40, 40)
        self.assertEqual(self.bst.size(50), 6)
        self.assertEqual(self.bst.size(70), 2)
        self.assertEqual(self.bst.size(30), 3)
        self.assertEqual(self.bst.size(10), 1)
        self.assertEqual(self.bst.size(80), 1)
        self.assertEqual(self.bst.size(40), 1)

    def test_get_existing_key(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")

        result = self.bst.get(2)
        self.assertEqual(result, "banana")
        self.assertOrderingProperty(self.bst.root)

    def test_get_nonexistent_key(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")

        result = self.bst.get(9)
        self.assertEqual(result, None)

    def test_get_empty_tree(self):
        result = self.bst.get(5)
        self.assertEqual(result, None)

    def test_contains(self):
        # empty tree contains no key
        self.assertFalse(self.bst.contains(1))

        self.bst.put(5, "apple")
        self.assertTrue(self.bst.contains(5))

        self.bst.put(2, "banana")
        self.assertTrue(self.bst.contains(2))

        self.bst.put(7, "cherry")
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

    def test_ordering_property(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")
        #     (5)
        #    /   \
        #  (2)    (7)
        # /   \
        #      (4)
        self.assertOrderingProperty(self.bst.root)

    def assertOrderingProperty(self, node):
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

    def test_get_max_key(self):
        # empty tree
        expected = None
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

        # 1 node
        self.bst.put(5, "apple")
        expected = 5
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

        self.bst.put(2, "banana")
        expected = 5
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

        self.bst.put(7, "cherry")
        expected = 7
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

        self.bst.put(4, "date")
        expected = 7
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

        self.bst.put(9, "eggplant")
        expected = 9
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

    def test_get_max_key_random_tests(self):
        random_keys = [randint(0, 1_000) for _ in range(100)]
        for key in random_keys:
            self.bst.put(key, str(key))

        expected = max(random_keys)
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)

    def test_get_min_key(self):
        # empty tree
        expected = None
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

        # 1 node
        self.bst.put(5, "apple")
        expected = 5
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

        self.bst.put(2, "banana")
        expected = 2
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

        self.bst.put(1, "cherry")
        expected = 1
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

        self.bst.put(4, "date")
        expected = 1
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

        self.bst.put(9, "eggplant")
        expected = 1
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

    def test_get_min_key_random_tests(self):
        random_keys = [randint(0, 1_000) for _ in range(100)]
        for key in random_keys:
            self.bst.put(key, str(key))

        expected = min(random_keys)
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)

    def test_get_floor(self):
        self.bst.put(50, 50)
        self.bst.put(70, 70)
        self.bst.put(30, 20)
        self.bst.put(10, 10)
        self.bst.put(80, 80)
        self.bst.put(40, 40)

        # floor == root
        self.assertEqual(self.bst.get_floor(50), 50)
        self.assertEqual(self.bst.get_floor(70), 70)
        self.assertEqual(self.bst.get_floor(30), 30)
        self.assertEqual(self.bst.get_floor(10), 10)
        self.assertEqual(self.bst.get_floor(80), 80)
        self.assertEqual(self.bst.get_floor(40), 40)

        # other
        self.assertEqual(self.bst.get_floor(1), None)
        self.assertEqual(self.bst.get_floor(5), None)
        self.assertEqual(self.bst.get_floor(15), 10)
        self.assertEqual(self.bst.get_floor(25), 10)
        self.assertEqual(self.bst.get_floor(35), 30)
        self.assertEqual(self.bst.get_floor(45), 40)
        self.assertEqual(self.bst.get_floor(69), 50)
        self.assertEqual(self.bst.get_floor(99), 80)
        self.assertEqual(self.bst.get_floor(88), 80)
        self.assertEqual(self.bst.get_floor(77), 70)

    def test_get_ceiling(self):
        self.bst.put(50, 50)
        self.bst.put(70, 70)
        self.bst.put(30, 20)
        self.bst.put(10, 10)
        self.bst.put(80, 80)
        self.bst.put(40, 40)

        # ceiling == root
        self.assertEqual(self.bst.get_ceiling(50), 50)
        self.assertEqual(self.bst.get_ceiling(70), 70)
        self.assertEqual(self.bst.get_ceiling(30), 30)
        self.assertEqual(self.bst.get_ceiling(10), 10)
        self.assertEqual(self.bst.get_ceiling(80), 80)
        self.assertEqual(self.bst.get_ceiling(40), 40)

        # other
        self.assertEqual(self.bst.get_ceiling(1), 10)
        self.assertEqual(self.bst.get_ceiling(5), 10)
        self.assertEqual(self.bst.get_ceiling(15), 30)
        self.assertEqual(self.bst.get_ceiling(25), 30)
        self.assertEqual(self.bst.get_ceiling(35), 40)
        self.assertEqual(self.bst.get_ceiling(45), 50)
        self.assertEqual(self.bst.get_ceiling(69), 70)
        self.assertEqual(self.bst.get_ceiling(99), None)
        self.assertEqual(self.bst.get_ceiling(88), None)
        self.assertEqual(self.bst.get_ceiling(77), 80)

    def test_get_floor_random(self):
        # random binary tree
        tree_size = 1_000
        max_key_range = 1_000
        random_keys = []
        for _ in range(tree_size):
            rand_key = randrange(0, max_key_range)
            random_keys.append(rand_key)
            self.bst.put(rand_key, str(rand_key))

        # pick random key (not necessarily in the bst)
        k = randrange(0, max_key_range)
        # save result
        result = self.bst.get_floor(k)

        # check for None
        min_key = min(random_keys)
        if result is None:
            self.assertLess(k, min_key)
            return

        if k < min_key:
            self.assertIsNone(result)
            return

        max_key = max(random_keys)
        if k >= max_key:
            self.assertEqual(result, max_key)
            return

        # expected is not None
        # keep unique keys and sort them to check
        random_keys = sorted(list(set(random_keys)))
        result_index = random_keys.index(result)

        # find lower and upper bounds for assertion
        lower_bound = random_keys[result_index]
        upper_index = min(result_index + 1, tree_size - 1)
        upper_bound = random_keys[upper_index]

        self.assertGreaterEqual(result, lower_bound)
        self.assertLess(result, upper_bound)

    def test_get_ceiling_random(self):
        # random binary tree
        tree_size = 1_000
        max_key_range = 1_000
        random_keys = []
        for _ in range(tree_size):
            rand_key = randrange(0, max_key_range)
            random_keys.append(rand_key)
            self.bst.put(rand_key, str(rand_key))

        # pick random key (not necessarily in the bst)
        k = randrange(0, max_key_range)
        # save result
        result = self.bst.get_ceiling(k)

        # check for None
        max_key = max(random_keys)
        if result is None:
            self.assertGreater(k, max_key)
            return

        if k > max_key:
            self.assertIsNone(result)
            return

        min_key = min(random_keys)
        if k <= min_key:
            self.assertEqual(result, min_key)
            return

        # expected is not None
        # keep unique keys and sort them to check
        random_keys = sorted(list(set(random_keys)))
        result_index = random_keys.index(result)

        # find lower and upper bounds for assertion
        lower_index = max(0, result_index - 1)
        upper_index = result_index

        lower_bound = random_keys[lower_index]
        upper_bound = random_keys[upper_index]

        self.assertGreater(result, lower_bound)
        self.assertLessEqual(result, upper_bound)

    def test_get_rank(self):
        self.bst.put(50, 50)
        self.assertEqual(self.bst.get_rank(50), 1)
        self.bst.put(70, 70)
        self.assertEqual(self.bst.get_rank(50), 1)
        self.assertEqual(self.bst.get_rank(70), 2)
        self.bst.put(30, 30)
        self.assertEqual(self.bst.get_rank(30), 1)
        self.assertEqual(self.bst.get_rank(50), 2)
        self.assertEqual(self.bst.get_rank(70), 3)
        self.bst.put(10, 10)
        self.assertEqual(self.bst.get_rank(10), 1)
        self.assertEqual(self.bst.get_rank(30), 2)
        self.assertEqual(self.bst.get_rank(50), 3)
        self.assertEqual(self.bst.get_rank(70), 4)
        self.bst.put(80, 80)
        self.assertEqual(self.bst.get_rank(10), 1)
        self.assertEqual(self.bst.get_rank(30), 2)
        self.assertEqual(self.bst.get_rank(50), 3)
        self.assertEqual(self.bst.get_rank(70), 4)
        self.assertEqual(self.bst.get_rank(80), 5)
        self.bst.put(40, 40)
        self.assertEqual(self.bst.get_rank(10), 1)
        self.assertEqual(self.bst.get_rank(30), 2)
        self.assertEqual(self.bst.get_rank(40), 3)
        self.assertEqual(self.bst.get_rank(50), 4)
        self.assertEqual(self.bst.get_rank(70), 5)
        self.assertEqual(self.bst.get_rank(80), 6)

    def test_get_parent_node(self):
        # empty tree
        with self.assertRaises(KeyError):
            self.bst._get_parent_node(5)

        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")
        #     (5)
        #    /   \
        #  (2)    (7)
        # /   \
        #      (4)

        # parent of the root is itself
        expected = None
        parent = self.bst._get_parent_node(5)
        self.assertEqual(expected, parent)

        expected = self.bst._get_node_at(5)
        parent = self.bst._get_parent_node(2)
        self.assertEqual(expected, parent)

        expected = self.bst._get_node_at(5)
        parent = self.bst._get_parent_node(7)
        self.assertEqual(expected, parent)

        expected = self.bst._get_node_at(2)
        parent = self.bst._get_parent_node(4)
        self.assertEqual(expected, parent)

        # key not in the BST
        with self.assertRaises(KeyError):
            self.bst._get_parent_node(1)

    def test_del_max(self):
        with self.assertRaises(KeyError):
            self.bst.del_max()

        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")
        #     (5)
        #    /   \
        #  (2)    (7)
        # /   \
        #      (4)

        # max == 7
        self.bst.del_max()
        self.assertFalse(self.bst.contains(7))
        self.assertOrderingProperty(self.bst.root)
        # check updated sizes
        expected_size = 3
        new_size = self.bst.size(5)
        self.assertEqual(expected_size, new_size)
        self.assertSizeConsistency(self.bst.root)

        # max == 5
        self.bst.del_max()
        self.assertFalse(self.bst.contains(5))
        self.assertOrderingProperty(self.bst.root)
        # check updated sizes
        expected_size = 2
        new_size = self.bst.size(2)
        self.assertEqual(expected_size, new_size)
        self.assertSizeConsistency(self.bst.root)

        # max == 4
        self.bst.del_max()
        self.assertFalse(self.bst.contains(4))
        self.assertOrderingProperty(self.bst.root)
        # check updated sizes
        expected_size = 1
        new_size = self.bst.size(2)
        self.assertEqual(expected_size, new_size)
        self.assertSizeConsistency(self.bst.root)

        # max == 2
        self.bst.del_max()
        self.assertFalse(self.bst.contains(2))
        self.assertOrderingProperty(self.bst.root)
        self.assertTrue(self.bst.is_empty)
        self.assertSizeConsistency(self.bst.root)

        # tree should be empty
        with self.assertRaises(KeyError):
            self.bst.del_max()
    
    def test_del_min(self):
        with self.assertRaises(KeyError):
            self.bst.del_min()

        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")
        #     (5)
        #    /   \
        #  (2)    (7)
        # /   \
        #      (4)

        # min == 2
        self.bst.del_min()
        self.assertFalse(self.bst.contains(2))
        self.assertOrderingProperty(self.bst.root)
        # check updated sizes
        expected_size = 3
        new_size = self.bst.size(5)
        self.assertEqual(expected_size, new_size)

        # min == 4
        self.bst.del_min()
        self.assertFalse(self.bst.contains(4))
        self.assertOrderingProperty(self.bst.root)
        # check updated sizes
        expected_size = 2
        new_size = self.bst.size(5)
        self.assertEqual(expected_size, new_size)

        # min == 5
        self.bst.del_min()
        self.assertFalse(self.bst.contains(5))
        self.assertOrderingProperty(self.bst.root)
        # check updated sizes
        expected_size = 1
        new_size = self.bst.size(7)
        self.assertEqual(expected_size, new_size)

        # min == 7
        self.bst.del_min()
        self.assertFalse(self.bst.contains(7))
        self.assertOrderingProperty(self.bst.root)
        self.assertTrue(self.bst.is_empty)

        # tree should be empty
        with self.assertRaises(KeyError):
            self.bst.del_min()
    
    def test_del_key(self):
        # empty tree
        with self.assertRaises(KeyError):
            self.bst.del_key(1)

        # not-empty tree
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(4, "date")
        self.bst.put(6, "elephant")
        #     (5)
        #    /   \
        #  (2)    (7)
        # /   \   /
        #    (4) (6)

        # del root
        self.bst.del_key(5)
        #     (6)
        #    /   \
        #  (2)    (7)
        # /   \   /
        #    (4)
        # sucessor == 6
        self.assertFalse(self.bst.contains(5))
        self.assertEqual(6, self.bst.root.key)
        self.assertEqual(7, self.bst.root.right.key)
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
        
        self.bst.put(1,1)
        #      (6)
        #     /   \
        #   (2)    (7)
        #   / \   /
        # (1) (4)
        # sucessor == 4
        self.bst.del_key(2)
        #      (6)
        #     /   \
        #   (4)    (7)
        #   / \   /
        # (1) 
        # sucessor == 4
        self.assertFalse(self.bst.contains(2))
        self.assertEqual(4, self.bst.root.left.key)
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
        
        self.bst.del_key(1)
        #      (6)
        #     /   \
        #   (4)    (7)
        #   / \   /
        # sucessor == None
        self.assertFalse(self.bst.contains(1))
        self.assertIsNone(self.bst.root.left.left)
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
        
        self.bst.del_key(7)
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
        
        self.bst.del_key(6)
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
        
        self.bst.del_key(4)
        self.assertOrderingProperty(self.bst.root)
        self.assertSizeConsistency(self.bst.root)
        self.assertTrue(self.bst.is_empty)

    def assertSizeConsistency(self, subtree):
        if subtree is None:
            return True
        
        subtree_size = self.bst._size(subtree)
        left_size = self.bst._size(subtree.left)
        right_size = self.bst._size(subtree.right)
        expected_size = 1 + left_size + right_size
        self.assertTrue( subtree_size == expected_size)
                
        self.assertSizeConsistency(subtree.left)
        self.assertSizeConsistency(subtree.right)
        
if __name__ == "__main__":
    unittest.main()
