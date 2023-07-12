"""
Collections: insert and remove items. Which item to remove?

| Collection          |   Removed item          |
| ------------------- | ----------------------- |
| Stack               | Last added (LIFO)       |
| Queue               | First added (FIFO)      |
| Randomized queue    | Random                  |            
| Priority queue (PQ) | Largest or smallest     |

Priority queues have a limited capacity.

Priority queue (PQ) API:
    - init          : initialize a empty queue data structure
    - insert(key)   : insert a key into the PQ
    - remove_max    : remove and return the largest queue
    - is_empty      : True if the priority queue is empty
    - get_max       : return the largest key
"""
import os
import sys
package_path = os.path.abspath('..')
sys.path.append(package_path)

from stacks_queues.stacks import ArrayStack

class UnorderedArrayPQ(ArrayStack):
    """
    - Based on pushdown stacks.
    - `insert` is equivalent to `push` in the stack data structure
    - `remove_max`: find the max key, exchange it with the last one and then
    `pop` the item from the list
    
    """
    def __init__(self, capacity):
        super().__init__()
        self.pq = self._stack
        self.CAPACITY = capacity
    
    @property
    def is_empty(self):
        return len(self.pq) == 0

    @property
    def is_full(self):
        return len(self.pq) == self.CAPACITY
        
    def insert_key(self, key):
        """
        Inserts a key into the end of PQ -> equivalent to `push` in the stack
        - checks if the PQ is at full capacity:
                - if so, remove the minimum 
        """
        if self.is_full:
            self.remove_min()
        super().push(key)
        
    def remove_max(self):
        """
        Removes and returns the first occurrence of the largest key.
            1) Find max key
            2) Swap with last item (if different)
            3) Apply super().pop
        """
        if self.is_empty:
            return None
        
        max_key, max_key_index = self.get_max()
        
        if max_key != self.pq[-1]:
            self.pq[max_key_index], self.pq[-1] = \
                self.pq[-1], self.pq[max_key_index]
            
        return super().pop()
    
    def remove_min(self):
        """
        Removes the first occurrence of the SMALLEST key to make room for a new
        key:
            1) Find min key
            2) Swap with last item (if different)
            3) Apply super().pop
        """
        if self.is_empty:
            return None
        
        min_key, min_key_index = self.get_min()
        
        if min_key != self.pq[-1]:
            self.pq[min_key_index], self.pq[-1] = \
                self.pq[-1], self.pq[min_key_index]
            
        return super().pop()
    
    def get_max(self):
        """
        Return the largest key in PQ and its index.
        """
        if self.is_empty:
            return None
        
        max_key = max(self.pq)
        max_key_index = self.pq.index(max_key)
        return max_key, max_key_index
    
    def get_min(self):
        """
        Return the smallest key in PQ and its index.
        """
        if self.is_empty:
            return None
        
        min_key = min(self.pq)
        min_key_index = self.pq.index(min_key)
        return min_key, min_key_index

class OrderedArrayPQ(ArrayStack):
    """
    Very similar to the unordered array PQ. The difference consists in keeping
    the keys in order.
    """
    def __init__(self, capacity):
        super().__init__()
        self.pq = self._stack
        self.CAPACITY = capacity
    
    @property
    def is_empty(self):
        return len(self.pq) == 0

    @property
    def is_full(self):
        return len(self.pq) == self.CAPACITY
    
    def insert_key(self, key):
        if self.is_full:
            self.remove_min()
        super().push(key)
        self._stack.sort()      # keep queue sorted
    
    def remove_max(self):
        if self.is_empty:
            return None
        
        return self.pq.pop()
    
    def remove_min(self):
        if self.is_empty:
            return None
        
        return self._stack.pop(0)
    
    def get_max(self):
        if self.is_empty:
            return None
        
        return self._stack[-1], len(self._stack) - 1
   
    def get_min(self):
        if self.is_empty:
            return None
        
        return self._stack[0], 0
    
import unittest
from random import randint

class TestsUnorderedArrayPQ(unittest.TestCase):
    def setUp(self) -> None:
        self.PriorityQueue = UnorderedArrayPQ
    
    def test_is_empty_or_full(self):
        
        pq = self.PriorityQueue(3)        # -> []
        self.assertTrue(pq.is_empty)
        self.assertFalse(pq.is_full)
        
        pq.insert_key('a')              # -> ['a']
        self.assertFalse(pq.is_empty)
        self.assertFalse(pq.is_full)
        
        pq.insert_key('b')              # -> ['a', 'b']
        self.assertFalse(pq.is_empty)
        self.assertFalse(pq.is_full)
        
        pq.insert_key('c')              # -> ['a', 'b', 'c']
        self.assertFalse(pq.is_empty)
        self.assertTrue(pq.is_full)
        
        pq.remove_max()                 # -> ['a', 'b']
        self.assertFalse(pq.is_empty)
        self.assertFalse(pq.is_full)
    
        pq.remove_max()                 # -> ['a']
        self.assertFalse(pq.is_empty)
        self.assertFalse(pq.is_full)
    
        pq.remove_max()                 # -> []
        self.assertTrue(pq.is_empty)
        self.assertFalse(pq.is_full)
    
    def test_get_max(self):
        pq = self.PriorityQueue(3)
        pq.insert_key(1)
        pq.insert_key(2)
        pq.insert_key(0)
        result = pq.get_max()
        expected = (2, 1)
        self.assertEqual(result, expected)
        
        pq = self.PriorityQueue(3)
        result = pq.get_max()
        expected = None
        self.assertEqual(result, expected)
    
    def test_get_min(self):
        pq = self.PriorityQueue(3)
        pq.insert_key(1)
        pq.insert_key(2)
        pq.insert_key(0)
        result = pq.get_min()
        expected = (0, 2)
        self.assertEqual(result, expected)
        
        pq = self.PriorityQueue(3)
        result = pq.get_min()
        expected = None
        self.assertEqual(result, expected)
    
    def test_remove_max(self):
        pq = self.PriorityQueue(3)
        
        pq.insert_key(2)
        pq.insert_key(1)
        pq.insert_key(0)
        
        result = pq.remove_max()
        self.assertEqual(result, 2)
        self.assertEqual(pq._stack, [0, 1])
        
        result = pq.remove_max()
        self.assertEqual(result, 1)
        self.assertEqual(pq._stack, [0])
        
        result = pq.remove_max()
        self.assertEqual(result, 0)
        self.assertEqual(pq._stack, [])
        self.assertTrue(pq.is_empty)
        
        pq = self.PriorityQueue(3)
        result = pq.remove_max()
        expected = None
        self.assertEqual(result, expected)

    def test_remove_min(self):
        pq = self.PriorityQueue(3)
        
        pq.insert_key(0)
        pq.insert_key(2)
        pq.insert_key(1)    # [0, 2, 1]
        
        result = pq.remove_min()
        self.assertEqual(result, 0)
        self.assertEqual(pq._stack, [1, 2])
        
        result = pq.remove_min()
        self.assertEqual(result, 1)
        self.assertEqual(pq._stack, [2])
        
        result = pq.remove_min()
        self.assertEqual(result, 2)
        self.assertEqual(pq._stack, [])
        self.assertTrue(pq.is_empty)
        
        pq = self.PriorityQueue(3)
        result = pq.remove_min()
        expected = None
        self.assertEqual(result, expected)


class TestsOrderedArrayPQ(TestsUnorderedArrayPQ):
    def setUp(self) -> None:
        self.PriorityQueue = OrderedArrayPQ
    
    def test_is_empty_or_full(self):
        return super().test_is_empty_or_full()
        
    def test_get_max(self):
        pq = self.PriorityQueue(3)
        pq.insert_key(1)
        pq.insert_key(2)
        pq.insert_key(0)
        result = pq.get_max()
        expected = (2, 2)
        self.assertEqual(result, expected)
        
        pq = self.PriorityQueue(3)
        result = pq.get_max()
        expected = None
        self.assertEqual(result, expected)
        
        
    def test_get_min(self):
        pq = self.PriorityQueue(3)
        pq.insert_key(1)
        pq.insert_key(2)
        pq.insert_key(0)
        result = pq.get_min()
        expected = (0, 0)
        self.assertEqual(result, expected)
        
        pq.insert_key(3)
        result = pq.get_min()
        expected = (1, 0)
        self.assertEqual(result, expected)
        
        pq = self.PriorityQueue(3)
        result = pq.get_min()
        expected = None
        self.assertEqual(result, expected)
        
    def test_insert_key(self):
        pq = self.PriorityQueue(3)
        
        pq.insert_key(1)
        self.assertEqual(pq._stack, [1])
        
        pq.insert_key(2)
        self.assertEqual(pq._stack, [1, 2])
        
        pq.insert_key(0)
        self.assertEqual(pq._stack, [0, 1, 2])
        
        pq.insert_key(3)
        self.assertEqual(pq._stack, [1, 2, 3])
        
        pq.insert_key(2)
        self.assertEqual(pq._stack, [2, 2, 3])
        
    def test_random_insertions(self):
        capacity = 10
        pq = self.PriorityQueue(capacity)
        
        expected = []
        
        for _ in range(1_000):
            random_key = randint(0, 100)
            
            # expected
            if len(expected) == capacity:
                expected.pop(0)
            expected.append(random_key)
            expected.sort()
            
            # result
            pq.insert_key(random_key)
            
            # assert
            self.assertEqual(pq._stack, expected)
        
if __name__ == '__main__':
    unittest.main()