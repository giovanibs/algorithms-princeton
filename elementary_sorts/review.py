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