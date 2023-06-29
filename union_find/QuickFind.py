from UnionFind import UnionFind

class QuickFind(UnionFind):
    '''
    '''
    def union(self, element1: int, element2: int) -> int:
        self.validate_element_index(element1, element2)
        
        root1 = self.find(element1)
        root2 = self.find(element2)
        
        if root1 != root2:
            for element in self.parent:
                if self.find(element) == root1:
                    self.parent[element] = root2
                    
            self.sets_count -= 1
            
        return self.sets_count
        