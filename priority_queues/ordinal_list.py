from collections import UserList
from functools import wraps

class OrdinalList(UserList):
    """
    A custom implementation of a list with starting index at `1`
    """
    
    def decrement_index_by_one(func):
        
        @wraps(func)
        def wrapper(self, i=-1, *args, **kwargs):
            """
            Sets a default value of -1 for the i parameter. This ensures that
            when no argument is provided, as in `pop()`, the default value is
            used correctly.
            """
            if isinstance(i, slice):
                raise NotImplementedError("Slicing not supported yet.")
            
            if not isinstance(i, int):
                raise ValueError
            
            if i > len(self):
                raise IndexError
            
            if i > 0:       # Adjust the index if it's positive
                i -= 1
            elif i < 0:     # super() will handle negative indices
                i = i 
            else:
                raise IndexError("Ordinal list has no index 0.")
            
            return func(self, i, *args, **kwargs)
        
        return wrapper
    
    @decrement_index_by_one
    def __getitem__(self, i):
        return super().__getitem__(i)

    @decrement_index_by_one
    def __setitem__(self, i, item):
        return super().__setitem__(i, item)

    @decrement_index_by_one
    def __delitem__(self, i):
        return super().__delitem__(i)
        
    @decrement_index_by_one
    def insert(self, i, item):
        return super().insert(i, item)

    @decrement_index_by_one
    def pop(self, i=-1):
        return super().pop(i)
    
import unittest

class TestsOrdinalList(unittest.TestCase):
    def setUp(self):
        self.lst = OrdinalList([1, 2, 3, 4, 5])

    def test_getitem(self):
        self.assertEqual(self.lst[1], 1)
        self.assertEqual(self.lst[3], 3)
        self.assertEqual(self.lst[-1], 5)

    def test_getitem_index_zero(self):
        with self.assertRaises(IndexError):
            self.lst[0]

    def test_getitem_invalid_index(self):
        with self.assertRaises(IndexError):
            self.lst[6]

    def test_setitem(self):
        self.lst[1] = 10
        self.assertEqual(self.lst[1], 10)

    def test_setitem_index_zero(self):
        with self.assertRaises(IndexError):
            self.lst[0] = 10

    def test_setitem_invalid_index(self):
        with self.assertRaises(IndexError):
            self.lst[6] = 10

    def test_delitem(self):
        del self.lst[1]
        self.assertEqual(self.lst[1], 2)

    def test_delitem_index_zero(self):
        with self.assertRaises(IndexError):
            del self.lst[0]

    def test_delitem_invalid_index(self):
        with self.assertRaises(IndexError):
            del self.lst[6]

    def test_insert(self):
        self.lst.insert(2, 10)
        self.assertEqual(self.lst[2], 10)
        self.assertEqual(self.lst[3], 2)

    def test_insert_index_zero(self):
        with self.assertRaises(IndexError):
            self.lst.insert(0, 10)

    def test_insert_invalid_index(self):
        with self.assertRaises(IndexError):
            self.lst.insert(6, 10)

    def test_pop(self):
        self.assertEqual(self.lst.pop(), 5)
        self.assertEqual(self.lst.pop(2), 2)
        self.assertEqual(len(self.lst), 3)
        self.assertEqual(self.lst[1], 1)
        self.assertEqual(self.lst[2], 3)
        self.assertEqual(self.lst[3], 4)

    def test_pop_index_zero(self):
        with self.assertRaises(IndexError):
            self.lst.pop(0)

    def test_pop_invalid_index(self):
        with self.assertRaises(IndexError):
            self.lst.pop(6)

if __name__ == '__main__':
    unittest.main()