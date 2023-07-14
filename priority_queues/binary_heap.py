from ordinal_list import OrdinalList

class BinaryHeap:
    """
        The binary heap is a data structure that can efficiently support the
    basic priority-queue operations.
    
        Uses a complete binary tree, which is one that's perfectly balanced,
    except possibly for the bottom level.
    
    ### Heap-ordered binary tree
    
        - Keys in nodes.
        - Largest key is at the root.
        - Parent's key no smaller then children's key.
    
    ### Array representation
    
        - Indices start at 1 (for convenience, `array[0]` is empty)
        - Take nodes in level order
        - No explicit links needed
    
    ### Properties
    
        - Largest key is the root of the binary tree, which is `array[1]`
        - Parent of node at the index `k` is at index `k//2`
        - Children of node at `k` are at `2k` and `2k+1`
    
                           (...)
                          /
                    (k//2)
                   /      \
              ( k )        (k+1)
             /     \
        (2*k)       (2*k+1)      
    
    ### Bottom-up reheapify: `swim`
    
        If there's a violation of the heap order, that is, a child's key becomes
        greater than its parent's key, apply `swim` method for the node:
        
        1) Exchange the key in child, `a[k]`, with its parent, `a[k//2]`.
        
        2) Repeat until heap order is restored.
    
    ### Top-down heapify: `sink`
    
        If by any chance the parent's key becomes smaller than any of it's
        children, apply `sink` method:
        
        1) Exchange key in parent with key in largest child (to make sure the
        new parent is also greater than the other child).
        
        2) Repeat until heap order is restored.
    
    ### Insertion in a heap
    
        1) Add new node at the end of the array and increment heap size.
        2) Swim up the new node to restore heap order.
    
    ### Delete the maximum in a heap
    
        1) Exchange item at root with the item at the end of the heap.
        2) Pop out the last node and save it to return and decrement heap size.
        3) Sink down the new root to restore heap order.
        4) Return the removed key.
    """
    
    def __init__(self, items=[]):
        # Indices start at 1: OrdinalList is 1-based index
        self._a = OrdinalList() 
        
        for item in items:
            self.insert(item)
        
    def __len__(self):
        return len(self._a)
    
    @property
    def is_empty(self):
        return len(self) == 0
        
    @property
    def a(self):
        return self._a
        
    def insert(self, item):
        """
        ### Insertion in a heap
        
        1) Add new node at the end of the array.
        2) Increment the size of the heap
        2) Swim it up to restore heap order.
        """
        self._a.append(item)
        # size of the heap follows changes in len(array)
        self._swim_up_item_at(len(self))
        
    def del_maximum(self):
        """
        ### Delete the maximum in a heap
        
        1) Exchange item at root with the item at the end of the heap.
        2) Pop out the last node, save it to return and decrement heap size.
        3) Sink down the swapped item at root to restore heap order.
        4) Return the removed key.
        """
        root = 1
        last_key = len(self)
        
        self._swap_items_at(root, last_key)         # (1)
        maximum = self._a.pop(last_key)             # (2)
        self._sink_down_item_at(root)               # (3)
        return maximum                              # (4)
    
    def _swim_up_item_at(self, k):
        """
        ### Bottom-up reheapify: `swim`
        
        If there's a violation of the heap order, that is, a child's key becomes
        greater than its parent's key, apply `swim` method for the node:
        
        1) Exchange the key in child, `a[k]`, with the key in its parent,
        `a[k//2]`.
        2) Repeat until heap order is restored.
        """
        self._validate_keys(k)
        
        while (k > 1) and (self._a[k] > self._a[k//2]):       # item at `k` is < its parent
            self._swap_items_at(k, k//2)                    # promote k and demote k//2
            k = k//2
            
    def _sink_down_item_at(self, k):
        """
        ### Top-down heapify: `sink`
        
        If by any chance the parent's key becomes smaller than any of it's
        children, apply `sink` method:
        
        1) Exchange key in parent with key in largest child (to make sure the
        new parent is greater than both children).
        2) Update `k`
        3) Repeat until until we reach a node with both children smaller, or
        the bottom.
        """
        self._validate_keys(k)
        while 2*k <= len(self): # while item at `k` has at least 1 child
            
            l = self._get_largest_child(k)
            if l is not None and self._a[k] < self._a[l]:
                self._swap_items_at(k, l)
                k = l
            else:
                break
                
    def _swap_items_at(self, key1, key2):
        """
        Swap item at key1 with item at key2
        """
        self._validate_keys(key1, key2)
        
        self._a[key1], self._a[key2] = \
                self._a[key2], self._a[key1]

    def _validate_keys(self, *keys):
        if min(keys) < 1 or max(keys) > len(self):
            raise IndexError("1 <= k <= N")
                
    def _get_largest_child(self, k):
        """
        Returns the INDEX of largest item between bh[k*2] and bh[k*2+1].
        """
        if 2*k > len(self):                 # item at `k` has NO child
            return None
        elif 2*k == len(self):              # item at `k` has only 1 child
            return 2*k
        elif self._a[2*k] >= self._a[2*k + 1]:      # item at 2*k is larger
            return 2*k
        else:                                       # item at 2*k+1 is larger
            return 2*k + 1


### TESTS ###
import unittest

class TestsBinaryHeap(unittest.TestCase):
    def setUp(self) -> None:
        self.BinaryHeap = BinaryHeap # extensible for HeapSort
        self.bh = self.BinaryHeap()
        
    def test_init_with_no_items(self):
        self.assertEqual(self.bh.a, [])
        
    def test_init_with_items(self):
        items = [1, 2, 3]
        self.bh = self.BinaryHeap(items)
        expected = [3, 1, 2]
        self.assertEqual(len(items), len(self.bh))
        self.assertEqual(expected, self.bh.a)
        
    def test_swim_up(self):
        
        self.bh._a = [2, 1, 3]
        # swim up root
        self.bh._swim_up_item_at(1)
        expected = [2, 1, 3]
        self.assertEqual(expected, self.bh.a)
        
        # swim up smaller item
        self.bh._swim_up_item_at(2)
        expected = [2, 1, 3]
        self.assertEqual(expected, self.bh.a)
        
        # swim up larger item
        self.bh._swim_up_item_at(3)
        expected = [3, 1, 2]
        self.assertEqual(expected, self.bh.a)
        
        # deeper node
        self.bh._a = [6, 5, 4, 3, 2, 1, 7]
        #     key = [0,    1, 2, 3, 4, 5, 6, 7]
        self.bh._swim_up_item_at(7)
        expected = [7, 5, 6, 3, 2, 1, 4]
        self.assertEqual(expected, self.bh.a)
        
        # IndexError
        self.bh._a = [3, 2, 1]
        with self.assertRaises(IndexError):
            self.bh._swim_up_item_at(0)
        with self.assertRaises(IndexError):
            self.bh._swim_up_item_at(4)
        
    def test_sink_down(self):
        self.bh._a = [2, 1, 3]
        
        # sink down smaller parent
        self.bh._sink_down_item_at(1)
        expected = [3, 1, 2]
        self.assertEqual(expected, self.bh.a)
        
        # sink down larger parent
        self.bh._sink_down_item_at(1)
        expected = [3, 1, 2]
        self.assertEqual(expected, self.bh.a)
        
        # sink down node with no child
        self.bh._sink_down_item_at(2)
        expected = [3, 1, 2]
        self.assertEqual(expected, self.bh.a)
        
        # deeper tree
        self.bh._a = [2, 5, 4, 3, 6, 1, 7]
        #     key = [0,     1, 2, 3, 4, 5, 6, 7]
        self.bh._sink_down_item_at(1)
        expected = [5, 6, 4, 3, 2, 1, 7]
        self.assertEqual(expected, self.bh.a)
        
        # IndexError
        self.bh._a = [3, 2, 1]
        with self.assertRaises(IndexError):
            self.bh._sink_down_item_at(0)
        with self.assertRaises(IndexError):
            self.bh._sink_down_item_at(4)
        
    def test_swap_items(self):
        self.bh._a = [5, 4, 3, 2, 1]
        #     key = [0,    1, 2, 3, 4, 5]
        
        self.bh._swap_items_at(1, 5)
        expected = [1, 4, 3, 2, 5]
        self.assertEqual(expected, self.bh.a)
        
        self.bh._swap_items_at(3, 5)
        expected = [1, 4, 5, 2, 3]
        self.assertEqual(expected, self.bh.a)
        
        self.bh._swap_items_at(1, 3)
        expected = [5, 4, 1, 2, 3]
        self.assertEqual(expected, self.bh.a)
        
        with self.assertRaises(IndexError):
            self.bh._swap_items_at(0, 5)
            
        with self.assertRaises(IndexError):
            self.bh._swap_items_at(1, 6)
            
    def test_insert(self):
        self.bh.insert("first")
        expected = ["first"]
        self.assertEqual(expected, self.bh.a)
        
        self.bh.insert("last")
        expected = ["last", "first"]
        self.assertEqual(expected, self.bh.a)
        
        self.bh.insert("middle")
        expected = ["middle", "first", "last"]
        self.assertEqual(expected, self.bh.a)
        
        self.bh.insert("wannabe last")
        expected = ["wannabe last", "middle", "last", "first"]
        self.assertEqual(expected, self.bh.a)
        
    def test_del_maximum(self):
        self.bh = self.BinaryHeap(['a', 'b', 'c', 'd', 'e'])
        # expected = ['e', 'd', 'b', 'a', 'c']
        maximum = self.bh.del_maximum()
        # expected = ['d', 'c', 'b', 'a']
        expected_maximum = 'e'
        self.assertEqual(expected_maximum, maximum)
        expected_a = ['d', 'c', 'b', 'a']
        self.assertEqual(expected_a, self.bh.a)
        
    def test_get_largest_child(self):
        self.bh = self.BinaryHeap([1, 2, 3, 4, 5])
        # expected = [5, 4, 3, 1, 2]
        # keys        1  2  3  4  5
        result = self.bh._get_largest_child(1)
        expected = 2
        self.assertEqual(expected, result)
        
        result = self.bh._get_largest_child(2)
        expected = 5
        self.assertEqual(expected, result)
        
        result = self.bh._get_largest_child(3)
        expected = None
        self.assertEqual(expected, result)
        