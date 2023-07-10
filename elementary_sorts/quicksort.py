from random import shuffle

class QuickSort:
    """
    - In-place sorting algorith.
    - Uses recursion, just like mergesort, but it is done after
    all the work is done.
    It is not stable.
    
    1) Shuffle the array: probabilistic guarantee against worst case
    
    2) Partition the array. That is, find some `j`, such as entry `a[j]` is in place, that is:
            - no larger entry to the left of `j`
            - no smaller entry to the right of `j`
    
    3) Sort each piece recursively: a[lo, j) and a(j, hi)
    """
    @staticmethod
    def sort(a):
        # 1) Shuffle the array: probabilistic guarantee against worst case
        shuffle(a)
        lo = 0
        hi = len(a)
        QuickSort._sort(a, lo, hi)
        
    def _sort(a, lo, hi):
        
        if (hi - lo) <= 1:
            return
        
        # 2) Partition the array. That is, find some `j`, such as entry
        # `a[j]` is in place
        j = QuickSort._partition(a, lo, hi)
        
        # at this point, there is no larger entry to the left of `j` and
        # no smaller entry to the right of `j`.
        
        # 3) Sort each piece recursively
        # j-th entry is in order, so it`s ignored for the next partitioning
        QuickSort._sort(a, lo, j)
        QuickSort._sort(a, j+1, hi)
        
    @staticmethod
    def _partition(a, lo, hi):
        """
        1) Start at pointer `lo`:
                - `i = lo + 1`
                - `j = hi`
        
        2) Repeat until `i` and `j` pointers crosses:
                - Scan `i` from left to right to find the first element `a[i]`, such as `a[i] < a[lo]`
                - Scan `j` from left to right to find the first element `a[j]`, such as `a[j] > a[lo]`
        
        3) Swap `a[i]` with `a[j]` (they're out of order)
        
        4) Swap partitioning item `a[lo]` with `a[j]` after `i` and `j` crosses.
        
        #############################
        VISUAL EXAMPLE:
        array = [Q, U, I, C, K, S, O, R, T, E, X, A, M, P, L, E]
        
        - SHUFFLE array and START pointers:
        
            0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15 > position
            K   R   A   T   E   L   E   P   U   I   M   Q   C   X   O   S
            ^   ^ i                                                     ^ j
            lo                                                         
        
        - NO CROSS OVER, so SWAP them and find next (i, j):
        
            0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
            K   R   A   T   E   L   E   P   U   I   M   Q   C   X   O   S       
            ^   ^ i -> a[i] > a[lo]                         ^ j -> a[j] < a[lo]
            lo
        
        - NO CROSS OVER, so SWAP them and find next (i, j):
        
            0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
            K   C   A   T   E   L   E   P   U   I   M   Q   R   X   O   S
            ^ lo        ^ i -> a[i] > a[lo]     ^ j -> a[j] < a[lo]
                             
        - NO CROSS OVER, so SWAP them and find next (i, j):
        
            0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
            K   C   A   I   E   L   E   P   U   T   M   Q   R   X   O   S
            ^                   ^   ^ j -> a[j] < a[lo]
            lo                  i -> a[i] > a[lo]       
        
        - Next (i, j) found, but they have CROSSED. 
        
            0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
            K   C   A   I   E   E   L   P   U   T   M   Q   R   X   O   S
            ^                   ^   ^ i -> a[i] > a[lo]
            lo                  j -> a[j] < a[lo]
        
        - Since the elements have crossed, i.e. any entry to the left of `i`
        is less than a[lo], and any entry to the right of `j` is greater than
        a[lo], we swap a[lo] with a[j] and end the partiotioning.
        The returning array will be:
        
            0   1   2   3   4   [5] 6   7   8   9   10  11  12  13  14  15
            E   C   A   I   E   [K] L   P   U   T   M   Q   R   X   O   S
            ^                   ^   ^ i -> a[i] > a[lo]
            lo                  j -> a[j] < a[lo]
            
        Now `K` is the partitioning element and it is already in its place,
        thus the quick sort algorithm will call `partition` again for each
        of the subarrays a[0, j) and a[j+1, ]
        """
        i = lo + 1
        j = hi - 1
        # print(f"{a = }\n{lo = }\n{i = }\n{j = }")
        while True:
            
            while a[i] < a[lo]: # find item on the left TO SWAP
                if i == (hi - 1):
                    break
                i += 1
            
            while a[j] > a[lo]: # find item on the right to swap
                if j == lo:
                    break
                j -= 1
                
            # `i` and `j` cross
            if i >= j:
                break
            
            a[i], a[j] = a[j], a[i] # swap items
        
        # since the elements have crossed and any entry to the left of `i`
        # is less than the partitioning entry, we swap a[lo] and a[j] and
        # finally `a` is partitioned:
        a[lo], a[j] = a[j], a[lo]
        
        return j

import unittest

class TestQuickSort(unittest.TestCase):
    def setUp(self) -> None:
        self.sorter = QuickSort
    
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

    def test_sort(self):
        a = [1,0]
        self.sorter.sort(a)
        self.assertEqual(a, [0, 1])

        a = [2_000, 30, 100]
        self.sorter.sort(a)
        self.assertEqual(a, [30, 100, 2_000])

        a = ['c', 'b', 'e', 'd', 'a']
        self.sorter.sort(a)
        self.assertEqual(a, ['a', 'b', 'c', 'd', 'e'])

    def test_random_cases(self):
        for n in range(1_000):
            sorted_a = list(range(n))
            shuffle(a := sorted_a[:])
            self.sorter.sort(a)
            self.assertEqual(a, sorted_a)