class MergeSort:
    """
    Given an array `a`, these are the basic steps:

    1) Divide array in two halves:
            - left half:  `a[lo:mid]`
            - right half: `a[mid:hi]`

    2) Recursively sort each half
    3) Merge the two halves
    """

    def merge(self, a: list, lo, mid, hi):
        """
        Abstract in-place merge: merge two sorted subarrays into a sorted array.

        Using 3 pointers: `merged`, `left`, `right`:
        - For each position `a[merged]`:
                - `a[merged] = min(aux[left], aux[right])`
                - increment the respective pointer.

        - If any of the subarrays are exhausted, populate the remaining positions
        of `a` with the remaining items of the remaining subarray
        """

        # auxiliary array
        aux = a.copy()
        left, right = lo, mid

        for merged_index in range(len(a)):
            # if any subarray is exhausted
            if left == mid or right == hi:
                # populate the remaining positions with
                # the remaining subarray's remaining items
                a[merged_index:] = aux[left:mid] or aux[right:hi]
                break

            if aux[left] <= aux[right]:
                a[merged_index] = aux[left]
                left += 1
            else:
                a[merged_index] = aux[right]
                right += 1
