from unittest import TestCase
from mergesort import MergeSort

class TestMergeSort(TestCase):
    def setUp(self) -> None:
        self.sorter = MergeSort()
    
    def test_merge(self):
        a = [
            3, 5, 6,    # sorted left subarray
            0, 1, 2,    # sorted right subarray
        ]
        
        n = len(a)
        lo = 0
        mid = n//2
        hi = n
        
        self.sorter.merge(a, lo, mid, hi)
        self.assertEqual(a, sorted(a))
        