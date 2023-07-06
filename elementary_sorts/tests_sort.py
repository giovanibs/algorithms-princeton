import unittest
import random
from selection_sort import SelectionSort
from InsertionSort import InsertionSort
from ShellSort import ShellSort

class TestSelectionSort(unittest.TestCase):
    def setUp(self) -> None:
        self.sorter = SelectionSort()
    
    def test_sort_int(self):
        array = list(range(16))
        random.shuffle(array)
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
        
class TestInsertionSort(TestSelectionSort):
    def setUp(self) -> None:
        self.sorter = InsertionSort()
    
class TestShellSort(TestSelectionSort):
    def setUp(self) -> None:
        self.sorter = ShellSort()
    

if __name__ == "__main__":
    unittest.main()