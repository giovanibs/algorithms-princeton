try:
    from ..binary_search_trees.bst2 import BinarySearchTree as BST
except:
    import os
    import sys
    package_path = os.path.abspath('../../') # algorithms-princeton
    sys.path.append(package_path)
    from symbol_tables.binary_search_trees.bst2 import BinarySearchTree as BST

class RedBlackBST(BST):
    """
    # Left-leaning red-black BST
    
    Implementation of a symbol table using a left-leaning
    red-black BST.
    
    The basic idea behind red-black BSTs is to encode 2-3 trees
    by starting with standard BSTs (which are made up of 2-nodes)
    and adding extra information to encode 3-nodes.
    
    We think of the links as being of two different types:
        - red links: bind together two 2-nodes to represent 3-nodes
        - black links: bind together the 2-3 tree.
    
    Specifically, we represent 3-nodes as two 2-nodes connected
    by a single red link that leans left. We refer to BSTs that
    represent 2-3 trees in this way as red-black BSTs.

    One advantage of using such a representation is that it allows us
    to use our get() code for standard BST search without modification. 
    
    ### Color representation
    
    Since each node is pointed to by precisely one link (from its parent),
    we encode the color of links in nodes, by adding a boolean instance
    variable color to our Node data type, which is true if the link from
    the parent is red and false if it is black.
    
    By convention, null links are black.
    
    ### Rotations
    
    The implementation that we will consider might allow right-leaning
    red links or two red-links in a row during an operation, but it
    always corrects these conditions before completion, through
    judicious use of an operation called rotation that switches
    orientation of red links.
    
    First, suppose that we have a right-leaning red link that needs to be
    rotated to lean to the left. This operation is called a left rotation.
    
    Implementing a right rotation that converts a left-leaning red link
    to a right-leaning one amounts to the same code, with left and right
    interchanged.
    
    ### Flipping colors
    
    The implementation that we will consider might also allow a black
    parent to have two red children. The color flip operation flips the
    colors of the the two red children to black and the color of the
    black parent to red.
    """
    RED = True
    BLACK = False
    
    def __init__(self):
        super().__init__()
    
    class _Node:
        def __init__(self, key, val, color=None):
            
            self.assert_color(color)
            self.color = color or RedBlackBST.BLACK
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.size = 1

        def assert_color(self, color):
            if color not in [None, RedBlackBST.BLACK, RedBlackBST.RED]:
                raise ValueError("Invalid color value.")
            
            
if __name__ == "__main__":
    bst = RedBlackBST()
    node = bst._Node(1, 1)
    print(node.color)