import graphviz
from random import random # used with graphviz

class RedBlackBST:
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
    NOT_BST = "Not in symmetric order"
    NOT_23TREE = "Not a 2-3 tree"
    NOT_BALANCED = "Not balanced"
    NOT_SIZE_CONSISTENT = "Subtree counts not consistent"
    RED_ROOT = "BST's root cannot be RED"

    def __init__(self):
        self.root = None

    class _Node:
        def __init__(self, key, val, size=1, color=None):
            self.assert_color(color)
            self.color = RedBlackBST.RED if color is None else color
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.size = size

        def assert_color(self, color):
            if color not in [None, RedBlackBST.BLACK, RedBlackBST.RED]:
                raise ValueError("Invalid color value.")

        def __repr__(self) -> str:
            return f"_Node(key={self.key}, val={self.val}, size={self.size}, color={'RED' if self.color else 'BLACK'})"
    
        def __eq__(self, other):
            if isinstance(other, RedBlackBST._Node):
                return self.key == other.key \
                    and self.val == other.val \
                    and self.size == other.size \
                    and self.color == other.color
            else:
                raise TypeError
    # ------------------------------------------------
    #   New methods/properties.
    # ------------------------------------------------
    def is_red(self, node):
        """
        Is `node` RED?
        By default, null links are BLACK.
        """
        if node is None:
            return False

        return node.color

    def _rotate_left(self, subtree):
        """
        Orient a (temporarily) right-leaning red link to lean left.
        
        (a) save `red_right` node;
        
        (b) move nodes between `root` and `red_right`,
        i.e. `red_right.left`, to `subtree.right`;
        
        (c) set `red_right` left link to node at `root`
        
        (d) update colors
        
        (e) update sizes
        
        (f) return the new subtree root
        """
        right_node = subtree.right           # (a)
        subtree.right = right_node.left      # (b)
        right_node.left = subtree            # (c)
        # (d)
        right_node.color = subtree.color
        subtree.color = RedBlackBST.RED
        # (e)
        right_node.size = subtree.size
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        # (f)
        return right_node

    def _rotate_right(self, subtree):
        """
        Orient a left-leaning link to the left.
        
        (a) save `left_node` node;
        
        (b) move nodes between `left_node` and `subtree`,
        i.e. `left_node.right`, to `subtree.left`;
        
        (c) set `left_node`'s right link to node at `root`
        
        (d) update colors
        
        (e) update sizes
        
        (f) return the new subtree root
        
                        (subtree)
                       /         \
            (left_node)
        """
        left_node = subtree.left            # (a)
        subtree.left = left_node.right      # (b)
        left_node.right = subtree           # (c)
        # (d)
        left_node.color = subtree.color
        subtree.color = RedBlackBST.RED
        # (e)
        left_node.size = subtree.size
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        # (f)
        return left_node

    def _flip_colors(self, subtree):
        """
        Flip the colors of a node and its two children.
        `subtree` must have opposite color of its two children.
        """
        if subtree is None or subtree.left is None or subtree.right is None:
            return
        
        if (subtree.left.color != subtree.right.color) or \
            (subtree.color == subtree.left.color):
            return        
        
        subtree.color       = not subtree.color
        subtree.left.color  = not subtree.left.color
        subtree.right.color = not subtree.right.color
        
        return True

    def _move_red_left(self, subtree):
        """
        Assuming that `subtree` is red and both `subtree.left`
        and `subtree.left.left` are black, make `subtree.left`
        or one of its children red.
        """
        if subtree is None:
            return subtree
        
        if not subtree.color:
            return subtree
        
        if self.is_red(subtree.left) \
                and self.is_red(subtree.left.left):
            return subtree
        
        self._flip_colors(subtree)
        
        # right subtree is red now, gotta fix it
        if self.is_red(subtree.right.left):
            subtree.right = self._rotate_right(subtree.right)
            subtree = self._rotate_left(subtree)
            self._flip_colors(subtree)
        
        return subtree

    def _move_red_right(self, subtree):
        """
        Assuming that `subtree` is red and both `subtree.right`
        and `subtree.right.left` are black, make `subtree.right`
        or one of its children red.
        """
        if subtree is None:
            return subtree
        
        if not self.is_red(subtree):
            return subtree
        
        if self.is_red(subtree.right) \
                and self.is_red(subtree.right.left):
            return subtree
        
        self._flip_colors(subtree)
        
        if self.is_red(subtree.left.left):
            subtree = self._rotate_right(subtree)
            self._flip_colors(subtree)
        
        return subtree

    def restore_balance(self, subtree):
        # right-leaning red link
        if self.is_red(subtree.right) and not self.is_red(subtree.left):
            subtree = self._rotate_left(subtree)
        
        # two consecutives left-leaning red links
        if self.is_red(subtree.left) and self.is_red(subtree.left.left):
            subtree = self._rotate_right(subtree)
        
        # two red children
        if self.is_red(subtree.left) and self.is_red(subtree.right):
            self._flip_colors(subtree)
        
        # update sizes
        subtree.size = 1 + self._size(subtree.left) + self._size(subtree.right)
        
        return subtree
        
    # ------------------------------------------------
    #   Check integrity of red-black tree data structure.
    # ------------------------------------------------
    def assert_integrity(self):
        """
        Checks for:
        - symmetric order
        - 2-3 tree
        - balanced tree
        - subtree size consistency
        """
        assert self.is_BST,                 RedBlackBST.NOT_BST
        assert self.is_23tree,              RedBlackBST.NOT_23TREE
        assert self.is_balanced,            RedBlackBST.NOT_BALANCED
        assert self.is_size_consistent,     RedBlackBST.NOT_SIZE_CONSISTENT
        assert not self.is_red(self.root),  RedBlackBST.RED_ROOT
        
        return True
        
    @property
    def is_BST(self):
        """
        Does this binary tree satisfy symmetric order?
        Note: this test also ensures that data structure is a binary
        tree since order is strict.
        """
        return self._is_BST(self.root, None, None)
        
    def _is_BST(self, subtree, lo, hi):
        """
        Is the tree rooted at `subtree` a BST with all keys strictly
        between `lo` and `hi` (both inclusive)?
        If `lo` or `hi` is null, treat as empty constraint.
        """
        if subtree is None:
            return True
        
        this_key = subtree.key
        
        if (lo is not None) and (this_key <= lo):
            return False
        
        if (hi is not None) and (this_key >= hi):
            return False
        
        # key == 2
        return self._is_BST(subtree.left, lo=lo, hi=this_key) \
            and self._is_BST(subtree.right, lo=this_key, hi=hi)
    
    @property
    def is_size_consistent(self):
        """
        Returns true if the subtree count, i.e. its size, is
        consistent in the data structure rooted at that node,
        false otherwise.
        """
        return self._is_size_consistent(self.root)
    
    def _is_size_consistent(self, subtree):
        if subtree is None:
            return True
        
        subtree_size = self._size(subtree)

        expected = (
            1
            + self._size(subtree.left)
            + self._size(subtree.right)
        )
        if subtree_size != expected:
            return False
        
        return self._is_size_consistent(subtree.left) and \
            self._is_size_consistent(subtree.right)
    
    @property
    def is_23tree(self):
        """
        Checks whether the tree is a 2-3 tree:
        - No right-leaning red link;
        - AND no node is connected to two red links.
        """
        return self._is_23tree(self.root)
    
    def _is_23tree(self, subtree):
        """
        - No right-leaning red link;
        - AND no node is connected to two red links.
        """
        if subtree is None:
            return True
        
        # no red right links
        if self.is_red(node=subtree.right):
            return False
        
        # no node is connected to two red links
        # PS.: exempt root because it should never be RED
        if (subtree is not self.root) and \
            self.is_red(subtree) and \
                self.is_red(subtree.left):
            return False
        return self._is_23tree(subtree.left) and self._is_23tree(subtree.right)
    
    @property
    def is_balanced(self):
        """
        A perfectly balanced red-black-tree is one whose
        null links are all the same distance from the root,
        as any 2-3-tree.
        """
        black = 0 # number of black links on path from root to min
        subtree = self.root
        
        # min path as reference for number of black links
        while subtree is not None:
            if not self.is_red(subtree):
                black += 1
            subtree = subtree.left
        
        # check starting from root
        return self._is_balanced(self.root, black)
    
    def _is_balanced(self, subtree, black):
        """
        - Every path from root to null link has same number
        of black links.
        - Never two red links in-a-row.
        """
        # hit a leaf, aka null link
        if subtree is None:
            return black == 0
        
        # decrease reference count
        if not self.is_red(subtree):
            black -= 1
        
        # recursively check left and right subtree
        return self._is_balanced(subtree.left, black) and \
            self._is_balanced(subtree.right, black)
        
    # ------------------------------------------------
    #   Overridden BST methods/properties.
    # ------------------------------------------------
    def put(self, k, v):
        self.root = self._put(k, v, self.root)
        self.root.color = RedBlackBST.BLACK

    def _put(self, k, v, subtree):
        # -------------------------------------------------
        # (1) puts new node just like a normal BST
        if subtree is None:
            return self._Node(k, v)
        
        if k == subtree.key:
            subtree.val = v
        
        elif k < subtree.key:
            subtree.left = self._put(k, v, subtree.left)
        
        else: # k > subtree.key
            subtree.right = self._put(k, v, subtree.right)
        
        # -------------------------------------------------
        # (2) fix-up color links if necessary
        return self.restore_balance(subtree)

    def del_min(self):
        """
        Removes the smallest key from the BST.
        """
        if self.is_empty:
            raise KeyError("BST is empty.")
        
        # if both children of root are black, set root to red to
        # move_red_left in the future
        if not self.is_red(self.root.left) \
                and not self.is_red(self.root.right):
            self.root.color = RedBlackBST.RED

        self.root = self._del_min(self.root);
        
        if not self.is_empty:
            # restore root BACK to BLACK
            self.root.color = RedBlackBST.BLACK;
        
    def _del_min(self, subtree):
        """
        """
        # if given node is the smallest
        if subtree.left is None:
            # replace the node with its right link
            return None
        
        if not self.is_red(subtree.left) and not self.is_red(subtree.left.left):
            subtree = self._move_red_left(subtree)
        
        subtree.left = self._del_min(subtree.left)
        
        return self.restore_balance(subtree)
    
    def del_max(self):
        if self.is_empty:
            raise KeyError("BST is empty.")
        
        # if both children of root are black, set root to red
        if not self.is_red(self.root.left) and not self.is_red(self.root.right):
            self.root.color = RedBlackBST.RED

        self.root = self._del_max(self.root)
        
        if not self.is_empty:
            # restore root BACK to BLACK
            self.root.color = RedBlackBST.BLACK

    def _del_max(self, subtree):
        if self.is_red(subtree.left):
            subtree = self._rotate_right(subtree)
            
        if subtree.right is None:
            return None
        
        if not self.is_red(subtree.right) and \
                not self.is_red(subtree.right.left):
            subtree = self._move_red_right(subtree)
            
        subtree.right = self._del_max(subtree.right)
        
        return self.restore_balance(subtree)

    def del_key(self, k):
        if self.is_empty:
            raise KeyError("BST is empty.")
        
        if not self.contains(k):
            raise KeyError(f"Given key `{k}` not in BST.")
        
        # if both children of root are black, set root to red
        if not self.is_red(self.root.left) and not self.is_red(self.root.right):
            self.root.color = RedBlackBST.RED
        
        self.root = self._del_key(k, self.root)
        
        if not self.is_empty:
            # restore root BACK to BLACK
            self.root.color = RedBlackBST.BLACK

    def _del_key(self, k, subtree):
        """
        Recursive function to delete a key from the red-black tree.

        Args:
            key: The key to be deleted.
            subtree: The current subtree being processed.

        Returns:
            The updated subtree after deletion.
        """
        
        ########################
        ### DELETE FROM LEFT ###
        ########################
        if k < subtree.key:
            
            # Check if the left child is a 2-node
            # (black node with two black children).
            if not self.is_red(subtree.left) and \
                    not self.is_red(subtree.left.left):
                
                # Convert the 2-node into a 3-node or 4-node
                # by borrowing from the right sibling.
                subtree = self._move_red_left(subtree)
            
            # Continue the search in the left subtree.
            subtree.left = self._del_key(k, subtree.left)
            
            # Rebalance the tree after deletion
            return self.restore_balance(subtree)
        
        #########################
        ### DELETE FROM RIGHT ###
        #########################
        
        # If the left child is red, do a right rotation
        # to make it easier to delete the key.
        if self.is_red(subtree.left):
            subtree = self._rotate_right(subtree)
        
        # If the key matches the current node's key and the
        # right child is None, it means we found the node
        # to be deleted. Return None to remove it.
        if k == subtree.key and subtree.right is None:
            return None
        
        # Check if the right child is a 2-node
        # (black node with two black children).
        if not self.is_red(subtree.right) and not self.is_red(subtree.right.left):
            
            # Convert the 2-node into a 3-node or 4-node
            # by borrowing from the left sibling.
            subtree = self._move_red_right(subtree)
        
        # If the key matches the current node's key, replace
        # it with the minimum key from the right subtree.
        if k == subtree.key:
            aux = self._min(subtree.right)
            subtree.key = aux.key
            subtree.val = aux.val
            subtree.right = self._del_min(subtree.right)
            
        # Continue the search in the right subtree.
        else:
            subtree.right = self._del_key(k, subtree.right)
        
        # Rebalance the tree after deletion.
        return self.restore_balance(subtree)
        
    # ------------------------------------------------
    #   Not overridden BST methods/properties
    # ------------------------------------------------
    @property
    def is_empty(self):
        return self.root is None
    
    def contains(self, k):
        """
        Does this BST contain the given key?
        """
        return self.get(k) is not None
        
    def size(self):
        """
        Returns the size of the BST.
        """
        return self._size(self.root)
            
    def _size(self, subtree):
        """
        Returns the size of the BST rooted at `subtree`.
        """
        if subtree is None:
            return 0
        else:
            return subtree.size
 
    def get(self, k):
        if self.is_empty:
            return None
        
        return self._get(k, self.root)
    
    def _get(self, k, subtree):
        """
        A recursive algorithm to search for a key in a BST and return
        its value `val`.
        
        For a given key, `k`, and a given root of a subtree, `subtree`:
        
        1) If the subtree is empty, we have a search miss.
        
        2) If not, starting from the `subtree`, we compare `k`
        with the `subtree`'s key: 
            
            - If `k == subtree.key`, we have a search hit;
            
            - Otherwise, we search (recursively) in the appropriate
            subtree until `k` is found or we hit an empty subtree:
                
                - `k < subtree.key`: search in the left subtree
                
                - `k > subtree.key`: search in the right subtree
        """
        if subtree is None:
            return None
        
        if k == subtree.key:
            return subtree.val
        
        if k < subtree.key:
            return self._get(k, subtree.left)
        
        if k > subtree.key:
            return self._get(k, subtree.right)
    
    def min(self):
        """
        Returns the smallest key in the BST.
        """
        smallest = self._min(self.root)
        if smallest is None:
            return None
        else:
            return smallest.key 
        
    def _min(self, subtree):
        """
        If the subtree is None, then there is no smallest key.
        
        If the left link of the subtree is null, the smallest
        key in this subtree is the key at the subtree root;
        
        Otherwise, the smallest key in the subtree is the
        smallest key in the subtree rooted at the left link.
        """
        if subtree is None:
            return None
        
        if subtree.left is None:
            return subtree
        else:
            return self._min(subtree.left)
        
    def max(self):
        """
        Returns the LARGEST key in the BST.
        """
        return self._max(self.root)
        
    def _max(self, subtree):
        """
        If the subtree is None, then there is no largest key.
        
        If the right link of the subtree is null, the largest
        key in this subtree is the key at the subtree root;
        
        Otherwise, the largest key in the subtree is the
        largest key in the subtree rooted at the right link.
        """
        if subtree is None:
            return None
        
        if subtree.right is None:
            return subtree.key
        else:
            return self._max(subtree.right)

    def floor(self, k):
        """
        Returns the LARGEST key in the BST that is equal to or
        smaller than the given key.
        """
        return self._floor(k, self.root)
        
    def _floor(self, k, subtree):
        """
        Compare `k` with key of the root of the `subtree`:
        
        (a) If subtree is empty, return None.
        
        (b) If `k == subtree.key`, then `k` is the floor.
        
        (c) If `k < subtree.key`, then the floor of key **MUST**
        be in the left subtree.
        
        (d) If `k > subtree.key`, then the floor of key **COULD**
        be in the right subtree. That is, is there a key smaller
        than or equal to `k` in the right subtree?
            - if yes, recursively find and return it;
            - if not, or if `k` is equal to the key at the root,
            then `subtree.key` is the floor of `k`.
        """
        # (a)
        if (subtree is None) or (k < self._min(subtree).key):
            return None
        
        # (b)
        if k == subtree.key:
            return subtree.key
        
        # (c) MUST be in the left subtree
        if k < subtree.key:
            return self._floor(k, subtree.left)
        
        # (d) COULD be in the right subtree
        if k > subtree.key:
            floor = self._floor(k, subtree.right)
            
            # if not
            if floor is None:
                return subtree.key
            else:
                return floor
    
    def ceiling(self, k):
        """
        Returns the SMALLEST key in the BST that is greater than
        or equal to the given key `k`.
        """
        return self._ceiling(k, self.root)
        
    def _ceiling(self, k, subtree):
        """
        Compare `k` with key of the root of the `subtree`:
        
        (a) If subtree is empty, return None.
        
        (b) If `k == subtree.key`, then `k` is the ceiling.
        
        (c) If `k > subtree.key`, then the ceiling of `k` **MUST**
        be in the right subtree: recursively look for it.
        
        (d) If `k < subtree.key`, then the ceiling of key **COULD**
        be in the left subtree. That is, is there a key larger
        than or equal to `k` in the left subtree?
            - if yes, recursively find and return it;
            - if not, or if `k` is equal to the key at the root,
            then `subtree.key` is the ceiling of `k`.
        """
        # (a)
        if (subtree is None) or (k > self._max(subtree)):
            return None
        
        # (b)
        if k == subtree.key:
            return subtree.key
        
        # (c) MUST be in the right subtree. Find and return it.
        if k > subtree.key:
            return self._ceiling(k, subtree.right)
        
        # (d) COULD be in the left subtree
        if k < subtree.key:
            ceiling = self._ceiling(k, subtree.left)
            
            # if it is not in the left subtree
            if ceiling is None:
                return subtree.key
            else:
                return ceiling

    def select(self, r):
        """
        Returns the key of rank `r`, i.e. the key such that
        precisely `r` other keys in the BST are smaller.
        
        0 <= r < size(BST)
        """
        if r < 0 or r >= self.size():
            raise ValueError
        
        return self._select(r, self.root)
    
    def _select(self, r, subtree):
        """
        For the given rank `r` (0<= r < subtree size) and a
        subtree root `subtree`:
        
        (a) If `r == size(subtree.left)`, we return the key
        at the subtree root;
        
        (b) If `r < size(subtree.left)`, we look (recursively)
        for the key of rank `r` in the left subtree;
        
        (c) If `r > size(subtree.left)`, we look (recursively)
        for the key of rank (r - size(subtree.left) - 1)
        in the right subtree.
        """
        left_size = self._size(subtree.left)
        # (a)
        if r == left_size:
            return subtree.key
        # (b)
        elif r < left_size:
            return self._select(r, subtree.left)
        # (c)
        else: # r > left_size:
            new_r = r - left_size - 1
            return self._select(new_r, subtree.right)

    def rank(self, k):
        """
        Returns the rank (0 <= rank < BST size) of the given key `k`.
        In other words, the number of keys in the symbol table
        strictly less than `k`.
        """
        if not self.contains(k):
            raise KeyError(f"`{k}` not in the BST!")
        
        return self._rank(k, self.root)
        
    def _rank(self, k, subtree):
        """
        If `k == subtree.key`, we return the number of keys in the
        left subtree;
        
        if `k < subtree.key`, we recursively look for the rank of
        the key in the left subtree;
        
        if `k > subtree.key`, we return the sum of:
            + `1` (to count the key at the root)
            + left subtree size
            + (recursively) the rank of the key in the right subtree.
        """
        if k == subtree.key:
            return self._size(subtree.left)
        
        elif k < subtree.key:
            return self._rank(k, subtree.left)
        
        else:   # k > subtree.key
            return 1 + self._size(subtree.left) + self._rank(k, subtree.right)

    def keys(self, lo=None, hi=None):
        """
        Returns all keys in the BST between `lo` (inclusive) and
        `hi` (also inclusive) in ascending order.
        """
        if lo is None:
            lo = self.min()
        if hi is None:
            hi = self.max()
            
        q = [] # queue
            
        self._in_order(self.root, lo, hi, q)
        
        return q
    
    def _in_order(self, subtree, lo, hi, q):
        """
        Traverse left subtree.
        Enqueue key.
        Traverse right subtree.
        """
        if subtree is None:
            return
        
        if lo < subtree.key:
            self._in_order(subtree.left, lo, hi, q)
            
        if subtree.key >= lo and subtree.key <= hi:
            q.append(subtree.key)
        
        if hi > subtree.key:
            self._in_order(subtree.right, lo, hi, q)

    def display(self, filename='img/red_black_bst', view=True):
        """
        Display tree by rendering it with Graphviz.
        """
        dot = graphviz.Digraph()
        root = self.root
        if root is None:
            dot.node("", shape="point")
            dot.render(filename, view=view, format='png')
            return
        
        root_color = "red" if root.color else "black"
        dot.node(str(root.key), color=root_color)

        def add_nodes_edges(node):
            
            ### LEFT NODE
            # LINK: Node or null
            if node.left:
                left_node = str(node.left.key)
                shape = "ellipse"
                weight = "1"
            else:
                left_node = "None" + str(random())
                shape = "point"
                weight = "2"
            
            # EDGE: RED or BLACK
            if self.is_red(node.left):
                color = "red"
                penwidth = "2"
            else:
                color = "black"
                penwidth = "1"
                
            dot.node(left_node, shape=shape, color=color)
            dot.edge(
                str(node.key),  # node from
                left_node,      # node to
                color=color,
                penwidth=penwidth,
                weight=weight,
                )
            
            # recursively add more nodes
            if node.left:
                add_nodes_edges(node.left)
            
            ### RIGHT NODE
            # LINK: Node or null
            if node.right:
                right_node = str(node.right.key)
                shape = "ellipse"
                weight = "1"
            else:
                right_node = "None" + str(random())
                shape = "point"
                weight = "2"
            
            # EDGE: RED or BLACK
            if self.is_red(node.right):
                color = "red"
                penwidth = "2"
            else:
                color = "black"
                penwidth = "1"
                
            dot.node(right_node, shape=shape, color=color)
            dot.edge(
                str(node.key),  # node from
                right_node,      # node to
                color=color,
                penwidth=penwidth,
                weight=weight,
                )
            # recursively add more nodes
            if node.right:
                add_nodes_edges(node.right)
            
        add_nodes_edges(root)
        dot.render(filename, view=view, format='png')
    
# ------------------------------------------------
#   TESTS
# ------------------------------------------------
import unittest
from random import randint, choice

class TestsRedBlackBST(unittest.TestCase):
    def setUp(self):
        self.bst = RedBlackBST()
        
        # for display testing: open the rendered image
        self.view = False
        
    def test_is_BST_empty_tree(self):
        self.assertTrue(self.bst.is_BST)
    
    def test_is_not_a_BST(self):
        # left subtree > root
        self.bst.root = root = self.bst._Node(1, 'a')
        root.left = self.bst._Node(2, 'b')
        self.assertFalse(self.bst.is_BST)
        
        # right subtree < root
        root.left = None
        root.right = self.bst._Node(0, 'c')          # not ok
        self.assertFalse(self.bst.is_BST)
        
        # deeper tree
        root.right = self.bst._Node(3, 'd')          # ok
        root.right.right = self.bst._Node(2, 'b')    # not ok
        self.assertFalse(self.bst.is_BST)
             
    def test_is_BST(self):
        # left subtree < root
        root = self.bst.root = self.bst._Node(1, 'a')
        root.left = self.bst._Node(0, 'b')
        self.assertTrue(self.bst.is_BST)
        
        # right subtree > root
        root.left = None
        root.right = self.bst._Node(2, 'c')
        self.assertTrue(self.bst.is_BST)
        
        # deeper tree
        root.right = self.bst._Node(3, 'b')
        root.right.right = self.bst._Node(4, 'c')
        root.right.left = self.bst._Node(2, 'd')
        self.assertTrue(self.bst.is_BST)

    def test_is_size_consistent_empty_tree(self):
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_is_size_consistent_false(self):
        root = self.bst.root = self.bst._Node(3, 'a', size=2)
        self.assertFalse(self.bst.is_size_consistent)
        
        root.left = self.bst._Node(2, 'b', size=2)     # nok
        root.size = 2                                  # ok
        self.assertFalse(self.bst.is_size_consistent)
        
        root.right = self.bst._Node(5, 'c', size=3)    # nok
        root.right.left = self.bst._Node(4, 'e', size=1) # ok
        root.size = 4
        self.assertFalse(self.bst.is_size_consistent)
        
    def test_is_size_consistent(self):
        root = self.bst.root = self.bst._Node(3, 'a')
        self.assertTrue(self.bst.is_size_consistent)
        
        root.left = self.bst._Node(2, 'b')
        root.size = 2
        self.assertTrue(self.bst.is_size_consistent)
        
        root.right = self.bst._Node(5, 'c')
        root.size = 3
        self.assertTrue(self.bst.is_size_consistent)
        
        root.left.left = self.bst._Node(1, 'd')
        root.left.size = 2
        root.size = 4
        self.assertTrue(self.bst.is_size_consistent)
        
        root.right.left = self.bst._Node(4, 'e')
        root.right.size = 2
        root.size = 5
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_is_red(self):
        # IS RED
        red_node = self.bst._Node(1, 'a', color=True)
        self.assertTrue(self.bst.is_red(red_node))
        
        # IS NOT RED
        black_node = self.bst._Node(1, 'a', color=False)
        self.assertFalse(self.bst.is_red(black_node))
        
        # DEFAULT COLOR IS RED!
        new_node = self.bst._Node(1, 'a')
        self.assertTrue(self.bst.is_red(new_node))
        
    def test_is_23tree_empty_tree(self):
        self.assertTrue(self.bst.is_23tree)
        
    def test_is_23tree_right_red_link(self):
        # right-leaning red link
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=True)
        self.assertFalse(self.bst.is_23tree)
        
        # deeper right-leaning red link
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        root.left = self.bst._Node(2, 'c', color=True)
        self.assertTrue(self.bst.is_23tree)
        root.left.color = False
        root.left.right = self.bst._Node(4, 'd', color=True)
        self.assertFalse(self.bst.is_23tree)
        
    def test_is_23tree_4node(self):
        # node connected to two red links, aka 4-node
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        root.right.left = self.bst._Node(6, 'b', color=True)
        root.right.left.left = self.bst._Node(8, 'b', color=True)
        self.assertFalse(self.bst.is_23tree)
    
    def test_is_23tree(self):
        # no right-leaning red links
        # AND no node is connected to two red links
        self.bst.root = root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        
        root.left = self.bst._Node(3, 'c', color=True)
        self.assertTrue(self.bst.is_23tree)
        
        root.left.left = self.bst._Node(2, 'd', color=True)
        root.left.color = False
        root.left.right = self.bst._Node(4, 'e', color=False)
        self.assertTrue(self.bst.is_23tree)
        
        root.right.left = self.bst._Node(6, 'b', color=True)
        root.right.right = self.bst._Node(8, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
    
    def test_is_balanced_empty_tree(self):
        self.assertTrue(self.bst.is_balanced)
    
    def test_is_NOT_balanced(self):
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
        # not balanced, must rotate left
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        # fix
        root.right.left = root
        root = self.bst.root = root.right
        root.left.right = None
        root.left.color = True
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
    def test_is_NOT_balanced_4node(self):
        # not balanced bc 4-link-node
        root = self.bst.root = self.bst._Node(7, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        root.left = self.bst._Node(5, 'b', color=True)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        # 4th link coming up
        root.right = self.bst._Node(9, 'c', color=False)
        root.color = True
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        
    def test_is_balanced(self):
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        # rotate left
        root.right.left = root
        root = self.bst.root = root.right
        root.left.right = None
        root.left.color = True
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
        
        root.right = self.bst._Node(9, 'c', color=False)
        # not balanced bc 4-node
        self.assertTrue(self.bst.is_23tree)
        self.assertFalse(self.bst.is_balanced)
        # split 4-node
        root.left.color = False
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_balanced)
    
    def test_assert_integrity_empty_tree(self):
        self.bst.assert_integrity()
        
    def test_assert_integrity_NOT_BST(self):
        self.bst.root = self.bst._Node(1, 'a', color=False)
        self.bst.root.left = self.bst._Node(2, 'a', color=True)
        
        with self.assertRaisesRegex(AssertionError, RedBlackBST.NOT_BST):
            self.bst.assert_integrity()
        
    def test_assert_integrity_NOT_23TREE(self):
        self.bst.root = self.bst._Node(5, 'a', color=False)
        self.bst.root.right = self.bst._Node(7, 'b', color=True)
        
        with self.assertRaisesRegex(AssertionError, RedBlackBST.NOT_23TREE):
            self.bst.assert_integrity()
            
    def test_assert_integrity_NOT_BALANCED(self):
        self.bst.root = self.bst._Node(5, 'a', color=False)
        self.bst.root.right = self.bst._Node(7, 'b', color=False)

        with self.assertRaisesRegex(AssertionError, RedBlackBST.NOT_BALANCED):
            self.bst.assert_integrity()
            
    def test_assert_integrity_NOT_SIZE_CONSISTENT(self):
        self.bst.root = self.bst._Node(3, 'a', size=2)

        with self.assertRaisesRegex(AssertionError,
                                    RedBlackBST.NOT_SIZE_CONSISTENT):
            self.bst.assert_integrity()
            
    def test_assert_integrity_RED_ROOT(self):
        self.bst.root = self.bst._Node(3, 'a', color=True)

        with self.assertRaisesRegex(AssertionError,
                                    RedBlackBST.RED_ROOT):
            self.bst.assert_integrity()
            
    def test_rotate_left(self):
        previous_root = self.bst.root = self.bst._Node(5, 'a', size=2, color=False)
        previous_right = previous_root.right = self.bst._Node(7, 'c', size=1, color=True)
        #   (5)
        #  /  \\
        #     (7)
        self.assertFalse(self.bst.is_23tree)
        self.bst.root = self.bst._rotate_left(previous_root)
        #   (7)
        #  //  \
        # (5)
        self.assertEqual(self.bst.root, previous_right)
        self.assertEqual(self.bst.root.left.key, 5)
        self.assertTrue(previous_root.color)
        self.bst.assert_integrity()
    
    def test_rotate_left_more_nodes(self):
        # very HYPOTHETICAL case for testing purposes
        root = self.bst.root = self.bst._Node(5, 'a', size=4, color=False)
        root.left = self.bst._Node(4, 'b', size=1, color=False)
        root.right = self.bst._Node(7, 'c', size=2, color=True)
        root.right.left = self.bst._Node(6, 'd', size=1, color=False)
        #       (5)
        #      /   \\
        #    (4)   (7)
        #          /
        #       (6)
        self.assertFalse(self.bst.is_23tree)
        
        self.bst.root = self.bst._rotate_left(root)
        #        (7)
        #      //   \
        #    (5)
        #   /   \
        # (4)    (6)
        self.assertTrue(self.bst.is_23tree)
        self.assertTrue(self.bst.is_size_consistent)
        
    def test_rotate_right_simple(self):
        previous_root = self.bst.root = self.bst._Node(7, 'a', size=2, color=False)
        previous_left_node = self.bst.root.left = self.bst._Node(5, 'c', size=1, color=True)
        #   (7)
        #  //  \
        # (5)
        self.bst.root = self.bst._rotate_right(self.bst.root)
        #    (5)
        #   /  \\
        #      (7)
        self.assertEqual(self.bst.root, previous_left_node)
        self.assertEqual(self.bst.root.right, previous_root)
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_rotate_right_more_nodes(self):
        # highly HYPOTHETICAL case for testing purposes
        previous_root = self.bst.root = self.bst._Node(7, 'a', size=5, color=False)
        self.bst.root.right = self.bst._Node(8, 'e', size=1, color=False)
        previous_left_node = self.bst.root.left = self.bst._Node(5, 'b', size=3, color=True)
        previous_between = self.bst.root.left.right = self.bst._Node(6, 'c', size=1, color=False)
        previous_left_node.left = self.bst._Node(4, 'd', size=1, color=False)
        #      (7)
        #     //  \
        #    (5)   (8)
        #   /   \
        # (4)   (6)
        self.bst.root = self.bst._rotate_right(self.bst.root)
        #      (5)
        #      / \
        #   (4)   (7)
        #         / \
        #      (6)   (8)
        self.assertEqual(self.bst.root, previous_left_node)
        self.assertEqual(self.bst.root.right, previous_root)
        self.assertEqual(self.bst.root.right.left, previous_between)
        self.assertTrue(self.bst.is_size_consistent)
    
    def test_flip_colors_empty_tree(self):
        self.assertFalse(self.bst._flip_colors(self.bst.root))
    
    def test_flip_colors_one_null_child(self):
        # left child is None
        root = self.bst.root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=False)
        self.assertFalse(self.bst._flip_colors(self.bst.root))
        
        # right child is None
        root.right = None
        root.left = self.bst._Node(3, 'c', color=True)
        self.assertFalse(self.bst._flip_colors(self.bst.root))
        
    def test_flip_colors_same_color_parent_child(self):
        # all black
        self.bst.root = root = self.bst._Node(5, 'a', color=False)
        root.right = self.bst._Node(7, 'b', color=False)
        root.left = self.bst._Node(3, 'c', color=False)
        self.assertFalse(self.bst._flip_colors(self.bst.root))
        # all red
        root.color = True
        root.right.color = True
        root.left.color = True
        self.assertFalse(self.bst._flip_colors(self.bst.root))

    def test_flip_colors(self):
        # black parent
        self.bst.root = root = self.bst._Node(5, 'a', color=False)
        left_child =root.left = self.bst._Node(3, 'c', color=True)
        right_child =root.right = self.bst._Node(7, 'b', color=True)
        
        self.assertTrue(self.bst._flip_colors(root))
        self.assertTrue(root.color)
        self.assertFalse(left_child.color)
        self.assertFalse(right_child.color)
        
        # flip again (red parent)
        self.assertTrue(self.bst._flip_colors(root))
        self.assertFalse(root.color)
        self.assertTrue(left_child.color)
        self.assertTrue(right_child.color)
        
    def test_put_empty_tree(self):
        bst = self.bst
        bst.put(5, 5)
        self.assertEqual(bst.root.key, 5)
        
    def test_put_existing_key(self):
        bst = self.bst
        bst.put(5, 5)
        bst.put(5, 10)
        self.assertEqual(bst.root.key, 5)
        self.assertEqual(bst.root.val, 10)
        
    def test_put_left(self):
        bst = self.bst
        bst.put(5, 5)
        bst.put(3, 3)
        bst.assert_integrity()
        expected_node = bst._Node(3, 3, color=True, size=1)
        self.assertEqual(expected_node, bst.root.left)
        
    def test_put_right(self):
        bst = self.bst
        bst.put(5, 5)
        bst.put(7, 7)
        bst.assert_integrity()
        expected_root = bst._Node(7, 7, color=False, size=2)
        expected_left = bst._Node(5, 5, color=True, size=1)
        self.assertEqual(expected_root, bst.root)
        self.assertEqual(expected_left, bst.root.left)
        
    def test_put(self):
        bst = self.bst
        bst.put(5, "apple")
        bst.put(2, "banana")
        bst.put(7, "cherry")
        bst.put(4, "date")
        bst.assert_integrity()
    
    def test_del_min_empty_tree(self):
        with self.assertRaises(KeyError):
            self.bst.del_min()
            
    def test_del_min_single_node(self):
        self.bst.put('a', 'apple')
        self.bst.del_min()
        self.assertTrue(self.bst.is_empty)
    
    def test_del_min_single_child(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.del_min()
        self.assertFalse(self.bst.contains('a'))
        self.assertEqual(self.bst.root.key, 'b')
        self.assertTrue(self.bst.assert_integrity())
    
    def test_del_min_two_children(self):
        bst = self.bst
        bst.put('a', 'apple')
        bst.put('b', 'banana')
        bst.put('c', 'cherry')
        bst.del_min()
        self.assertFalse(bst.contains('a'))
        self.assertEqual(bst.root.key, 'c')
        self.assertTrue(bst.is_red(bst.root.left))
        self.assertTrue(bst.assert_integrity())
    
    def test_del_min_deeper_node(self):
        bst = self.bst
        bst.put('d', 'daisy')
        bst.put('c', 'cherry')
        bst.put('b', 'banana')
        bst.put('a', 'apple')
        bst.del_min()
        self.assertFalse(bst.contains('a'))
        self.assertTrue(bst.contains('b'))
        self.assertTrue(bst.contains('d'))
        self.assertEqual(bst.root.key, 'c')
        self.assertTrue(bst.assert_integrity())
    
    def test_del_min(self):
        bst = self.bst
        
        # random keys
        keys = {randint(0, 1_000) for _ in range(100)}
        for key in keys:
            bst.put(key, str(key))
        
        min_key = min(keys)
        bst.del_min()
        expected_tree_size = len(keys) - 1
        self.assertFalse(bst.contains(min_key))
        self.assertEqual(bst.size(), expected_tree_size)
        self.assertTrue(bst.assert_integrity())
    
    def test_del_max_empty_tree(self):
        with self.assertRaises(KeyError):
            self.bst.del_max()
            
    def test_del_max_single_node(self):
        self.bst.put('a', 'apple')
        self.bst.del_max()
        self.assertTrue(self.bst.is_empty)
    
    def test_del_max_single_child(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.del_max()
        self.assertFalse(self.bst.contains('b'))
        self.assertEqual(self.bst.root.key, 'a')
        self.assertTrue(self.bst.assert_integrity())
    
    def test_del_max_root_with_two_children(self):
        bst = self.bst
        bst.put('a', 'apple')
        bst.put('b', 'banana')
        bst.put('c', 'cherry')
        bst.del_max()
        self.assertFalse(bst.contains('c'))
        self.assertEqual(bst.root.key, 'b')
        self.assertTrue(bst.assert_integrity())
    
    def test_del_max_deeper_with_left_child(self):
        bst = self.bst
        bst.put('a', 'apple')
        bst.put('b', 'banana')
        bst.put('c', 'cherry')
        bst.put('d', 'daisy')
        bst.del_max()
        self.assertFalse(bst.contains('d'))
        self.assertEqual(bst.root.key, 'b')
        self.assertTrue(bst.assert_integrity())
    
    def test_del_max(self):
        bst = self.bst
        
        # random keys
        keys = {randint(0, 1_000) for _ in range(100)}
        for key in keys:
            bst.put(key, str(key))
        
        max_key = max(keys)
        bst.del_max()
        expected_tree_size = len(keys) - 1
        self.assertFalse(bst.contains(max_key))
        self.assertEqual(bst.size(), expected_tree_size)
        self.assertTrue(bst.assert_integrity())

    def test_del_key_empty_BST(self):
        with self.assertRaises(KeyError):
            self.bst.del_key(1)
    
    def test_del_key_not_in_BST(self):
        self.bst.put('a', 'apple')
        
        with self.assertRaises(KeyError):
            self.bst.del_key('b')

    def test_del_key_root(self):
        self.bst.put('a', 'apple')
        self.bst.del_key('a')
        self.assertTrue(self.bst.is_empty)
    
    def test_del_key_left_with_no_child(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.bst.del_key('a')
        self.assertFalse(self.bst.contains('a'))
        self.assertTrue(self.bst.assert_integrity())

    def test_del_key_left_with_left_child(self):
        self.bst.put('d', 'daisy')
        self.bst.put('c', 'cherry')
        self.bst.put('b', 'banana')
        self.bst.put('a', 'apple')
        self.bst.del_key('b')
        self.assertFalse(self.bst.contains('b'))
        self.assertTrue(self.bst.assert_integrity())
    
    def test_del_key_left_with_both_children(self):
        self.bst.put('e', 'eggplant')
        self.bst.put('d', 'daisy')
        self.bst.put('c', 'cherry')
        self.bst.put('b', 'banana')
        self.bst.put('a', 'apple')
        self.bst.del_key('b')
        self.assertFalse(self.bst.contains('b'))
        self.assertTrue(self.bst.assert_integrity())
        
    def test_del_key_right_with_no_child(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.bst.del_key('c')
        self.assertFalse(self.bst.contains('c'))
        self.assertTrue(self.bst.assert_integrity())
    
    def test_del_key_right_with_left_child(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.bst.put('d', 'daisy')
        self.bst.del_key('d')
        self.assertFalse(self.bst.contains('d'))
        self.assertTrue(self.bst.assert_integrity())
    
    def test_del_key_right_with_both_children(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.bst.put('d', 'daisy')
        self.bst.put('e', 'eggplant')
        self.bst.put('f', 'fig')
        self.bst.put('g', 'guava')
        self.bst.del_key('d')
        self.assertFalse(self.bst.contains('d'))
        self.assertTrue(self.bst.assert_integrity())
    
    def test_del_key(self):
        # random keys
        keys = {randint(0, 1_000) for _ in range(100)}
        for key in keys:
            self.bst.put(key, str(key))
        
        keys = list(keys)
        while keys:
            random_key = choice(keys)   # choose random key from keys
            keys.remove(random_key)
            self.bst.del_key(random_key)
            self.assertFalse(self.bst.contains(random_key))
            self.assertTrue(self.bst.assert_integrity())
    
    def test_Node_invalid_color(self):
        with self.assertRaises(ValueError):
            self.bst._Node('a', 'a', color = 'blue')
    
    def test_Node_repr(self):
        node = self.bst._Node('a', 'apple', size = 3, color = False)
        expected = "_Node(key=a, val=apple, size=3, color=BLACK)"
        self.assertEqual(expected, node.__repr__())
            
    def test_Node_eq(self):
        node1 = self.bst._Node('a', 'apple', size = 3, color = False)
        node2 = self.bst._Node('a', 'apple', size = 3, color = False)
        self.assertIsNot(node1, node2)
        self.assertEqual(node1, node2)
            
    def test_Node_not_eq(self):
        node1 = self.bst._Node('a', 'apple', size = 3, color = False)
        node2 = self.bst._Node('a', 'apple', size = 4, color = False)
        self.assertIsNot(node1, node2)
        self.assertNotEqual(node1, node2)
            
    def test_Node_eq_type_error(self):
        node1 = self.bst._Node('a', 'apple')
        node2 = 'a'
        self.assertIsNot(node1, node2)
        with self.assertRaises(TypeError):
            node1 == node2
    
    def test_min_empty_tree(self):
        self.assertIsNone(self.bst.min())
        
    def test_min(self):
        self.bst.put(5, "apple")
        self.assertEqual(5, self.bst.min())
        
        self.bst.put(2, "banana")
        self.assertEqual(2, self.bst.min())
        
        self.bst.put(7, "cherry")
        self.assertEqual(2, self.bst.min())
        
        self.bst.put(6, "date")
        self.assertEqual(2, self.bst.min())
        
        self.bst.put(1, "eggplant")
        self.assertEqual(1, self.bst.min())
        
    def test_max_empty_tree(self):
        self.assertIsNone(self.bst.max())
        
    def test_max(self):
        self.bst.put(5, "apple")
        self.assertEqual(5, self.bst.max())
        
        self.bst.put(2, "banana")
        self.assertEqual(5, self.bst.max())
        
        self.bst.put(7, "cherry")
        self.assertEqual(7, self.bst.max())
        
        self.bst.put(6, "date")
        self.assertEqual(7, self.bst.max())
        
        self.bst.put(9, "eggplant")
        self.assertEqual(9, self.bst.max())
    
    def test_floor_empty_tree(self):
        self.assertIsNone(self.bst.floor(1))
    
    def test_floor(self):
        self.bst.put(50, 50)
        self.bst.put(70, 70)
        self.bst.put(30, 20)
        self.bst.put(10, 10)
        self.bst.put(80, 80)
        self.bst.put(40, 40)

        # floor == root
        self.assertEqual(self.bst.floor(50), 50)
        self.assertEqual(self.bst.floor(70), 70)
        self.assertEqual(self.bst.floor(30), 30)
        self.assertEqual(self.bst.floor(10), 10)
        self.assertEqual(self.bst.floor(80), 80)
        self.assertEqual(self.bst.floor(40), 40)

        # other
        self.assertIsNone(self.bst.floor(1))
        self.assertIsNone(self.bst.floor(5))
        self.assertEqual(self.bst.floor(15), 10)
        self.assertEqual(self.bst.floor(25), 10)
        self.assertEqual(self.bst.floor(35), 30)
        self.assertEqual(self.bst.floor(45), 40)
        self.assertEqual(self.bst.floor(69), 50)
        self.assertEqual(self.bst.floor(99), 80)
        self.assertEqual(self.bst.floor(88), 80)
        self.assertEqual(self.bst.floor(77), 70)
    
    def test_ceiling_empty_tree(self):
        self.assertIsNone(self.bst.ceiling(1))
    
    def test_ceiling(self):
        self.bst.put(50, 50)
        self.bst.put(70, 70)
        self.bst.put(30, 20)
        self.bst.put(10, 10)
        self.bst.put(80, 80)
        self.bst.put(40, 40)

        # ceiling == root
        self.assertEqual(self.bst.ceiling(50), 50)
        self.assertEqual(self.bst.ceiling(70), 70)
        self.assertEqual(self.bst.ceiling(30), 30)
        self.assertEqual(self.bst.ceiling(10), 10)
        self.assertEqual(self.bst.ceiling(80), 80)
        self.assertEqual(self.bst.ceiling(40), 40)

        # other
        self.assertEqual(self.bst.ceiling(1), 10)
        self.assertEqual(self.bst.ceiling(5), 10)
        self.assertEqual(self.bst.ceiling(15), 30)
        self.assertEqual(self.bst.ceiling(25), 30)
        self.assertEqual(self.bst.ceiling(35), 40)
        self.assertEqual(self.bst.ceiling(45), 50)
        self.assertEqual(self.bst.ceiling(69), 70)
        self.assertEqual(self.bst.ceiling(99), None)
        self.assertEqual(self.bst.ceiling(88), None)
        self.assertEqual(self.bst.ceiling(77), 80)

    def test_select_empty_tree(self):
        with self.assertRaises(ValueError):
            self.bst.select(0)
        
    def test_select_out_of_range(self):
        self.bst.put(5, "apple")
        
        with self.assertRaises(ValueError):
            self.assertIsNone(self.bst.select(-1))
        
        with self.assertRaises(ValueError):
            self.assertIsNone(self.bst.select(1))
        
    def test_select(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(6, "date")
        self.bst.put(3, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)
        self.assertEqual(2, self.bst.select(0))
        self.assertEqual(3, self.bst.select(1))
        self.assertEqual(5, self.bst.select(2))
        self.assertEqual(6, self.bst.select(3))
        self.assertEqual(7, self.bst.select(4))
    
    def test_rank_empty_tree(self):
        with self.assertRaises(KeyError):
            self.bst.rank(1)
        
    def test_rank_key_not_in_BST(self):
        self.bst.put(5, "apple")
        
        with self.assertRaises(KeyError):
            self.bst.rank(2)
        
    def test_rank(self):
        self.bst.put(5, "apple")
        self.bst.put(2, "banana")
        self.bst.put(7, "cherry")
        self.bst.put(6, "date")
        self.bst.put(3, "eggplant")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        #     (3) (6)
        self.assertEqual(0, self.bst.rank(2))
        self.assertEqual(1, self.bst.rank(3))
        self.assertEqual(2, self.bst.rank(5))
        self.assertEqual(3, self.bst.rank(6))
        self.assertEqual(4, self.bst.rank(7))
    
    def test_keys_empty_tree(self):
        self.assertEqual([], self.bst.keys())
    
    def test_all_keys(self):
        bst = self.bst # for convenience
        
        bst.put(5, "apple")
        self.assertEqual([5], self.bst.keys())
        
        bst.put(2, "banana")
        self.assertEqual([2, 5], self.bst.keys())
        
        bst.put(7, "cherry")
        self.assertEqual([2, 5, 7], self.bst.keys())
        
        bst.put(6, "date")
        bst.put(1, "eggplant")
        bst.put(8, "fig")
        self.assertEqual([1, 2, 5, 6, 7, 8], self.bst.keys())
    
    def test_keys_in_range(self):
        bst = self.bst # for convenience
        
        bst.put(5, "apple")
        bst.put(2, "banana")
        bst.put(7, "cherry")
        bst.put(6, "date")
        bst.put(1, "eggplant")
        bst.put(8, "fig")
        #      (5)
        #     /   \
        #   (2)    (7)
        #   / \    / \
        # (1)    (6) (8)
        
        result = bst.keys(1, 1)
        expected = [1]
        self.assertEqual(expected, result)
        
        result = bst.keys(7, 7)
        expected = [7]
        self.assertEqual(expected, result)
        
        result = bst.keys(1, 2)
        expected = [1, 2]
        self.assertEqual(expected, result)
        
        result = bst.keys(7, 10)
        expected = [7, 8]
        self.assertEqual(expected, result)
        
        result = bst.keys(1, 5)
        expected = [1, 2, 5]
        self.assertEqual(expected, result)
        
        result = bst.keys(2, 7)
        expected = [2, 5, 6, 7]
        self.assertEqual(expected, result)
        
        result = bst.keys(0, 10)
        expected = [1, 2, 5, 6, 7, 8]
        self.assertEqual(expected, result)
    
    def test_display_empty(self):
        self.bst.display('img/test_empty_bst', view=self.view)
    
    def test_display_left_red(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.display('img/test_left_red', view=self.view)
    
    def test_display_right_red(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.root.right = self.bst.root.left
        self.bst.root.left = None
        self.bst.display('img/test_right_red', view=self.view)
    
    def test_display(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.bst.put('d', 'daisy')
        self.bst.put('e', 'eggplant')
        self.bst.put('f', 'fig')
        self.bst.put('g', 'guava')
        self.bst.display('img/test_display', view=self.view)
    
    def test_move_red_left_empty_tree(self):
        self.assertIsNone(self.bst._move_red_left(self.bst.root))
    
    def test_move_red_left_black_subtree(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.assertEqual(self.bst._move_red_left(self.bst.root), self.bst.root)
    
    def test_move_red_left_two_left_reds(self):
        self.bst.put('d', 'daisy')
        self.bst.put('c', 'cherry')
        self.bst.put('b', 'banana')
        self.bst.put('a', 'apple')
        self.bst.root.color = True
        self.bst.root.left.color = True
        self.assertEqual(self.bst._move_red_left(self.bst.root), self.bst.root)
    
    def test_move_red_right_empty_tree(self):
        self.assertIsNone(self.bst._move_red_right(self.bst.root))
    
    def test_move_red_right_black_subtree(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.assertEqual(self.bst._move_red_right(self.bst.root), self.bst.root)
    
    def test_move_red_right_two_left_reds(self):
        self.bst.put('a', 'apple')
        self.bst.put('b', 'banana')
        self.bst.put('c', 'cherry')
        self.bst.put('d', 'daisy')
        self.bst.root.color = True
        self.bst.root.right.color = True
        self.assertEqual(self.bst._move_red_right(self.bst.root), self.bst.root)
    
#   END OF TESTS
# ------------------------------------------------   
if __name__ == "__main__":
    bst = RedBlackBST()
    bst.put('a', 'apple')
    print(bst.root)
