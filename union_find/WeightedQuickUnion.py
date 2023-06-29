from QuickUnion import QuickUnion

class WeightedQuickUnionSize(QuickUnion):
    '''
    Implementation of weighted quick union by (root)size
    '''
    def __init__(self, n: int):
        super().__init__(n)
        self.size = [1 for _ in range(n)]
    
    def union(self, element1: int, element2: int) -> int:
        self.validate_element_index(element1, element2)
        
        root1 = self.find(element1)
        root2 = self.find(element2)
        size_root1 = self.size[root1]
        size_root2 = self.size[root2]
        
        if root1 == root2:
            return self.sets_count
        
        if size_root1 >= size_root2:
            self.parent[root2] = root1
            self.size[root1] += size_root2
        else:
            self.parent[root1] = root2
            self.size[root2] += size_root1
            
        self.sets_count -= 1
            
        return self.sets_count

        
class WeightedQuickUnionHeight(QuickUnion):
    '''
    Implementation of weighted quick union by (root)height
    '''
    def __init__(self, n: int):
        super().__init__(n)
        self.height = [0 for _ in range(n)]
    
    def union(self, element1: int, element2: int) -> int:
        self.validate_element_index(element1, element2)
        
        root1 = self.find(element1)
        root2 = self.find(element2)
        height_root1 = self.height[root1]
        height_root2 = self.height[root2]
        
        if root1 == root2:
            return self.sets_count
        
        if height_root1 == height_root2:
            self.parent[root2] = root1
            self.height[root1] += 1
        elif height_root1 > height_root2:
            self.parent[root2] = root1
        else:
            self.parent[root1] = root2
            
        self.sets_count -= 1
            
        return self.sets_count
        