from mergesort import MergeSort

class BottomUpMerge(MergeSort):
    """
    Pass through the array, merging subarrays of size `1`
    Repeat for subarrays of size 2, 4, 8...
    
    """
    def sort(self, a):
        n = len(a)
        
        if n <= 1:
            # array is sorted
            return
        
        for size in self.doubling_range(1, n):
            
            for lo in range(0, n-size, 2*size):
                hi = min(lo + 2*size, n)
                mid = lo + size
                
                self.merge(a, lo=lo, mid=mid, hi=hi)
    
    def _sort(self):
        pass
    
    def doubling_range(self, start, stop):
        i = start
        while i < stop:
            yield i
            i *= 2

#################
# TESTS
#################            
import unittest
from tests_mergesort import TestMergeSort

class TestsBottomUpMerge(TestMergeSort):
    def setUp(self) -> None:
        self.mergesort = BottomUpMerge()
    
    def test_bot_up_sort(self):
        a = [1, 0]
        self.mergesort.sort(a)
        self.assertEqual(a, [0, 1])
        
        a = [1, 2, 0]
        self.mergesort.sort(a)
        self.assertEqual(a, [0, 1, 2])
        
        a = [0, 1, 2]
        self.mergesort.sort(a)
        self.assertEqual(a, [0, 1, 2])
        
        a = [2, 1, 0]
        self.mergesort.sort(a)
        self.assertEqual(a, [0, 1, 2])
        
if __name__ == "__main__":
    unittest.main()