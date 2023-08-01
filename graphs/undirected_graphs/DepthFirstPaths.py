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
    
    def path_to(self, v: int):
        if not self.G.has_vertex(v):
            raise IndexError(Graph.VERTEX_NOT_IN_GRAPH)
        
        x = v
        path_to = []
        
        while x != self.s and self._edge_to[x] is not None:
            x = self._edge_to[x]
            path_to.append(x)
        
        return path_to or None

# ------------------------------------------------------------------------------
# UNIT TESTS
# ------------------------------------------------------------------------------

class TestsDFP(TestsDFS):
    def setUp(self) -> None:
        self.DFS = DFP   # test DFP against DFS tests
        self.DFP = DFP

    def test_100_edge_to_no_edges(self):
        V = 5
        G = Graph(V)
        
        for v in range(G.vertices_count):
            dfp = self.DFP(G, v)
            self.assertFalse(any(dfp._edge_to))
    
    def test_101_edge_to_two_connected_vertices(self):
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
        
    def test_102_edge_to_many_connected(self):
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

    def test_200_path_to_with_no_edges(self):
        V = 1
        G = Graph(V)
        v0 = 0
        
        dfp = self.DFP(G, v0)
        self.assertIsNone(dfp.path_to(v0))
    
    def test_201_path_to_with_vertex_not_in_graph(self):
        V = 1
        G = Graph(V)
        v0, v_not_in_graph = 0, 1
        dfp = self.DFS(G, v0)
        
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            dfp.path_to(v_not_in_graph)

    def test_202_path_to_two_connected_vertices(self):
        V = 2
        G = Graph(V)
        v0, v1 = 0, 1
        G.add_edge(v0, v1)
        
        dfp = self.DFP(G, v0)
        expected = [v0]
        result = dfp.path_to(v1)
        self.assertEqual(expected, result)

        dfp = self.DFP(G, v1)
        expected = [v1]
        result = dfp.path_to(v0)
        self.assertEqual(expected, result)

    def test_203_path_to_many_connected(self):
        V = 4
        G = Graph(V)
        v0, v1, v2, v3 = 0, 1, 2, 3
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        G.add_edge(v1, v3)
        
        ### source = v0
        dfp = self.DFP(G, v0)
        
        result = dfp.path_to(v1)
        expected = [v0]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v2)
        expected = [v1, v0]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v3)
        expected = [v1, v0]
        self.assertEqual(expected, result)

        ### source = v1
        dfp = self.DFP(G, v1)
        
        result = dfp.path_to(v0)
        expected = [v1]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v2)
        expected = [v1]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v3)
        expected = [v1]
        self.assertEqual(expected, result)

        ### source = v2
        dfp = self.DFP(G, v2)
        
        result = dfp.path_to(v0)
        expected = [v1, v2]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v1)
        expected = [v2]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v3)
        expected = [v1, v2]
        self.assertEqual(expected, result)

        ### source = v3
        dfp = self.DFP(G, v3)
        
        result = dfp.path_to(v0)
        expected = [v1, v3]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v1)
        expected = [v3]
        self.assertEqual(expected, result)
        
        result = dfp.path_to(v2)
        expected = [v1, v3]
        self.assertEqual(expected, result)

    def test_203_path_to_long_chain(self):
        V = 100
        G = Graph(V)
        for v in range(G.vertices_count-1):
            G.add_edge(v, v+1)

        dfp         = self.DFP(G, 0)
        last_vertex = G.vertices_count - 1
        expected    = list(range(last_vertex-1, -1, -1))
        result      = dfp.path_to(last_vertex)
        self.assertEqual(expected, result)

#
