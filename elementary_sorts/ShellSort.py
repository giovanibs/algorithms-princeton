class ShellSort:
    """
    This code implements the Shell sort algorithm,
    which is an extension of the insertion sort algorithm
    
    The algorithm uses a sequence of `gap` sizes to perform
    multiple steps over the array. It starts with the largest
    `gap` size and gradually reduces the `gap` until it reaches `1`
    and the array is fully sorted.
    
    At each step, it performs insertion sort on subarrays
    defined by the current `gap` size.
    
    This helps move smaller elements towards the beginning
    of the array faster, improving the overall sorting efficiency.
    """
    def sort(self, array):
        
        n = len(array)
        
        gap_sequence = self.knuths_sequence(n)
            
        # Iterate over the gap sequence, starting from the largest value
        for gap in gap_sequence[::-1]:
            
            # Perform insertion sort with the current gap
            for i in range(gap, n):
                for j in range(i, 0, -gap):
                    
                    # swap elements if they are in the wrong order
                    if array[j] < array[j-gap]:
                        array[j], array[j-gap] = array[j-gap], array[j]

    def knuths_sequence(self, n: int) -> list:
        """
        Generates a gap sequence using the Knuth's formula:
            `gap = 3*gap + 1`
        """
        gap = 1
        gap_sequence = []
        while gap < n//3:
            gap_sequence.append(gap)
            gap = 3*gap + 1
        return gap_sequence