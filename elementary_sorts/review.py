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
        self.sorter = MergeSort
        
    def test_merge(self):
        a = [1, 0]
        aux = a[:]
        lo = 0
        hi = len(a) # 2
        mid = lo + (hi-lo)//2 # 1
        self.sorter._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1])
        
        a = [2, 0, 1]
        aux = a[:]
        lo = 0
        hi = len(a)
        mid = lo + (hi-lo)//2
        self.sorter._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2])
        
        a = [0, 1, 2]
        aux = a[:]
        lo = 0
        hi = len(a)
        mid = lo + (hi-lo)//2
        self.sorter._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2])
        
        a = [2, 0, 1]
        aux = a[:]
        lo = 0
        hi = len(a)
        mid = lo + (hi-lo)//2
        self.sorter._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [0, 1, 2])
        
        a = [2, 0, 1, 5, 6, 3, 4]
        aux = a[:]
        lo = 3
        hi = 7
        mid = lo + (hi-lo)//2
        self.sorter._merge(a, lo, mid, hi, aux)
        self.assertEqual(a, [2, 0, 1, 3, 4, 5, 6])
        
        with self.assertRaises(AssertionError):
            a = [2, 1, 0]
            aux = a[:]
            lo = 0
            hi = len(a)
            mid = lo + (hi-lo)//2
            self.sorter._merge(a, lo, mid, hi, aux)
        
        with self.assertRaises(AssertionError):
            a = [0, 1, 3, 2]
            aux = a[:]
            lo = 0
            hi = len(a)
            mid = lo + (hi-lo)//2
            self.sorter._merge(a, lo, mid, hi, aux)
    
    def test_edge_cases(self):
        # a is empy
        a = []
        self.sorter.sort(a)
        self.assertEqual(a, [])

        # a has 1 element
        a = [1]
        self.sorter.sort(a)
        self.assertEqual(a, [1])

        # a is already sorted
        a = ['a', 'b', 'c', 'd', 'e']
        self.sorter.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

        # a is reversely sorted
        a = ['e', 'd', 'c', 'b', 'a']
        self.sorter.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

    def test_merge_and_sort(self):
        a = [1,0]
        self.sorter.sort(a)
        self.assertEqual(a, [0, 1])

        a = [2_000, 30, 100]
        self.sorter.sort(a)
        self.assertEqual(a, [30, 100, 2_000])

        a = ['c', 'b', 'e', 'd', 'a']
        self.sorter.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

    def test_mergesort_random_cases(self):
        for n in range(1_000):
            sorted_a = list(range(n))
            shuffle(a := sorted_a[:])
            self.sorter.sort(a)
            self.assertEqual(a, sorted_a)


# # # # # # # # # # # # 
#   BOTTOM-UP MERGE   #
# # # # # # # # # # # #

class BottomUpMerge(MergeSort): # we`re gonna re-use the merge method
    """
    Overall steps:
    
    1) Start merging subarrays of length `1`
    2) subsequentally doubles the length of the subarrays and keep merging 
    """
    
    @staticmethod
    def sort(a):
        n = len(a)
        
        if n <= 1: # array is sorted
            return
        
        doubling_range = BottomUpMerge.doubling_range(1, n)
        
        for step in doubling_range:
            aux = a[:]
            
            for lo in range(0, n-step, 2*step):
                hi = min(lo + 2*step, n) # is overflow a possibility?
                mid = lo + step
                BottomUpMerge._merge(a, lo, mid, hi, aux)
    
    @staticmethod
    def _sort():
        pass
    
    @staticmethod
    def doubling_range(start, stop):
        """
        Aux method to generate a doubling range from `start` to `stop`
        """
        i = start
        while i < stop:
            yield i
            i *= 2

class TestBottomUpMerge(TestMergeSort):
    def setUp(self) -> None:
        self.sorter = BottomUpMerge


# # # # # # # # # # # # 
#   QUICK SELECT      #
# # # # # # # # # # # #
class QuickSelect:
    """
    Goal: find the `k`-th (0-indexed) entry in the given array `a`.
    
    """
    
    @staticmethod
    def select(a, k):
        """
        Steps:
        1) Shuffle `a`
        2) Partition `a`
        3) Check in which subarray `k` should be (< or > partition index?)
        4) Partition only the desired subarray and repeat the process until one of this conditions are met:
            - k == partition element's index or
            - the array is sorted, then return `a[k]`.
        """
        n = len(a)
        # egdge cases
        if not n:
            return None
        
        if k >= n:
            raise ValueError(f"{k = } must be less than {len(a) = }")
        
        if n == 1:
            return a[0]
        
        shuffle(a)
        hi = n
        lo = 0
        
        while lo < (hi-1):
            j = QuickSelect._partition(a, lo, hi)
            
            if k < j:       # k is in the left subarray a[lo, j)
                hi = j
            elif k > j:     # k is in the right subarray a[j+1, hi]
                lo = j + 1
            else:           # k == j
                break    
        
        return a[k]
    
    @staticmethod
    def _partition(a, lo, hi):
        """
        Goal: find a `j`-th array entry, so that:
            - all entries to its left are less than `a[j]`
            - all entries to its right are greater than `a[j]`
            
        Steps:
            1) initialize 3 pointers:
                - lo                : first subarray index
                - `left = lo + 1`   : scan subarray from left to right.
                - `right = hi - 1`  : scan subarray from right to left; 
            
            2) Repeat until left and right crosses:
                - scan subarray from left to right until a[left] > a[lo]
                - scan subarray from right to left until a[right] < a[lo]
                - swap a[left] < a[right], since they're out of order
                
            3) Upon crossing:
                - all entries to the right of a[right] are `> a[lo]` and
                - all entries to its left are `< a[lo]`
                - then, swap a[lo] and a[right] so that the partition element
                is in its righful place
            
            4) Return the value of `right`.
        """
        
        left = lo + 1
        right = hi - 1
        
        while True:
            while a[left] < a[lo]:
                if left == hi-1:
                    break
                left += 1
            
            while a[right] > a[lo]:
                right -= 1
            
            if left >= right:
                break
            
            a[left], a[right] = a[right], a[left]
            
        a[lo], a[right] = a[right], a[lo]
        
        return right
   
from random import randrange

class TestsQuickSelect(unittest.TestCase):
    def setUp(self) -> None:
        self.selector = QuickSelect
        
    def test_partition(self):
        a = [3, 1, 0, 2]
        expected = 3
        result = self.selector._partition(a, lo=0, hi=4)
        self.assertEqual(result, expected)
        
        for n in range(2, 1_000):
            shuffle(a := list(range(n)))
            n = len(a)
            expected = a[0]
            result = self.selector._partition(a, 0, n)
            self.assertEqual(result, expected,
                            f"{a = }\n{expected = }\n{result = }"
                             )

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
        #             ^ k
        expected = a[k:= 3]
        
        result = self.selector.select(a, k)
        self.assertEqual(result, expected)
        
    def test_random_cases(self):
        for n in range(2, 1_000):
            a = list(range(n))
            k = randrange(0, n)
            expected = a[k]
            shuffle(a)
            result = self.selector.select(a, k)
            self.assertEqual(result, expected)
            
if __name__ == "__main__":
    unittest.main()