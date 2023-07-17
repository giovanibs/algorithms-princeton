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
    
    def get_value(self, k):
        """
        Returns the value property of the `_Node` at given key `k`.
        """
        node = self._get_node_at(k)
        return None if node is None else node.value
    
    def _get_node_at(self, k):
        """
        Returns the _Node object at the given key `k`.
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
    
    def _get_parent_node(self, k):
        """
        Returns the parent _Node object of the _Node at `k`.
        """
        node = self._get_node_at(k)
        
        if node is None:
            raise KeyError("Given key is not in the tree.")
        
        return node.parent
    
    def put(self, k, v):
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
            
        else:   # just update node's value, no subtree resizing
            node.value = v
        
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
    
    def get_size(self, k):
        node = self._get_node_at(k)
        return self._size(node)
    
    def _size(self, node):
        if node is None:
            return 0
        
        return node.size
        
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
            return (
                1
                + self._size(subtree_root.left)
                + self._rank(k, right_subtree)
            )
    
    def del_max(self):
        """
        Removes the largest key from the BST.
        """
        raise NotImplementedError
        
    def del_key(self, k):
        """
        """
        raise NotImplementedError
    
    class _Node:
        def __init__(self, key, value, left=None, right=None, parent=None):
            self.key    = key
            self.value  = value
            self.left   = left
            self.right  = right
            self.size   = 1         # subtree size with this node as its root
            self.parent = parent
            
        def __repr__(self) -> str:
            return str(self.key)

import unittest
from random import randint, randrange

class TestsBST(unittest.TestCase):
    def setUp(self) -> None:
        self.bst = BST()
    
    def test_get_value_existing_key(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')

        result = self.bst.get_value(2)
        self.assertEqual(result, 'banana')

    def test_get_value_nonexistent_key(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')

        result = self.bst.get_value(9)
        self.assertEqual(result, None)

    def test_get_value_empty_tree(self):

        result = self.bst.get_value(5)
        self.assertEqual(result, None)

    def test_put_new_key(self):
        self.bst.put(5, 'apple')

        result = self.bst.get_value(5)
        self.assertEqual(result, 'apple')

    def test_put_duplicate_key(self):
        self.bst.put(5, 'apple')
        self.bst.put(5, 'banana')

        result = self.bst.get_value(5)
        self.assertEqual(result, 'banana')

    def test_put_multiple_keys(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')
        self.bst.put(4, 'date')

        result = self.bst.get_value(4)
        self.assertEqual(result, 'date')

    def test_put_and_get_value_large_tree(self):
        for i in range(1, 101):
            self.bst.put(i, str(i))

        result = self.bst.get_value(77)
        self.assertEqual(result, '77')
        self.assertOrderingProperty(self.bst.root)
        
    def test_ordering_property(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')
        self.bst.put(4, 'date')
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
        self.bst.put(5, 'apple')
        expected = 5
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)
        
        self.bst.put(2, 'banana')
        expected = 5
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)
        
        self.bst.put(7, 'cherry')
        expected = 7
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)
        
        self.bst.put(4, 'date')
        expected = 7
        result = self.bst.get_max_key()
        self.assertEqual(expected, result)
        
        self.bst.put(9, 'eggplant')
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
        self.bst.put(5, 'apple')
        expected = 5
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)
        
        self.bst.put(2, 'banana')
        expected = 2
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)
        
        self.bst.put(1, 'cherry')
        expected = 1
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)
        
        self.bst.put(4, 'date')
        expected = 1
        result = self.bst.get_min_key()
        self.assertEqual(expected, result)
        
        self.bst.put(9, 'eggplant')
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
        upper_index = min(result_index + 1, tree_size-1)
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
        lower_index = max(0, result_index-1)
        upper_index = result_index
        
        lower_bound = random_keys[lower_index]
        upper_bound = random_keys[upper_index]

        self.assertGreater(result, lower_bound)
        self.assertLessEqual(result, upper_bound)
        
    def test_get_size(self):
        self.bst.put(50, 50)
        self.assertEqual(self.bst.get_size(50), 1)
        self.bst.put(70, 70)
        self.assertEqual(self.bst.get_size(50), 2)
        self.assertEqual(self.bst.get_size(70), 1)
        self.bst.put(30, 30)
        self.assertEqual(self.bst.get_size(50), 3)
        self.assertEqual(self.bst.get_size(70), 1)
        self.assertEqual(self.bst.get_size(30), 1)
        self.bst.put(10, 10)
        self.assertEqual(self.bst.get_size(50), 4)
        self.assertEqual(self.bst.get_size(70), 1)
        self.assertEqual(self.bst.get_size(30), 2)
        self.assertEqual(self.bst.get_size(10), 1)
        self.bst.put(80, 80)
        self.assertEqual(self.bst.get_size(50), 5)
        self.assertEqual(self.bst.get_size(70), 2)
        self.assertEqual(self.bst.get_size(30), 2)
        self.assertEqual(self.bst.get_size(10), 1)
        self.assertEqual(self.bst.get_size(80), 1)
        self.bst.put(40, 40)
        self.assertEqual(self.bst.get_size(50), 6)
        self.assertEqual(self.bst.get_size(70), 2)
        self.assertEqual(self.bst.get_size(30), 3)
        self.assertEqual(self.bst.get_size(10), 1)
        self.assertEqual(self.bst.get_size(80), 1)
        self.assertEqual(self.bst.get_size(40), 1)
        
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
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')
        self.bst.put(4, 'date')
        #     (5)
        #    /   \
        #  (2)    (7)
        # /   \
        #      (4)
        
        # parent of the root is itself
        parent = self.bst._get_parent_node(5)
        expected = None
        self.assertEqual(parent, expected)
          
        parent = self.bst._get_parent_node(2)
        expected = self.bst._get_node_at(5)
        self.assertEqual(parent, expected)
          
        parent = self.bst._get_parent_node(7)
        expected = self.bst._get_node_at(5)
        self.assertEqual(parent, expected)
          
        parent = self.bst._get_parent_node(4)
        expected = self.bst._get_node_at(2)
        self.assertEqual(parent, expected)
        
        with self.assertRaises(KeyError):
            self.bst._get_parent_node(1)
            
if __name__ == '__main__':
    unittest.main()