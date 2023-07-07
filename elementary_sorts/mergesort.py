class MergeSort:
    """
    Given an array `a`, these are the basic steps:

    1) Divide array in two halves:
            - left half:  `a[lo, mid)`
            - right half: `a[mid, hi)`

    2) Recursively sort each half
    3) Merge the two halves
    """

    def sort(self, a):
        n = len(a)
        self._sort(a, lo=0, hi=n)

    def _sort(self, a, lo, hi) -> None:
        # 1) Base case: If the subarray size is 0 or 1,
        # it is already sorted.
        if (hi - lo) <= 1:
            return

        # 2) Recursive step:
        #   2.1) compute mid = (hi + lo)//2
        mid = (lo + hi) // 2

        #   2.2) sort (recursively) the two subarrays
        self._sort(a, lo=lo, hi=mid)  # a[lo:mid)
        self._sort(a, lo=mid, hi=hi)  # a[mid:hi)

        #   3.1) merge them.
        self.merge(a, lo, mid, hi)

    def merge(self, a, lo, mid, hi):
        """
        Abstract in-place merge: merge two sorted subarrays into a sorted array.

        Using 3 pointers: `merged`, `left`, `right`:
        - For each position `a[merged]`:
                - `a[merged] = min(aux[left], aux[right])`
                - increment the respective pointer.

        - If any of the subarrays are exhausted, populate the remaining positions
        of `a` with the remaining items of the remaining subarray
        """
        # this check is redundant, since it is already checked in the `_sort` method.
        if (hi - lo) <= 1:
            return

        # assert that both subarrays are already sorted
        assert a[lo:mid] == sorted(a[lo:mid]), "Left subarray not sorted!"
        assert a[mid:hi] == sorted(a[mid:hi]), "Right subarray not sorted!"

        # IMPROVEMENT: check if the array is already sorted
        if a[mid - 1] <= a[mid]:
            return

        # auxiliary array
        aux = a.copy()
        left, right = lo, mid

        for merged_index in range(lo, hi):
            # if any subarray is exhausted
            if left == mid or right == hi:
                # populate the remaining positions with
                # the remaining subarray's remaining items
                a[merged_index:hi] = aux[left:mid] or aux[right:hi]
                break

            if aux[left] <= aux[right]:
                a[merged_index] = aux[left]
                left += 1
            else:
                a[merged_index] = aux[right]
                right += 1
