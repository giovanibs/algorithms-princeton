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


import unittest


class DequeTests(unittest.TestCase):
    def setUp(self):
        self.deque = Deque()

    def test_empty_deque(self):
        self.assertTrue(self.deque.is_empty)
        self.assertEqual(len(self.deque), 0)
        with self.assertRaises(IndexError):
            self.deque.pop_first()
        with self.assertRaises(IndexError):
            self.deque.pop_last()

    def test_push_last(self):
        self.deque.push_last(1)
        self.assertFalse(self.deque.is_empty)
        self.assertEqual(len(self.deque), 1)
        self.assertEqual(self.deque.pop_first(), 1)

    def test_push_first(self):
        self.deque.push_first(1)
        self.assertFalse(self.deque.is_empty)
        self.assertEqual(len(self.deque), 1)
        self.assertEqual(self.deque.pop_first(), 1)

    def test_pop_first(self):
        self.deque.push_last(1)
        self.assertEqual(self.deque.pop_first(), 1)
        self.assertTrue(self.deque.is_empty)
        self.assertEqual(len(self.deque), 0)

    def test_pop_last(self):
        self.deque.push_last(1)
        self.assertEqual(self.deque.pop_last(), 1)
        self.assertTrue(self.deque.is_empty)
        self.assertEqual(len(self.deque), 0)

    def test_push_last_and_pop_first(self):
        self.deque.push_last(1)
        self.deque.push_last(2)
        self.deque.push_last(3)
        self.assertEqual(self.deque.pop_first(), 1)
        self.assertEqual(self.deque.pop_first(), 2)
        self.assertEqual(self.deque.pop_first(), 3)
        self.assertTrue(self.deque.is_empty)
        self.assertEqual(len(self.deque), 0)

    def test_push_first_and_pop_last(self):
        self.deque.push_first(1)
        self.deque.push_first(2)
        self.deque.push_first(3)
        self.assertEqual(self.deque.pop_last(), 1)
        self.assertEqual(self.deque.pop_last(), 2)
        self.assertEqual(self.deque.pop_last(), 3)
        self.assertTrue(self.deque.is_empty)
        self.assertEqual(len(self.deque), 0)

    def test_mixed_operations(self):
        self.deque.push_last(1)
        self.deque.push_last(2)
        self.deque.push_first(3)
        self.assertEqual(len(self.deque), 3)
        self.assertEqual(self.deque.pop_last(), 2)
        self.assertEqual(self.deque.pop_first(), 3)
        self.assertEqual(len(self.deque), 1)
        self.deque.push_first(4)
        self.assertEqual(self.deque.pop_last(), 1)
        self.assertEqual(len(self.deque), 1)
        self.assertEqual(self.deque.pop_first(), 4)
        self.assertTrue(self.deque.is_empty)
        self.assertEqual(len(self.deque), 0)


if __name__ == "__main__":
    unittest.main()
