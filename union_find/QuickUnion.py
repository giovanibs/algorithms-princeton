class QuickUnion:
    """
    This class represents a very simple union-find (or disjoint-sets)
    data structure (without improvements).

    The union-find data type models a collection of sets
    containing `n` nodes, named `0` through `n-1`.

    The value of the node represents its parent node. When
    the parent is the node itself, it is nominated the
    canonical / root / identifier / leader node of its set.
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError
        
        self.sets_count = n
        self.parent = list(range(n))

    def __repr__(self):
        return (
            f"QuickUnion (n = {len(self.parent)}):"
            + f"\n\t{self.parent = }\n\t{self.sets_count = }"
        )

    def __str__(self):
        return str(self.parent)

    def union(self, node1: int, node2: int) -> int:
        """
        Add a connection between the two nodes, i.e. merge the
        set containing `node1` with the set containing `node2`.
        """
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            self.parent[root1] = root2
            self.sets_count -= 1

        return self.sets_count

    def find(self, node: int) -> int:
        """
        Returns the root/canonical node of the set containing `node`.
        """
        self.validate_node_index(node)

        while node != self.parent[node]:
            node = self.parent[self.parent[node]]  # search path compression
        return node

    def are_connected(self, node1: int, node2: int) -> bool:
        """
        Return `True` iff both nodes are in the same set
        (i.e. both nodes have the same root node).
        """
        self.validate_node_index(node1, node2)
        return self.find(node1) == self.find(node2)

    def validate_node_index(self, *nodes):
        for node in nodes:
            if node < 0 or node > len(self.parent):
                raise IndexError(
                    f"The node [{node}] does not belong to this object."
                )
