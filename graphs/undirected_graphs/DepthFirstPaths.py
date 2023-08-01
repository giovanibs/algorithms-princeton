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
        self.DFP = DFP

    def test_100_dfs_no_edges(self):
        V = 5
        G = Graph(V)
        
        for v in range(G.vertices_count):
            dfp = self.DFP(G, v)
            self.assertFalse(any(dfp._edge_to))
    
    def test_101_two_connected_vertices(self):
        V = 2
        G = Graph(V)
        v0, v1 = 0, 1
        G.add_edge(v0, v1)
        
        dfp = self.DFP(G, v0)
        self.assertIsNone(dfp._edge_to[v0])
        self.assertEqual(dfp._edge_to[v1], v0)
        
        dfp = self.DFP(G, v1)
        self.assertIsNone(dfp._edge_to[v1])
        self.assertEqual(dfp._edge_to[v0], v1)
        
    def test_102_many_connected(self):
        V = 4
        G = Graph(V)
        v0, v1, v2, v3 = 0, 1, 2, 3
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        G.add_edge(v1, v3)
        
        dfp = self.DFP(G, v0)
        self.assertIsNone(dfp._edge_to[v0])
        self.assertEqual(dfp._edge_to[v1], v0)
        self.assertEqual(dfp._edge_to[v2], v1)
        self.assertEqual(dfp._edge_to[v3], v1)
        
        dfp = self.DFP(G, v1)
        self.assertIsNone(dfp._edge_to[v1])
        self.assertEqual(dfp._edge_to[v0], v1)
        self.assertEqual(dfp._edge_to[v2], v1)
        self.assertEqual(dfp._edge_to[v3], v1)

        dfp = self.DFP(G, v2)
        self.assertIsNone(dfp._edge_to[v2])
        self.assertEqual(dfp._edge_to[v0], v1)
        self.assertEqual(dfp._edge_to[v1], v2)
        self.assertEqual(dfp._edge_to[v3], v1)

        dfp = self.DFP(G, v3)
        self.assertIsNone(dfp._edge_to[v3])
        self.assertEqual(dfp._edge_to[v0], v1)
        self.assertEqual(dfp._edge_to[v1], v3)
        self.assertEqual(dfp._edge_to[v2], v1)

#
