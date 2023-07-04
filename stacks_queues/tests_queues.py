from queues import Queue, LinkedListQueue
import unittest

class QueueTests(unittest.TestCase):
    def setUp(self):
        self.q = Queue()
    
    def test_empty_queue(self):
        self.assertTrue(self.q.is_empty())
        self.assertEqual(self.q.len(), 0)
        self.assertIsNone(self.q.dequeue())

    def test_enqueue_dequeue(self):
        self.q.enqueue("A")
        self.q.enqueue("B")
        self.q.enqueue("C")
        self.assertEqual(self.q.len(), 3)
        self.assertEqual(self.q.dequeue(), "A")
        self.assertEqual(self.q.dequeue(), "B")
        self.assertEqual(self.q.len(), 1)
        self.q.enqueue("D")
        self.assertEqual(self.q.dequeue(), "C")
        self.assertEqual(self.q.dequeue(), "D")
        self.assertTrue(self.q.is_empty())

    def test_enqueue_dequeue_different_types(self):
        self.q.enqueue(1)
        self.q.enqueue("hello")
        self.q.enqueue([1, 2, 3])
        self.assertEqual(self.q.len(), 3)
        self.assertEqual(self.q.dequeue(), 1)
        self.assertEqual(self.q.dequeue(), "hello")
        self.assertEqual(self.q.dequeue(), [1, 2, 3])

    def test_enqueue_dequeue_large_number(self):
        for i in range(100000):
            self.q.enqueue(i)
        self.assertEqual(self.q.len(), 100000)
        self.assertEqual(self.q.dequeue(), 0)
        self.assertEqual(self.q.len(), 99999)
        
        while not self.q.is_empty():
            self.q.dequeue()
        self.assertIsNone(self.queue.dequeue())

class LinkedListQueueTests(QueueTests):
    def setUp(self):
        self.queue = LinkedListQueue()
    
if __name__ == "__main__":
    unittest.main()
