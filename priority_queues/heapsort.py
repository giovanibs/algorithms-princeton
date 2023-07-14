from binary_heap import BinaryHeap
from ordinal_list import OrdinalList


class HeapSort(BinaryHeap):
    def sort(self, furthest_k=None):
        root = 1
        furthest_k = self._validate_furthest_k(root, furthest_k)

        #  heapify phase
        k = furthest_k // 2
        while k >= 1:
            self._sink_down_item_at(k, furthest_k - 1)
            k -= 1

        # sortdown phase
        while furthest_k > 1:
            self._swap_items_at(root, furthest_k)
            self._sink_down_item_at(root, furthest_k - 1)
            furthest_k -= 1

    def _sink_down_item_at(self, k, furthest_k=None):
        """
        ### Top-down heapify: `sink`

        If by any chance the parent's key becomes smaller than any of it's
        children, apply `sink` method:

        1) Exchange key in parent with key in largest child (to make sure the
        new parent is greater than both children).
        2) Update `k`
        3) Repeat until until we reach a node with both children smaller, or
        the bottom (or the `furthest_k`).
        """
        self._validate_keys(k)

        furthest_k = self._validate_furthest_k(k, furthest_k)

        while 2 * k <= furthest_k:  # while item at `k` has at least 1 child
            l = self._get_largest_child(k, furthest_k)
            if l is not None and self._a[k] < self._a[l]:
                self._swap_items_at(k, l)
                k = l
            else:
                break

    def _validate_furthest_k(self, k, furthest_k):
        if furthest_k is None:
            return len(self)
        else:
            if (furthest_k < k) or (furthest_k > len(self)):
                raise ValueError(" 1 <= `k` <= `furthest_k` <= len(a) !")
        return furthest_k

    def _get_largest_child(self, k, furthest_k=None):
        """
        Returns the INDEX of largest item between bh[k*2] and bh[k*2+1].
        """
        furthest_k = self._validate_furthest_k(k, furthest_k)

        if 2 * k > furthest_k:  # item at `k` has NO child
            return None
        elif 2 * k == furthest_k:  # item at `k` has only 1 child
            return 2 * k
        elif self._a[2 * k] >= self._a[2 * k + 1]:  # item at 2*k is larger
            return 2 * k
        else:  # item at 2*k+1 is larger
            return 2 * k + 1


#############
### TESTS ###
#############
from binary_heap import TestsBinaryHeap
from random import shuffle

class TestsHeapSort(TestsBinaryHeap):
    def setUp(self) -> None:
        self.BinaryHeap = HeapSort
        self.bh = self.BinaryHeap()

    def test_sort_empty_heap(self):
        self.bh = self.BinaryHeap()
        self.bh.sort()
        result_a = self.bh.a
        expected_a = []
        self.assertEqual(expected_a, result_a)

    def test_sort_heap_size_1(self):
        items = ["one"]
        self.bh = self.BinaryHeap(items)
        self.bh.sort()
        result_a = self.bh.a
        expected_a = ["one"]
        self.assertEqual(expected_a, result_a)

    def test_sort_subarray(self):
        items = [5, 4, 3, 2, 1]
        self.bh = self.BinaryHeap(items)
        result_a = self.bh.a
        expected_a = [5, 4, 3, 2, 1]
        self.assertEqual(expected_a, result_a)

        self.bh.sort(furthest_k=1)
        result_a = self.bh.a
        expected_a = [5, 4, 3, 2, 1]
        self.assertEqual(expected_a, result_a)

        self.bh.sort(furthest_k=2)
        result_a = self.bh.a
        expected_a = [4, 5, 3, 2, 1]
        self.assertEqual(expected_a, result_a)

        self.bh.sort(furthest_k=3)
        # heapified a = [5, 4, 3, 2, 1]
        result_a = self.bh.a
        expected_a = [3, 4, 5, 2, 1]
        self.assertEqual(expected_a, result_a)

        self.bh.sort(furthest_k=4)
        result_a = self.bh.a
        expected_a = [2, 3, 4, 5, 1]
        self.assertEqual(expected_a, result_a)

    def test_sort_big_array(self):
        n = 10_000
        shuffle(items := list(range(n)))
        self.bh = self.BinaryHeap(items)
        self.bh.sort()
        expected_a = sorted(items)
        self.assertEqual(expected_a, self.bh.a)
    
    def test_sort_random_cases(self):
        for n in range(100):
            shuffle(items := list(range(n)))
            self.bh = self.BinaryHeap(items)
            self.bh.sort()
            expected_a = sorted(items)
            self.assertEqual(expected_a, self.bh.a)

    def test_sink_down_furthest_k(self):
        self.bh._a = OrdinalList([1, 2, 3, 4, 5])

        self.bh._sink_down_item_at(1, 2)
        expected_a = [2, 1, 3, 4, 5]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(1, 2)
        expected_a = [2, 1, 3, 4, 5]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(1, 3)
        expected_a = [3, 1, 2, 4, 5]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(1, 3)
        expected_a = [3, 1, 2, 4, 5]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(2, 4)
        expected_a = [3, 4, 2, 1, 5]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(2, 4)
        expected_a = [3, 4, 2, 1, 5]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(2, 5)
        expected_a = [3, 5, 2, 1, 4]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(1, 4)
        expected_a = [5, 3, 2, 1, 4]
        self.assertEqual(expected_a, self.bh.a)

        self.bh._sink_down_item_at(2, 5)
        expected_a = [5, 4, 2, 1, 3]
        self.assertEqual(expected_a, self.bh.a)

        # ValueError
        self.bh._a = OrdinalList([3, 2, 1])
        with self.assertRaises(ValueError):
            self.bh._sink_down_item_at(1, 0)
        with self.assertRaises(ValueError):
            self.bh._sink_down_item_at(1, 6)
        with self.assertRaises(ValueError):
            self.bh._sink_down_item_at(3, 2)

    def test_get_largest_child(self):
        self.bh = self.BinaryHeap([1, 2, 3, 4, 5])
        # expected = [5, 4, 2, 1, 3]
        # keys        1  2  3  4  5
        largest_k = self.bh._get_largest_child(1)
        expected_k = 2
        self.assertEqual(expected_k, largest_k)

        largest_k = self.bh._get_largest_child(1, 1)
        expected_k = None
        self.assertEqual(expected_k, largest_k)

        largest_k = self.bh._get_largest_child(2)
        expected_k = 5
        self.assertEqual(expected_k, largest_k)

        largest_k = self.bh._get_largest_child(2, 3)
        expected_k = None
        self.assertEqual(expected_k, largest_k)

        largest_k = self.bh._get_largest_child(2, 4)
        expected_k = 4
        self.assertEqual(expected_k, largest_k)

        largest_k = self.bh._get_largest_child(2, 5)
        expected_k = 5
        self.assertEqual(expected_k, largest_k)

        largest_k = self.bh._get_largest_child(3)
        expected_k = None
        self.assertEqual(expected_k, largest_k)
