from WeightedEdge import Edge


class EdgeWeightedGrah:
    def __init__(self, V: int) -> None:
        
        self._V: int = V
        """
        Number of vertices in the Graph"""
        self._adj: list[set[Edge]]