from random import randint, random
class ShuffleSort:
    """
    For a given array:
    1) Generate a random number for each array entry
    2) Sort the items in the array based on their respective random number
    """
    
    def shuffle(self, array: list) -> None:
        n = len(array)
        random_order = sorted([(random(), array_entry) for array_entry in array])
        
        for index, (_, array_entry) in enumerate(random_order):
            array[index] = array_entry


class KnuthShuffle:
    """
    Loop the given array. For each iteration `i`: 
    1) pick a integer `r` between `0` and `i` uniformly at random
    2) Swap `a[i]` and `a[r]`
    """
    def shuffle(self, array: list) -> None:
        n = len(array)
        for i in range(n):
            r = randint(0, i)
            array[i], array[r] = array[r], array[i]
