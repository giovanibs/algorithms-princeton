from mergesort import MergeSort

class BottomUpMerge(MergeSort):
    """
    Pass through the array, merging subarrays of size `1`
    Repeat for subarrays of size 2, 4, 8...
    
    """
    def sort(self, a):
        n = len(a)
        
        if n <= 1: # array is sorted
            return
        
        for size in self.doubling_range(1, n):
            
            for lo in range(0, n-size, 2*size):
                hi = min(lo + 2*size, n)
                mid = lo + size
                
                self.merge(a, lo=lo, mid=mid, hi=hi)
    
    def _sort(self):
        pass

    def doubling_range(self, start, stop):
        if start == 0:
            raise ValueError("Start should be > 0")
        if stop < start:
            raise ValueError("Stop should be >= start")
        
        i = start
        while i <= stop:
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
        
    def test_doubling_range_value_error(self):
        start = 0
        stop = 1
        with self.assertRaises(ValueError):
            list(self.mergesort.doubling_range(start, stop))
        
        start = 2
        stop = 1
        with self.assertRaises(ValueError):
            list(self.mergesort.doubling_range(start, stop))
        
    def test_doubling_range(self):
        start = 1
        stop = 2
        doubling_list = list(self.mergesort.doubling_range(start, stop))
        self.assertEqual(doubling_list, [1, 2])
        
        start = 2
        stop = 2
        doubling_list = list(self.mergesort.doubling_range(start, stop))
        self.assertEqual(doubling_list, [2])
        
        start = 1
        stop = 3
        doubling_list = list(self.mergesort.doubling_range(start, stop))
        self.assertEqual(doubling_list, [1, 2])
        
        start = 1
        stop = 4
        doubling_list = list(self.mergesort.doubling_range(start, stop))
        self.assertEqual(doubling_list, [1, 2, 4])
        
        start = 1
        stop = 7
        doubling_list = list(self.mergesort.doubling_range(start, stop))
        self.assertEqual(doubling_list, [1, 2, 4])
        
        start = 2
        stop = 7
        doubling_list = list(self.mergesort.doubling_range(start, stop))
        self.assertEqual(doubling_list, [2, 4])
     
    
        
if __name__ == "__main__":
    unittest.main()