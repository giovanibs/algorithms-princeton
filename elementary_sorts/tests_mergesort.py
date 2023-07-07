from unittest import TestCase
from mergesort import MergeSort

class TestMergeSort(TestCase):
    def setUp(self) -> None:
        self.mergesort = MergeSort()
    
    def test_merge_edge_cases(self):
        
        a = [] # empty list
        self.mergesort.merge(a, 0, 0, 0)
        self.assertEqual(a, [])

        b = [5] # single element
        self.mergesort.merge(b, 0, 1, 1)
        self.assertEqual(b, [5])

        c = [1, 2, 3, 4, 5] # already sorted list
        self.mergesort.merge(c, 0, 3, 5)
        self.assertEqual(c, [1, 2, 3, 4, 5])
    
    
    def test_merge(self):
        a = [
            3, 5, 6,    # sorted left subarray
            0, 1, 2,    # sorted right subarray
        ]
        
        n = len(a)
        lo = 0
        mid = n//2
        hi = n
        
        self.mergesort.merge(a, lo, mid, hi)
        self.assertEqual(a, sorted(a))
        
        a = [
            0, 1, 2,    # sorted left subarray
            7, 8, 9,    # sorted right subarray
        ]
        
        n = len(a)
        lo = 0
        mid = n//2
        hi = n
        
        self.mergesort.merge(a, lo, mid, hi)
        self.assertEqual(a, sorted(a))