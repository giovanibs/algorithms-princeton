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
    """
    def __init__(self):
        self.root = None
    
    def search(self, k):
        node = self.root
        
        while node is not None:
            if k < node.key:
                node = node.left
            elif k > node.key:
                node = node.right
            else:
                return node.value
        
        return None
    
    def put(self, k, v):
        self.root = self._put(self.root, k, v)
    
    def _put(self, node, k, v):
        
        if node is None:
            return self._Node(k, v)
        
        if k < node.key:                        # insert to the left
            node.left = self._put(node.left, k, v)
        elif k > node.key:                      # insert to the right
            node.right = self._put(node.right, k, v)
        else:                                   # node.key == v
            node.value = v
            
        return node
            
    class _Node:
        def __init__(self, key, value, left=None, right=None):
            self.key    = key
            self.value  = value
            self.left   = left
            self.right  = right
            
        def __repr__(self) -> str:
            return str(self.key)

import unittest

class TestsBST(unittest.TestCase):
    def setUp(self) -> None:
        self.bst = BST()
    
    def test_search_existing_key(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')

        result = self.bst.search(2)
        self.assertEqual(result, 'banana')

    def test_search_nonexistent_key(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')

        result = self.bst.search(9)
        self.assertEqual(result, None)

    def test_search_empty_tree(self):

        result = self.bst.search(5)
        self.assertEqual(result, None)

    def test_put_new_key(self):
        self.bst.put(5, 'apple')

        result = self.bst.search(5)
        self.assertEqual(result, 'apple')

    def test_put_duplicate_key(self):
        self.bst.put(5, 'apple')
        self.bst.put(5, 'banana')

        result = self.bst.search(5)
        self.assertEqual(result, 'banana')

    def test_put_multiple_keys(self):
        self.bst.put(5, 'apple')
        self.bst.put(2, 'banana')
        self.bst.put(7, 'cherry')
        self.bst.put(4, 'date')

        result = self.bst.search(4)
        self.assertEqual(result, 'date')

    def test_put_and_search_large_tree(self):
        for i in range(1, 101):
            self.bst.put(i, str(i))

        result = self.bst.search(77)
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

if __name__ == '__main__':
    unittest.main()