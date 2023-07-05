from queues import Queue, LinkedListQueue, Deque
import unittest
from tests_stacks import LinkedListStackTest


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_empty_queue(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.len(), 0)
        self.assertIsNone(self.queue.dequeue())

    def test_enqueue_dequeue(self):
        self.queue.enqueue("A")
        self.queue.enqueue("B")
        self.queue.enqueue("C")
        self.assertEqual(self.queue.len(), 3)
        self.assertEqual(self.queue.dequeue(), "A")
        self.assertEqual(self.queue.dequeue(), "B")
        self.assertEqual(self.queue.len(), 1)
        self.queue.enqueue("D")
        self.assertEqual(self.queue.dequeue(), "C")
        self.assertEqual(self.queue.dequeue(), "D")
        self.assertTrue(self.queue.is_empty())

    def test_enqueue_dequeue_different_types(self):
        self.queue.enqueue(1)
        self.queue.enqueue("hello")
        self.queue.enqueue([1, 2, 3])
        self.assertEqual(self.queue.len(), 3)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), "hello")
        self.assertEqual(self.queue.dequeue(), [1, 2, 3])

    def test_enqueue_dequeue_large_number(self):
        for i in range(100000):
            self.queue.enqueue(i)
        self.assertEqual(self.queue.len(), 100000)
        self.assertEqual(self.queue.dequeue(), 0)
        self.assertEqual(self.queue.len(), 99999)

        while not self.queue.is_empty():
            self.queue.dequeue()
        self.assertIsNone(self.queue.dequeue())


class LinkedListQueueTests(QueueTests):
    def setUp(self):
        self.queue = LinkedListQueue()
        
if __name__ == "__main__":
    unittest.main()
