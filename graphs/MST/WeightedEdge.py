from __future__ import annotations
from Comparable import Comparable


class Edge(Comparable):
    def __init__(self, v: int, w: int, weight: float) -> None:
        self._v = v
        self._w = w
        self._weight = weight
    

    def either(self) -> int:
        """Returns either endpoint."""
        return self._v


    def other(self, v: int) -> int:
        """Returns the other endpoint."""
        if v == self._v:
            return self._w
        
        return self._v


    def compare_to(self, other: Edge) -> int:
        """Compares `self` with `other`
        based on their `weight`"""
        
        if self._weight < other._weight:
            return -1
        
        elif self._weight > other._weight:
            return 1
        
        else:
            return 0


    def weight(self) -> float:
        """Returns the edge weight."""
        return self._weight


    def __str__(self) -> str:
        return f"Edge: {self._v}-{self._w} with weight {self._weight!r}"
