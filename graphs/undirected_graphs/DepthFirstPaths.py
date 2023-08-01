from undirected_graph import Graph
from tests_undirected_graph import TestsUndirectedGraph
from DepthFirstSearch import DFS, TestsDFS

class DFP(DFS):
    """
    DepthFirstPaths: Paths from a source vertex `v` to every other vertex.
    """

    def __init__(self, G: Graph, s: int) -> None:
        # redundant check only to initialize `_edge_to`
        if not isinstance(G, Graph):
            raise TypeError(DFP.NOT_A_GRAPH)
        
        self._edge_to : list[int|None] = [None for _ in range(G.vertices_count)]
        
        super().__init__(G, s)

    # redefine `_dfs` to populate `_edge_to`
    def _dfs(self, G: Graph, v: int):
        self._marked[v] = True

        for w in G.adjacent_to(v):
            if not self._marked[w]:
                self._edge_to[w] = v    # populate `_edge_to`
                self._dfs(G, w)
    
    def path_to(self, G: Graph, v: int):
        raise NotImplementedError

# ------------------------------------------------------------------------------
# UNIT TESTS
# ------------------------------------------------------------------------------

class TestsDFP(TestsDFS):
    def setUp(self) -> None:
        self.DFS = DFP   # test DFP against DFS tests
