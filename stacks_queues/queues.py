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