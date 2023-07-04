import unittest
from stacks import ArrayStack, LinkedListStack

class ArrayStackTest(unittest.TestCase):
    def setUp(self):
        # Create a new instance of ArrayStack for each test case
        self.stack = ArrayStack()

    def test_is_empty(self):
        # Test the is_empty() method
        # The stack should be empty initially
        self.assertTrue(self.stack.is_empty())
        
        # Push an item onto the stack
        self.stack.push(1)
        
        # The stack should no longer be empty
        self.assertFalse(self.stack.is_empty())

    def test_len(self):
        # Test the len() method
        # The initial length of the stack should be 0
        self.assertEqual(self.stack.len(), 0)
        
        # Push an item onto the stack
        self.stack.push(1)
        
        # The length of the stack should be 1
        self.assertEqual(self.stack.len(), 1)
        
        # Push another item onto the stack
        self.stack.push(2)
        
        # The length of the stack should be 2
        self.assertEqual(self.stack.len(), 2)

    def test_push(self):
        # Test the push() method
        # Push an item onto the stack
        self.stack.push(1)
        
        # The length of the stack should be 1
        self.assertEqual(self.stack.len(), 1)
        
        # Pop the item from the stack
        self.assertEqual(self.stack.pop(), 1)

    def test_pop(self):
        # Test the pop() method
        # Popping from an empty stack should raise an IndexError
        with self.assertRaises(IndexError):
            self.stack.pop()

        # Push two items onto the stack
        self.stack.push(1)
        self.stack.push(2)
        
        # Pop the top item from the stack, it should be 2
        self.assertEqual(self.stack.pop(), 2)
        
        # Pop the next item from the stack, it should be 1
        self.assertEqual(self.stack.pop(), 1)
        
        # The stack should be empty now
        self.assertTrue(self.stack.is_empty())
        
        # Popping from an empty stack should raise an IndexError
        with self.assertRaises(IndexError):
            self.stack.pop()
            
class LinkedListStackTest(ArrayStackTest):
    # Inherits all tests from ArrayStackTest, we just need to
    # redefine the setUp method to use a LinkedListStack instance:
    def setUp(self):
        self.stack = LinkedListStack()

if __name__ == '__main__':
    unittest.main()
