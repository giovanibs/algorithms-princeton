class LinkedListPQ:
    """
    Very basic implementation of a Priority Queue using a reverse-ordered queue.
    i.e. the largest `Node` will be kept at the head of the queue.
    `Node` objects added to the PQ will be inserted in order.
    
    API:
    - init          : initialize an empty queue data structure
    - insert_key    : insert a key into the PQ in the right order
    - remove_max    : remove and return the largest queue (i.e. the PQ's head)
    - is_empty      : True if the priority queue is empty
    - get_max       : return the largest key (i.e. the PQ's head)
    """
    def __init__(self):
        self._head = None
        self._len = 0
    
    @property
    def is_empty(self):
        return self._len == 0

    def insert_key(self, key):
        """
        Inserts a new Node with value `key` into the PQ, according to its
        priority.
        """
        
        if self.is_empty:
            self._head = self._Node(key)
            
        elif key >= self._head.item:
            self._head = self._Node(key, next=self._head)
            
        else: # find where the node belongs in the order
            current = self._head
            
            while (current.next is not None) and (key < current.next.item):
                current = current.next
                
            # found a node that is <= to the new node
            current.next = self._Node(key, next=current.next)
            
        self._len += 1
                
    def remove_max(self):
        """
        largest Node == queue head
        """
        largest = self._head.item
        self._head = self._head.next
        self._len -= 1
        return largest
    
    def get_max(self):
        """
        Return the largest key in PQ and its index.
        """
        if self.is_empty:
            return None
        
        return self._head.item
    
    class _Node:
        def __init__(self, item, next=None):
            self.item = item
            self.next = next
            
        def __eq__(self, other):
            return self.item == other.item
        
        def __lt__(self, other):
            return self.item < other.item

#   #   #   #   #   #   #   #
#           TESTS           #
#   #   #   #   #   #   #   #
import unittest
from random import shuffle, random

class TestsLinkedListPQ(unittest.TestCase):
    def setUp(self):
        self.pq = LinkedListPQ()
        
    def test_empty_pq(self):
        self.assertTrue(self.pq.is_empty)
        
        self.pq.insert_key('foo')
        self.assertFalse(self.pq.is_empty)
        
        self.pq.insert_key('bar')
        self.assertFalse(self.pq.is_empty)
        
        self.pq.remove_max()
        self.assertFalse(self.pq.is_empty)
        
        self.pq.remove_max()
        self.assertTrue(self.pq.is_empty)
        
    def test_get_max(self):
        items = [random() for _ in range(100)]
        expected = max(items)
        
        for item in items:
            self.pq.insert_key(item)
            
        result = self.pq.get_max()
        
        self.assertEqual(expected, result)
            
    def test_enqueue_dequeue_single_element(self):
        expected = 'a'
        self.pq.insert_key(expected)
        result = self.pq.remove_max()
        
        self.assertTrue(self.pq.is_empty)
        self.assertEqual(result, expected)
    
    def test_enqueue_dequeue_multiple_elements(self):
        n = 100
        
        for _ in range(1, n):
            shuffle(a:=list(range(n)))
            
            for key in a:
                self.pq.insert_key(key)
            
            dequeued = [self.pq.remove_max() for _ in a]
            expected = sorted(a, reverse=True)
            
            self.assertTrue(self.pq.is_empty)
            self.assertEqual(dequeued, expected)
            
if __name__ == "__main__":
    unittest.main()