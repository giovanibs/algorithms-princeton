from undirected_graph import Graph
from tests_undirected_graph import TestsUndirectedGraph

class DFS:
    """
    Depth-first search is a classic recursive method for
    systematically examining each of the vertices and edges
    in a graph. To visit a vertex:

    1) Mark it as having been visited.

    2) Visit (recursively) all the vertices that are adjacent
    to it and that have not yet been marked. 
    """
    CONNECTED   = True
    NOT_A_GRAPH = "First argument must be a Graph object."

    def __init__(self, G: Graph, s: int) -> None:
        # validation
        if not isinstance(G, Graph):
            raise TypeError(DFS.NOT_A_GRAPH)
        
        if not G.has_vertex(s):
            raise IndexError(Graph.VERTEX_NOT_IN_GRAPH)
        
        # init
        self.G      : Graph         = G
        self.s      : int           = s
        self._marked: list[bool]    = [False for _ in range(G.vertices_count)]
        
        # search
        self._dfs(G, s)

    def marked(self, v: int):
        """ Is vertex `v` connected to vertex `s`? """
        if not self.G.has_vertex(v):
            raise IndexError(Graph.VERTEX_NOT_IN_GRAPH)
        
        return self._marked[v]
    
    @property
    def count(self):
        return self._marked.count(DFS.CONNECTED)
    
    def _dfs(self, G: Graph, v: int):
        self._marked[v] = True

        for w in G.adjacent_to(v):
            if not self._marked[w]:
                self._dfs(G, w)

import unittest

class TestsDFS(unittest.TestCase):
    def setUp(self) -> None:
        self.DFS = DFS

    def test_000_init_type_error_not_a_graph(self):
        with self.assertRaisesRegex(TypeError, self.DFS.NOT_A_GRAPH):
            self.DFS("G", 0)
    
    def test_001_init_type_error_not_a_integer(self):
        G = Graph(0)
        with self.assertRaisesRegex(TypeError, Graph.VERTEX_NOT_INTEGER):
            self.DFS(G, "0")
    
    def test_002_init_value_error_negative_integer(self):
        G = Graph(0)
        with self.assertRaisesRegex(ValueError, Graph.VERTEX_NOT_POSITIVE):
            self.DFS(G, -1)

    def test_003_init_vertex_not_in_graph(self):
        G = Graph(0)
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            self.DFS(G, 1)
    
    def test_004_init_correct_marked_length(self):
        for V in range(1, 100):
            G = Graph(V)
            dfs = self.DFS(G, 0)
            expected = G.vertices_count
            marked_length = len(dfs._marked)
            self.assertEqual(expected, marked_length)
    
    def test_010_dfs_no_edges(self):
        V = 5
        G = Graph(V)
        
        for v in range(G.vertices_count):
            dfs = self.DFS(G, v)
            self.assertEqual(dfs.count, 1) # only the vertex itself
    
    def test_011_dfs_two_connected_vertices(self):
        V = 2
        G = Graph(V)
        v0, v1 = 0, 1
        G.add_edge(v0, v1)
        
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 2) # itself and `v1`
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 2) # itself and `v0`
    
    def test_012_dfs_two_connected_vertices_and_one_not(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 2) # itself and `v1`
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 2) # itself and `v0`
        
        dfs_v2 = self.DFS(G, v2)
        self.assertEqual(dfs_v2.count, 1) # only `v2` itself
    
    def test_013_dfs_many_connected(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 3) # itself + others
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 3) # itself + others
        
        dfs_v2 = self.DFS(G, v2)
        self.assertEqual(dfs_v2.count, 3) # itself + others
    
    def test_020_marked_vertex_not_in_graph(self):
        V = 2
        G = Graph(V)
        v0, v1, v_not_in_graph = 0, 1, 2
        G.add_edge(v0, v1)
        dfs = self.DFS(G, v0)
        
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            dfs.marked(v_not_in_graph)

    def test_020_marked(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        
        dfs_v0 = self.DFS(G, v0)
        self.assertTrue(dfs_v0.marked(v0))      # itself
        self.assertTrue(dfs_v0.marked(v1))      # v1 connected
        self.assertFalse(dfs_v0.marked(v2))     # v2 not connected
        
        dfs_v1 = self.DFS(G, v1)
        self.assertTrue(dfs_v1.marked(v0))      # v0 connected
        self.assertTrue(dfs_v1.marked(v1))      # itself
        self.assertFalse(dfs_v1.marked(v2))     # v2 not connected
        
        dfs_v2 = self.DFS(G, v2)
        self.assertFalse(dfs_v2.marked(v0))     # v0 not connected
        self.assertFalse(dfs_v2.marked(v1))     # v1 not connected
        self.assertTrue(dfs_v2.marked(v2))      # itself
        