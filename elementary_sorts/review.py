# # # # # # # # # # # #
#   SELECTION SORT    #
# # # # # # # # # # # #
class SelectionSort:
    """
    For each index in the given `array` with length `n`:
    1) SELECTS the smallest item in `array[index, n)`.
    2) swaps the found item with the item in the `index` position.
    """
    
    def sort(self, array: list) -> None:
        for index in range(len(array)):
            smallest, smallest_index = self.select_smallest(array, index)
            if index != smallest_index:
                self.swap_items(array, index, smallest_index)

    def select_smallest(self, array: list, index: int) -> tuple:
        smallest = min(array[index:])
        smallest_index = array.index(smallest)
        return smallest, smallest_index

    def swap_items(self, array, index1, index2) -> None:
        array[index1], array[index2] = \
                array[index2], array[index1]
                
from tests_sort import TestSelectionSort

class TestSelection(TestSelectionSort):
    def setUp(self) -> None:
        self.sorter = SelectionSort()
        
        
# # # # # # # # # # # # 
#   INSERTION SORT    #
# # # # # # # # # # # #
class InsertionSort:
    """
        Insertion sort creates a sorted subarray that subsequentially
    increases in length to add a new item. The new item is compared and swaped,
    from right to left, with each other item until it finds its place in the
    sorted subarray.
    
        In other words, for each `item` and its `index` in a given `array` with
    length `n` (starting from the second item a.k.a. `index == 1`):
    
    1) Loops through the subarray `array[0, index+1)`, starting from
    the RIGHT most item, ie. `array[index]`.
    
    2) Subsequentially compares the current `item` with each item to its
    left:
            - `array[index]` < `array[index-1]` ?
    
    3) Swaps the items if they are out of order. Increment `index` otherwise.
    """
    
    def sort(self, array):
        n = len(array)
        
        for index in range(n):
            for current_index in range(index, 0, -1):
                if array[current_index] < array[current_index - 1]:
                    self.swap_items(array, current_index, current_index-1)
                    
    def swap_items(self, array, index1, index2) -> None:
        array[index1], array[index2] = \
                array[index2], array[index1]
                
from tests_sort import TestInsertionSort

class TestInsertion(TestInsertionSort):
    def setUp(self) -> None:
        self.sorter = InsertionSort()
        
        
# # # # # # # # # # # # 
#   SHELL SORT        #
# # # # # # # # # # # #
class ShellSort:
    """
        Shell sort is an extension of the insertion sort, or rather it's a
    generalization. Basically, instead of doing the following comparison:
    
            - `array[index]` < `array[index-1]` ?
            
    it does the following:
    
            - `array[index]` < `array[index-gap]` ?
    
        That means that the subarrays are now defined by sampling items that
    are `gap`-indices apart, where `gap` is part of a sequence of sizes,
    having at least the size `1` -- eg. `gap_sequence = [1, 2, 4, 8]` -- and
    starting from the greatest gap, ie `gap_sequence[-1]`.
        
        When `gap` reaches `1`, it is like performing an insertion sort in the
    whole `array`. But, at this point, small items have already been moved from
    long distances during the iteration with larger gap sizes, thus reducing
    the number of compares and swaps.
    
    In other words:
    
    - Iterates over a reversed sequence of `gap` sizes and, the last being `1`.
    For each `gap`:
        - Iterates over the subarray `array[gap, n)`. For each index `i`:
            - Performs an insertion sort on the items distanced by the current
            `gap` size, starting from `array[i]` (aka the right most item) to
            `array[gap]`. That is, compares `array[i]` to `array[i-gap]` and
            swap them if they're out of order.
    """
    
    def sort(self, array):
        n = len(array)
        
        gap_sequence = self.knuths_sequence(n)

        for gap in gap_sequence[::-1]:
            
            # now comes the insertion sort
            for rightmost in range(gap, n):
                # `gap-1` bc it's exclusive (could be `zero` with no prejudice)
                for index in range(rightmost, gap-1, -gap):
                    if array[index] < array[index - gap]:
                        self.swap_items(array, index, index-gap)

    def swap_items(self, array, index1, index2) -> None:
        array[index1], array[index2] = \
                array[index2], array[index1]
                
    def knuths_sequence(self, n: int) -> list:
        """
        Generates a gap sequence using the Knuth's formula:
            `gap = 3*gap + 1`
        """
        
        # edge case
        if n//3 <= 1:
            return [1]
        
        gap = 1
        gap_sequence = []
        while gap < n//3:
            gap_sequence.append(gap)
            gap = 3*gap + 1
        return gap_sequence
                
from tests_sort import TestShellSort

class TestShell(TestShellSort):
    def setUp(self) -> None:
        self.sorter = ShellSort()
        
        
# # # # # # # # # # # # 
#   MERGE SORT        #
# # # # # # # # # # # #

class MergeSort:
    """
    Overall steps:
    
    1) Find `mid`
    2) Divide `a` into two subarrays and recursively sort them
            - a[lo:mid)
            - a[mid:hi)
    3) Merge them
    """
    @staticmethod
    def sort(a):
        n = len(a)
        MergeSort._sort(a, 0, n)
        
    @staticmethod
    def _sort(a, lo, hi):
        
        if (hi - lo) <= 1: # subarray is sorted
            return
        
        # 1) Find `mid`
        mid = lo + ( hi - lo )//2       # reduces chance of int overflow
        
        # 2) Divide `a` into two subarrays and recursively sort them:
        MergeSort._sort(a, lo, mid)     # left_subarray  == a[lo:mid)
        MergeSort._sort(a, mid, hi)     # right_subarray == a[mid:hi)
        
        # 3) Merge them
        aux = a[:]  # auxiliary array for merging
        MergeSort._merge(a, lo, mid, hi, aux)
            
    @staticmethod
    def _merge(a, lo, mid, hi, aux):
        """
        Merge two sorted subarrays of `a`:
            - `a[lo, mid)` and `a[mid, hi)`
        
        Steps:
        1) initiate 3 pointers:
                - `merged`: pointer to update values in `a`
                - `left`:   pointer to loop the left subarray (aux array)
                - `right`:  pointer to loop the left subarray (aux array)
        2) for each `a[merged]`:
                - `a[merged]` <- smallest between `aux[left]` and `aux[right]`
                - increment the index of the selected (left or right)
        """
        assert a[lo:mid] == sorted(a[lo:mid]), "Left subarray is not sorted!"
        assert a[mid:hi] == sorted(a[mid:hi]), "Right subarray is not sorted!"
        
        left  = lo
        right = mid
        
        # loop `a` with `merged` as index
        for merged in range(lo, hi):
            
            if (left == mid) or (right == hi):
                # one of the subarrays is exhausted
                a[merged:hi] = aux[left:mid] or aux[right:hi]
                break
            
            elif aux[left] <= aux[right]:
                a[merged] = aux[left]
                left += 1
        
            elif aux[right] < aux[left]:
                a[merged] = aux[right]
                right += 1
        
import unittest
from random import shuffle

class TestMergeSort(unittest.TestCase):
    def setUp(self) -> None:
        self.mergesort = MergeSort
        
    def test_merge(self):
        a = [1, 0]
        aux = a[:]
        lo = 0
        hi = len(a) # 2
        mid = lo + (hi-lo)//2 # 1
        self.mergesort._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1])
        
        a = [2, 0, 1]
        aux = a[:]
        lo = 0
        hi = len(a)
        mid = lo + (hi-lo)//2
        self.mergesort._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2])
        
        a = [0, 1, 2]
        aux = a[:]
        lo = 0
        hi = len(a)
        mid = lo + (hi-lo)//2
        self.mergesort._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2])
        
        a = [2, 0, 1]
        aux = a[:]
        lo = 0
        hi = len(a)
        mid = lo + (hi-lo)//2
        self.mergesort._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2])
        
        a = [2, 0, 1, 5, 6, 3, 4]
        aux = a[:]
        lo = 3
        hi = 7
        mid = lo + (hi-lo)//2
        self.mergesort._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [2, 0, 1, 3, 4, 5, 6])
        
        with self.assertRaises(AssertionError):
            a = [2, 1, 0]
            aux = a[:]
            lo = 0
            hi = len(a)
            mid = lo + (hi-lo)//2
            self.mergesort._merge(a, lo, mid, hi, aux)
        
        with self.assertRaises(AssertionError):
            a = [0, 1, 3, 2]
            aux = a[:]
            lo = 0
            hi = len(a)
            mid = lo + (hi-lo)//2
            self.mergesort._merge(a, lo, mid, hi, aux)
    
    def test_edge_cases(self):
        # a is empy
        a = []
        self.mergesort.sort(a)
        self.assertEqual(a, [])

        # a has 1 element
        a = [1]
        self.mergesort.sort(a)
        self.assertEqual(a, [1])

        # a is already sorted
        a = ['a', 'b', 'c', 'd', 'e']
        self.mergesort.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

        # a is reversely sorted
        a = ['e', 'd', 'c', 'b', 'a']
        self.mergesort.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

    def test_merge_and_sort(self):
        a = [1,0]
        self.mergesort.sort(a)
        self.assertEqual(a, [0, 1])

        a = [2_000, 30, 100]
        self.mergesort.sort(a)
        self.assertEqual(a, [30, 100, 2_000])

        a = ['c', 'b', 'e', 'd', 'a']
        self.mergesort.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

    def test_mergesort_random_cases(self):
        for n in range(1_000):
            sorted_a = list(range(n))
            shuffle(a := sorted_a[:])
            self.mergesort.sort(a)
            self.assertEqual(a, sorted_a)

if __name__ == "__main__":
    unittest.main()