class SelectionSort:
    """
    Given a list (size `n`), starting from the position in the list:
        1) start at the first position
        2) select the smallest remaining item (from `pointer1` to `n-1`)
        3) swap smallest item with pointer1
        4) next list position and repeat the process
    """
    
    def sort(self, array):
        
        for current_index, current in enumerate(array):
            
            smallest = current
            smallest_index = current_index
            
            # search for the smallest remaining item 
            remaining_items = array[current_index:]
            
            for item_index, item in enumerate(remaining_items):
                if item < smallest:
                    smallest = item
                    smallest_index = item_index + current_index
            
            # after selecting the smallest, swap the current with the new smallest
            if smallest < current:
                array[current_index], array[smallest_index] = \
                    array[smallest_index], array[current_index]
        
