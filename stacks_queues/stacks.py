class ArrayStack():
    def __init__(self):
        self._stack = []
        
    def is_empty(self):
        return len(self._stack) == 0
    
    def len(self):
        return len(self._stack)
    
    def push(self, item):
        self._stack.append(item)
    
    def pop(self):
        return self._stack.pop()
    
    
class LinkedListStack():
    def __init__(self):
        self._first = None
        self._len   = 0
        
    def is_empty(self):
        return self._first == None
    
    def len(self):
        return self._len
    
    def push(self, item):
        self._first = self._Node(item, self._first)
        self._len   += 1
    
    def pop(self):
        if self._len == 0:
            raise IndexError    
            
        popped_item = self._first.item
        self._first = self._first.next
        self._len   -= 1
        return popped_item
        
        
    class _Node:
        def __init__(self, item, next = None):
            self.item = item
            self.next = next