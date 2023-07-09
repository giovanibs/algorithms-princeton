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
        
        for size in self.doubling_range(1, n):      # n == 7 | size == 1   
                                                    #       
            for lo in range(0, n-size, 2*size):     # lo    0   2   4   6
                hi = min(lo + 2*size, n-1)          # hi    2   4   6   6
                mid = lo + (hi - lo)//2             # mid   1   3   5   6
                
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

class BottomUpMergeTests(TestMergeSort):
    def setUp(self) -> None:
        self.mergesort = BottomUpMerge()
    
    def test_sort(self):
        a = [4, 6, 5, 3]
        self.mergesort.sort(a)
        self.assertEqual(a, [3, 4, 5, 6])

if __name__ == "__main__":
    unittest.main()