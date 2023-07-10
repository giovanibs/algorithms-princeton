from quicksort import QuickSort
from random import shuffle

class QuickSelect(QuickSort):
    @staticmethod
    def sort():
        pass
    
    @staticmethod
    def _sort():
        pass
    
    @staticmethod
    def _partition(a, lo, hi):
        return QuickSort._partition(a, lo, hi)
    
    @staticmethod
    def select(a, k):
        """
        1) Shuffle `a`
        
        2) Partition array `a`:
                - j = partition(a, lo, hi)
                
        2) Repeat the partition on the subarray containing k:
                - if k > j: j = partition(a, j + 1, hi)
                - if k < j: j = partition(a, lo, j)

        3) When j == k, return a[k]
        """
        
        if not a:
            return None
        
        n = len(a)
        
        if k >= n:
            raise ValueError
        
        if n == 1:
            return a[0]
        
        # 1) Shuffle `a`
        shuffle(a)
        lo = 0
        hi = n
        
        # print(f"{a = }\n{k = }\n{lo = }\n{hi = }")
        
        while lo < (hi-1):
            # partition a
            j = QuickSelect._partition(a, lo, hi)
            
            if k < j:
                hi = j
            elif k > j:
                lo = j + 1
            else:
                return a[k]
        
        return a[k]
            
#####################
#   TESTS
#####################

import unittest
from random import randrange, shuffle

class TestQuickSelect(unittest.TestCase):
    def setUp(self) -> None:
        self.selector = QuickSelect
        
    def test_edge_cases(self):
        
        # a is empty
        a = []
        k = 0
        result = self.selector.select(a, k)
        self.assertEqual(result, None)
        
        # len(a) == 1
        a = ['one']
        k = 0
        result = self.selector.select(a, k)
        self.assertEqual(result, 'one')
        
        # k out of range
        a = ['a', 'b', 'c']
        k = 3
        with self.assertRaises(ValueError):
            self.selector.select(a, k)

    def test_quick_select(self):
        a = [0, 1, 2, 3, 4]
        k = 3
        
        result = self.selector.select(a, k)
        self.assertEqual(result, 3)
        
    def test_random_cases(self):
        for n in range(2, 1_000):
            a = list(range(n))
            k = randrange(0, n)
            expected = a[k]
            shuffle(a)
            
            result = self.selector.select(a, k)
            self.assertEqual(result, expected)
        