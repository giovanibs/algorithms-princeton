class Queue:
    '''
    FIFO queue implementation using Python list
    '''
    
    def __init__(self):
        self._queue = []
        
    def len(self):
        return len(self._queue)
        
    def is_empty(self):
        return self.len() == 0
    
    def enqueue(self, item):
        self._queue.insert(0, item)
        
    def dequeue(self):
        if self.is_empty():
            return None
        return self._queue.pop()


class LinkedListQueue:
    '''
    FIFO queue implementation using a linked list data structure
    '''
    
    def __init__(self):
        self._first = None
        self._last  = None
        self._len = 0
        
    def len(self):
        return self._len
        
    def is_empty(self):
        return self.len() == 0
    
    def enqueue(self, item):
        if self.is_empty():
            self._first = self._Node(item)
            self._last  = self._first
        else:
            # former last will point to the new item
            self._last.next = self._Node(item)
            # the new item is the last
            self._last  = self._last.next
            
        self._len += 1
        
    def dequeue(self):
        if self.is_empty():
            return None
        
        # retrieve the first item
        first_out = self._first.item
        
        # update queue
        self._first = self._first.next
        self._len -= 1
        
        return first_out
    
    class _Node():
        def __init__(self, item):
            self.item = item
            self.next = None