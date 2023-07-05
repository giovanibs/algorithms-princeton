import unittest
import random
from selection_sort import SelectionSort

class TestSelectionSort(unittest.TestCase):
    def setUp(self) -> None:
        self.sorter = SelectionSort()
    
    def test_sort_int(self):
        array = [2, 5, 0, 4, 1, 3]
        self.sorter.sort(array)
        self.assertEqual(array, sorted(array))
    
    def test_sort_str(self):
        array = ['cab', 'cba', 'bac', 'bca', 'abc', 'acb']
        self.sorter.sort(array)
        self.assertEqual(array, sorted(array))
        
    def test_sort_lots_of_items(self):
        array = list(range(10000))
        random.shuffle(array)
        self.sorter.sort(array)
        self.assertEqual(array, sorted(array))

if __name__ == "__main__":
    unittest.main()