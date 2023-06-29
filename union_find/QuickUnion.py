class QuickUnion:
    """
    This class represents a very simple union-find (or disjoint-sets)
    data structure (without improvements).

    The union-find data type models a collection of sets
    containing `n` elements, named `0` through `n-1`.

    The value of the element represents its parent element. When
    the parent is the element itself, it is nominated the
    canonical / root / identifier / leader element of its set.
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

    def union(self, element1: int, element2: int) -> int:
        """
        Add a connection between the two elements, i.e. merge the
        set containing `element1` with the set containing `element2`.
        """
        root1 = self.find(element1)
        root2 = self.find(element2)

        if root1 != root2:
            self.parent[root1] = root2
            self.sets_count -= 1

        return self.sets_count

    def find(self, element: int) -> int:
        """
        Returns the root/canonical element of the set containing `element`.
        """
        self.validate_element_index(element)

        while element != self.parent[element]:
            element = self.parent[self.parent[element]]  # path compression
        return element

    def are_connected(self, element1: int, element2: int) -> bool:
        """
        Return `True` iff both elements are in the same set
        (i.e. both elements have the same root element).
        """
        self.validate_element_index(element1, element2)
        return self.find(element1) == self.find(element2)

    def validate_element_index(self, *elements):
        for element in elements:
            if element < 0 or element > len(self.parent):
                raise IndexError(
                    f"The element [{element}] does not belong to this object."
                )
