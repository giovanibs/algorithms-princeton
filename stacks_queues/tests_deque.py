import unittest
from deque import Deque

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