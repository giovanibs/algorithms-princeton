from QuickUnion import QuickUnion

class WeightedQuickUnionSize(QuickUnion):
    '''
    Implementation of weighted quick union by (root)size
    '''
    def __init__(self, n: int):
        super().__init__(n)
        self.size = [1 for _ in range(n)]
    
    def union(self, node1: int, node2: int) -> int:
        self.validate_node_index(node1, node2)
        
        root1 = self.find(node1)
        root2 = self.find(node2)
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
    
    def union(self, node1: int, node2: int) -> int:
        self.validate_node_index(node1, node2)
        
        root1 = self.find(node1)
        root2 = self.find(node2)
        
        if root1 == root2:
            return self.sets_count
        
        height_root1 = self.height[root1]
        height_root2 = self.height[root2]
        
        if height_root1 == height_root2:
            self.parent[root2] = root1
            self.height[root1] += 1
        elif height_root1 > height_root2:
            self.parent[root2] = root1
        else:
            self.parent[root1] = root2
            
        self.sets_count -= 1
            
        return self.sets_count
    
        
class WeightedQuickUnionHeightPathCompression(WeightedQuickUnionHeight):
    '''
    Implementation of weighted quick union by (root)height with
    path compression
    
    e.g.:
                0  1  2  3  4  5  6  7
    parent = [0, 0, 1, 2, 3, 2, 5, 5]
    
    find(7): 
        1)  root == 0
            
        2.1)    touched_node == 7
        
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 1, 2, 3, 2, 5, 0]
                    
        2.2)    touched_node == 5
        
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 1, 2, 3, 0, 5, 0]
                    
        2.3)    touched_node == 2
        
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 0, 2, 3, 0, 5, 0]
                    
        2.4)    touched_node == 0
                return root
    '''
    def find(self, node):
        self.validate_node_index(node)
        
        root = node
        
        # 1) find the root
        while root != self.parent[root]:
            root = self.parent[root]
        
        # 2) set each touched node (from `node` to `root`)
        # to point to `root`
        touched_node = node
        while touched_node != root:
            self.parent[touched_node], touched_node = \
                root, self.parent[touched_node]
        
        return root

    
class WeightedQuickUnionHeightPathCompression2(WeightedQuickUnionHeight):
    '''
    Implementation of weighted quick union by (root)height with
    path compression
    
    e.g.:
                  0  1  2  3  4  5  6  7
        parent = [0, 0, 1, 2, 3, 4, 5, 6]
        
        find(7): 
            1)  root = 7
                grandparent = 5
                
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 1, 2, 3, 4, 5, 5]
                
            2)  root = 5
                grandparent = 3
                
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 1, 2, 3, 3, 5, 5]
                
            3)  root = 3
                grandparent = 1
                
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 1, 1, 3, 3, 5, 5]
                
            4)  root = 1
                grandparent = 0
                
                node      0  1  2  3  4  5  6  7
                parent = [0, 0, 1, 1, 3, 3, 5, 5]
                
            5)  root = 0
                root == parent[root]
                return root
    '''
    def find(self, node):
        self.validate_node_index(node)
        
        root = node
        
        while root != self.parent[root]:
            # set the node parent to it's grandparent
            grandparent = self.parent[self.parent[root]]
            self.parent[root] = grandparent
            root = self.parent[root]
    
        return root
    