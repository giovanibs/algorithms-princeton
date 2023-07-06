from collections import Counter
import math
from pprint import pprint
import unittest
from random import seed
from shuffling import ShuffleSort, KnuthShuffle

class TestsShuffleSort(unittest.TestCase):
    def setUp(self):
        # Initialize the shuffle_algo object
        self.shuffle_algo = ShuffleSort()
        seed(0)  # Set the random seed for reproducibility

    def test_shuffle_empty_array(self):
        array = []
        expected = []
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, expected)

    def test_shuffle_single_element_array(self):
        array = [5]
        expected = [5]
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, expected)

    def test_shuffle_multiple_elements_array(self):
        array = [1, 2, 3, 4, 5]
        expected = [4, 3, 5, 2, 1]
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, expected)
        
        array = list(range(10))
        expected = [7, 2, 0, 3, 6, 4, 9, 8, 1, 5]
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, expected)
        
    def test_shuffle_repeated_elements_array(self):
        array = [2, 2, 2, 2, 2]
        expected = [2, 2, 2, 2, 2]  # The shuffled array should remain the same
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, expected)
        
    def test_uniform_randomness(self):
        # Test the uniform randomness property of the shuffling algorithm
        
        seed(123) # Set a fixed seed for reproducibility

        # Create a Counter to track the occurrence of permutations
        permutations = Counter()
        num_permutations = 10_000

        for _ in range(num_permutations):
            array = [1, 2, 3]
            self.shuffle_algo.shuffle(array)
            permutation = tuple(array)
            permutations[permutation] += 1

        # Check if all permutations occur with roughly equal probability
        num_possible_permutations = math.factorial(len(array))
        expected_probability = 1 / num_possible_permutations
        tolerance = 0.05  # 5% tolerance for expected probability

        for count in permutations.values():
            probability = count / num_permutations
            self.assertAlmostEqual(probability, expected_probability, delta=tolerance)

class TestsKnuthShuffle(unittest.TestCase):

    def setUp(self):
        self.shuffle_algo = KnuthShuffle()

    def test_shuffle_empty_array(self):
        array = []
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, [])

    def test_shuffle_single_element_array(self):
        array = [42]
        self.shuffle_algo.shuffle(array)
        self.assertEqual(array, [42])

    def test_shuffle_sorted_array(self):
        array = [1, 2, 3, 4, 5]
        seed(1)  # Set a fixed seed for reproducibility
        self.shuffle_algo.shuffle(array)
        self.assertNotEqual(array, [1, 2, 3, 4, 5])

    def test_shuffle_repeated_elements(self):
        array = [1, 1, 2, 2, 3, 3]
        seed(42)  # Set a fixed seed for reproducibility
        self.shuffle_algo.shuffle(array)
        self.assertNotEqual(array, [1, 1, 2, 2, 3, 3])

    def test_shuffle_large_array(self):
        array = list(range(10_000))
        seed(123)  # Set a fixed seed for reproducibility
        self.shuffle_algo.shuffle(array)
        self.assertNotEqual(array, list(range(10_000)))
        
    def test_uniform_randomness(self):
        # Test the uniform randomness property of the shuffling algorithm
        
        seed(123) # Set a fixed seed for reproducibility

        # Create a Counter to track the occurrence of permutations
        permutations = Counter()
        num_permutations = 10_000

        for _ in range(num_permutations):
            array = [1, 2, 3]
            self.shuffle_algo.shuffle(array)
            permutation = tuple(array)
            permutations[permutation] += 1

        # Check if all permutations occur with roughly equal probability
        num_possible_permutations = math.factorial(len(array))
        expected_probability = 1 / num_possible_permutations
        tolerance = 0.05  # 5% tolerance for expected probability

        for count in permutations.values():
            probability = count / num_permutations
            self.assertAlmostEqual(probability, expected_probability, delta=tolerance)

if __name__ == '__main__':
    unittest.main()
