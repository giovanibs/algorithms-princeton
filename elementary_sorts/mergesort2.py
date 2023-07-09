class MergeSort:
    @staticmethod
    def sort(a):
        n = len(a)
        MergeSort._sort(a, 0, n)
    
    @staticmethod
    def _sort(a, lo, hi,):
        """
        1) Divide `a` into two subarrays
                - a[lo:mid)
                - a[mid:hi)
        
        2) Recursively sort them
        
        3) Merge them
        """
        
        # if len(subarray) is 0 or 1, then the array is sorted
        if (hi-lo) <= 1:
            return
        
        mid = lo + (hi - lo)//2
        MergeSort._sort(a, lo=lo, hi=mid)   # a[lo:mid)
        MergeSort._sort(a, lo=mid, hi=hi)   # a[mid:hi)
        
        aux = a[:]
        MergeSort._merge(a, lo, mid, hi, aux)
    
    @staticmethod
    def _merge(a, lo, mid, hi, aux):
        """
        Merge two pre-sorted subarrays of `a`:
        - `a[lo:mid)` and `a[mid:hi)`
        
        Steps:
        1) initiate three pointers:
                - `merged`  : index of original array ([lo,hi))
                - `left`    : index of the left subarray
                - `right`   : index of the right subarray
        
        2) For each `merged` index:
                - get the smallest item between `aux[left]` and `aux[right]`
                and assign to `a[merged]`
                - increment the respective pointer
        """
        
        if (hi-lo) <= 1:
            return
        
        # assert that both subarrays are already sorted
        assert a[lo:mid] == sorted(a[lo:mid]), "Left subarray not sorted!"
        assert a[mid:hi] == sorted(a[mid:hi]), "Right subarray not sorted!"
        
        left, right = lo, mid
        try:
            if a[mid-1] < a[mid]: # array is already sorted
                return
        except IndexError:
            print(f"{left = } | {right = }")
            raise IndexError

        for merged in range(lo, hi):
            
            # left or right subarray exhausted
            if (left == mid) or (right == hi):
                a[merged:hi] = aux[left:mid] or aux[right:hi]
                break
            
            elif aux[left] <= aux[right]:
                a[merged] = aux[left]
                left += 1
            elif aux[right] < aux[left]:
                a[merged] = aux[right]
                right += 1

# tests 
import unittest
from random import shuffle
from tests_mergesort import TestMergeSort

class MergeSortTests(unittest.TestCase):
    
    def test_merge(self):
        a = [
            0, 1, 2,
            3, 4, 5,
        ]
        n = len(a)
        lo, hi = 0, n
        mid = lo + (hi-lo)//2
        aux = a[:]
        
        MergeSort._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2, 3, 4, 5])
            
        # random tests
        for n in range(1_000):
            shuffle( a := list(range(n)) )
            lo, hi = 0, n
            mid = lo + (hi-lo)//2
            a[:] = [*sorted(a[lo:mid]), *sorted(a[mid:hi])]
            aux = a[:]
            
            MergeSort._merge(a, lo, mid, hi, aux)
            self.assertEqual(a, sorted(a))
   
    def test_sort(self):
        shuffle(a := list(range(10)))
        MergeSort.sort(a)
        self.assertEqual(a, sorted(a))
        
        for n in range(1_000):
            shuffle(a:=list(range(n)))
            MergeSort.sort(a)
            self.assertEqual(a, sorted(a))
 
class MergeSortOtherTests(TestMergeSort):
    def setUp(self) -> None:
        self.mergesort = MergeSort 
           
if __name__ == "__main__":
    unittest.main()