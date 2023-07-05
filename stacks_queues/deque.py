class Deque:
    """
    Implementation of a double-ended queue using linked list
    """

    class _Node:
        def __init__(self, item, next=None, prev=None):
            self.item = item
            self.next = next
            self.prev = prev

        def __str__(self):
            return f"{self.item = }\n{self.prev = }\n{self.next = }"

    def __init__(self):
        self._first_node = None
        self._last_node = None
        self._len = 0

    def __len__(self):
        return self._len

    @property
    def is_empty(self):
        return self._len == 0

    def push_last(self, new_item):
        new_node = self._Node(new_item, prev=self._last_node)

        if self.is_empty:
            self._last_node = self._first_node = new_node  # prev and next are None
        else:
            self._last_node.next = new_node
            self._last_node = new_node

        self._len += 1

    def push_first(self, new_item):
        new_node = self._Node(new_item, next=self._first_node)

        if self.is_empty:
            self._first_node = self._last_node = new_node
        else:
            self._first_node.prev = new_node
            self._first_node = new_node

        self._len += 1

    def pop_first(self):
        if self.is_empty:
            raise IndexError("This deque is empty.")

        first_item = self._first_node.item
        self._first_node = self._first_node.next

        if self._first_node is not None:
            self._first_node.prev = None
        else:
            self._last_node = None

        self._len -= 1

        return first_item

    def pop_last(self):
        if self.is_empty:
            raise IndexError("This deque is empty.")

        last_item = self._last_node.item
        self._last_node = self._last_node.prev

        if self._last_node is not None:
            self._last_node.next = None
        else:
            self._first_node = None

        self._len -= 1

        return last_item