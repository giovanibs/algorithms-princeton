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

from ..stacks_queues.queues import LinkedListQueue

class UnorderedLinkedListPQ(LinkedListQueue):
    """
    Inherits from LinkedListQueue since it already implements `first` and
    `last` nodes.
    """
    def __init__(self, capacity):
        super().__init__()
        self._min = None
        self._max = None
        self.CAPACITY = capacity
    
    @property
    def is_empty(self):
        return self._len == 0

    @property
    def is_full(self):
        return self._len == self.CAPACITY
        
    def insert_key(self, key):
        """
        Inserts a new Node with value `key` into the PQ. It is equivalent to
        `enqueue` in the LinkedListQueue.
        
        - if the PQ is at full capacity, call `remove_min` and then enqueue the
        new Node
        """
        if not self.is_full:
            super().enqueue(key)
        
    def remove_max(self):
        """
        Removes and returns the first occurrence of the largest key.
            1) Find max Node
            2) Swap with last Node (if different)
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
            1) find smallest Node
            2) swap with the last Node (if different)
            3) Pop Node (= dequeue)
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
        
        current = self._first
        max_node = current

        while current.next is not None:
            current = current.next
            if current.item > max_node.item:
                max_node = current
        
        return max_node
    
    def get_min(self):
        """
        Return the smallest key in PQ and its index.
        """
        if self.is_empty:
            return None
        
        current = self._first
        min_node = current

        while current.next is not None:
            current = current.next
            if current.item < min_node.item:
                min_node = current
        
        return min_node