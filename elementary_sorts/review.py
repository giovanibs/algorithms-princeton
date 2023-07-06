# # # # # # # # # # # #
#   SELECTION SORT    #
# # # # # # # # # # # #
class SelectionSort:
    """
    For each index in the given `array` with length `n`:
    1) SELECTS the smallest item from `index` to the end of the array (`n-1`).
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
    For each `item` and its `index` in a given `array` with length `n`:
    1) Loops through the subarray `array[:index]`,
        starting from the right most item
    2) Subsequentially compares the current `item` with each item to its left
    3) Swaps the items if they are out of order
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
    Shell sort is an extension of the insertion sort,
    or rather it's a generalization.
    
    It uses a sequence of `gap` sizes and, for each `gap`,
    starting from the greatest:
    
    1) Defines virtual subarrays with the indices of the `array` items
    distanced by the current `gap` size.
    ```
        array = [3, 1, 2]
        gap_sequence = [1]
        subarray = [1, 2]
    ```
    
    2) Performs an insertion sort in the virtual subarray.
    For each `item` and its `index` in a given `array` with length `n`:
    
            - Loops through the subarray `array[:index]`, starting from the right most item
            - Subsequentially compares the current `item` with each item to its left
            
            - Swaps the items if they are out of order
            
            ```
            index == 2 -> array[index] == 2
            array[index-gap] == 1 < array[index] -> don't swap
            array == [3, 1, 2]
            array[index-gap] == 3 > array[index] -> swap
            array == [2, 1, 3]
            
            index == 1 -> array[index] == 1
            array[index-gap] == 2 > array[index] -> swap
            array == [1, 2, 3]
            ```
    
    When `gap` reaches `1`, it performs a insertion sort in the whole `array`.
    """
    
    def sort(self, array):
        n = len(array)
        
        gap_sequence = self.knuths_sequence(n)

        for gap in gap_sequence[::-1]:
            
            for rightmost in range(gap, n):
                subarray = self.virtual_subarray(array[:rightmost+1], gap)
            
                for index in subarray[::-1]:
                    if array[index] < array[index - gap]:
                        self.swap_items(array, index, index-gap)

    def virtual_subarray(self, array, gap):
        """
        Returns a virtual subarray of a length n `array`
        with indices for every `gap`-th item
        """
        n = len(array)
        subarray = list(range(gap, n, gap))
        return subarray
                    
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