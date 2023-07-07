from unittest import TestCase
from mergesort import MergeSort
from random import shuffle

class TestMergeSort(TestCase):
    def setUp(self) -> None:
        self.mergesort = MergeSort()
    
    def test_mergesort(self):
        for n in range(1_000):
            shuffle(a := list(range(n)))
            self.mergesort.sort(a)
            self.assertEqual(a, sorted(a))
            
    def test_sort_empty_array(self):
        a = []
        self.mergesort.sort(a)
        self.assertEqual(a, [])

    def test_sort_single_element(self):
        a = [5]
        self.mergesort.sort(a)
        self.assertEqual(a, [5])

    def test_sort_sorted_array(self):
        a = [1, 2, 3, 4, 5]
        self.mergesort.sort(a)
        self.assertEqual(a, [1, 2, 3, 4, 5])

    def test_sort_reverse_sorted_array(self):
        a = [5, 4, 3, 2, 1]
        self.mergesort.sort(a)
        self.assertEqual(a, [1, 2, 3, 4, 5])

    def test_sort_random_array(self):
        a = [9, 2, 7, 1, 5, 3, 8, 4, 6]
        self.mergesort.sort(a)
        self.assertEqual(a, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_sort_duplicate_values(self):
        a = [5, 2, 7, 1, 5, 3, 8, 4, 5]
        self.mergesort.sort(a)
        self.assertEqual(a, [1, 2, 3, 4, 5, 5, 5, 7, 8])
    

class TestMerge(TestCase):
    def setUp(self) -> None:
        self.mergesort = MergeSort()
    
    def test_merge_unsorted_subarrays(self):
        
        # left subarray unsorted
        a = [1, 0, 2, 3, 4, 5]
        n = len(a)
        lo, mid, hi = 0, n//2, n
        
        with self.assertRaises(AssertionError):
            self.mergesort.merge(a, lo, mid, hi)
            
        # right subarray unsorted
        a = [0, 1, 2, 3, 5, 4]
        n = len(a)
        lo, mid, hi = 0, n//2, n
        
        with self.assertRaises(AssertionError):
            self.mergesort.merge(a, lo, mid, hi)
        
        # both unsorted
        a = [0, 2, 1, 3, 5, 4]
        n = len(a)
        lo, mid, hi = 0, n//2, n
        
        with self.assertRaises(AssertionError):
            self.mergesort.merge(a, lo, mid, hi)
        
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
        for n in range(1_000):
            shuffle(a:=list(range(n)))
            n = len(a)
            lo = 0
            mid = n//2
            hi = n
            
            # sort the subarrays
            a[lo:mid] = sorted(a[lo:mid])            
            a[mid:hi] = sorted(a[mid:hi])   
                     
            self.mergesort.merge(a, lo, mid, hi)
            self.assertEqual(a, sorted(a))