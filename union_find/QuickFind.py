from QuickUnion import QuickUnion

class QuickFind(QuickUnion):
    '''
    '''
    def union(self, node1: int, node2: int) -> int:
        self.validate_node_index(node1, node2)
        
        root1 = self.find(node1)
        root2 = self.find(node2)
        
        if root1 != root2:
            for node in self.parent:
                if self.find(node) == root1:
                    self.parent[node] = root2
                    
            self.sets_count -= 1
            
        return self.sets_count
        