class ThreeWayQuickSort:
    """
    The goal of 3-way partitioning is to speed up quicksort in the presence of
    duplicate keys.

    That is, for the partitioning entry `a[v]`, partition the input array
    `a[lo, hi)` into 3 parts so that:
    
        - Entries a[lo, lt) are `< a[v]`
        - Entries a[gt+1, hi) are `> a[v]`
        - Entries a[lt, gt] are `== a[v]`
    
    Steps:
    
    1) Let `v` be the partitioning item `a[lo]`.
    2) Start pointers:
        - i = lo
        - lt = lo
        - gt = hi - 1
    
    3) Scan i from left to right:
        - if a[i] < v:
            - swap a[i] and a[lt]
            - i++ and lt++
        
        - if `a[i] > v`:
            - swap `a[i]` and `a[gt]`
            - `gt--`
            
        - if `a[i] == v`:
            - `i++`
            
    4) The partitioning is complete when `i` and `gt` crosses.
    
    5) Recursively sort `a[lo, lt)` and `a(gt, hi)` until the whole array is sorted.
    """
    
    @staticmethod
    def sort(a):
        n = len(a)
        if n <= 1: # a is sorted
            return
        ThreeWayQuickSort._sort(a, 0, n)
    
    @staticmethod
    def _sort(a, lo, hi):
        
        if (hi - lo) <= 1: # a is sorted
            return
        
        # 1) Let `v` be the partitioning item `a[lo]`.
        v = a[lo]
        
        # 2) Start pointers:
        i = lt = lo
        gt = hi - 1
        
        # 3) Scan i from left to right:
        while i <= gt:
            if a[i] < v:
                a[i], a[lt] = a[lt], a[i]
                i  += 1
                lt += 1
                
            elif a[i] > v:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
                
            else:
                i += 1
                
        # 5) Recursively sort a[lo, lt) and a[gt+1, hi) until the whole array is
        # sorted.
        ThreeWayQuickSort._sort(a, lo, lt)
        ThreeWayQuickSort._sort(a, gt+1, hi)
        
import unittest
from random import shuffle, randrange

class Tests3WayQuickSort(unittest.TestCase):
    def setUp(self) -> None:
        self.sort = ThreeWayQuickSort.sort
    
    # EDGE CASES
    def test_sort_empty_array(self):
        a = []
        self.sort(a)
        self.assertEqual(a, [])

    def test_sort_single_element(self):
        a = [5]
        self.sort(a)
        self.assertEqual(a, [5])

    def test_sort_sorted_array(self):
        a = [1, 2, 3, 4, 5]
        self.sort(a)
        self.assertEqual(a, [1, 2, 3, 4, 5])

    def test_sort_reverse_sorted_array(self):
        a = [5, 4, 3, 2, 1]
        self.sort(a)
        self.assertEqual(a, [1, 2, 3, 4, 5])

    def test_sort_array_with_all_duplicates(self):
        a = [1, 1, 1, 1, 1]
        self.sort(a)
        self.assertEqual(a, [1, 1, 1, 1, 1])    
    
    # Basic sorting (no duplicates keys)
    def test_basic_sorting(self):
        for n in range(2, 1_000):
            a = list(range(n))
            expected = a[:]
            shuffle(a)
            self.sort(a)
            self.assertEqual(a, expected)
    
    # sorting with duplicate keys     
    def test_duplicate_keys(self):
        a = []
        for _ in range(100):
            duplicate_items = randrange(0, 10)*[randrange(0, 100)]
            a.extend(duplicate_items)
        
        expected = sorted(a)
        self.sort(a)
        self.assertEqual(a, expected)
        

if __name__ == '__main__':
    unittest.main()