from digraph import Digraph
from tests_digraph import TestsDigraph

class DFS:
    """
    Depth-first search is a classic recursive method for
    systematically examining each of the vertices and edges
    in a (di)graph. To visit a vertex:

    1) Mark it as having been visited.

    2) Visit (recursively) all the vertices that are outgoing
    from it and that have not yet been marked. 
    """
    CONNECTED   = True
    NOT_A_GRAPH = "First argument must be a Digraph object."

    def __init__(self, G: Digraph, s: int) -> None:
        # validation
        if not isinstance(G, Digraph):
            raise TypeError(DFS.NOT_A_GRAPH)
        
        if not G.has_vertex(s):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        # init
        self._G      : Digraph    = G
        self._source : int        = s
        self._marked : list[bool] = [False for _ in range(G.vertex_count)]
        
        # search
        self._dfs(G, s)

    def has_path_from_source(self, v: int):
        """ Is there a directed path from source to vertex `v`?"""
        if not self._G.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return self._marked[v]
    
    @property
    def count(self):
        """Returns number of vertices with an incoming
        path from source `s`.
        Considers the source itself."""
        return self._marked.count(DFS.CONNECTED)
    
    def _dfs(self, G: Digraph, v: int):
        self._marked[v] = True

        for w in G.outgoing_from(v):
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
        G = Digraph(0)
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            self.DFS(G, "0")
    
    def test_002_init_value_error_negative_integer(self):
        G = Digraph(0)
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            self.DFS(G, -1)

    def test_003_init_vertex_not_in_graph(self):
        G = Digraph(0)
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            self.DFS(G, 1)
    
    def test_004_init_correct_visited_length(self):
        for V in range(1, 100):
            G = Digraph(V)
            dfs = self.DFS(G, 0)
            expected = G.vertex_count
            marked_length = len(dfs._marked)
            self.assertEqual(expected, marked_length)
    
    def test_010_dfs_no_edges(self):
        V = 5
        G = Digraph(V)
        
        for v in range(G.vertex_count):
            dfs = self.DFS(G, v)
            self.assertEqual(dfs.count, 1) # only the vertex itself
    
    def test_011_dfs_two_connected_vertices(self):
        V = 2
        G = Digraph(V)
        v0, v1 = 0, 1
        G.add_edge(v0, v1) # v0 -> v1
        
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 2) # itself and `v1`
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 1) # itself, no other outgoing edge

        G.add_edge(v1, v0) # v1 -> v0
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 2) # itself and `v1`
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 2) # itself + outgoing edge to v0
    
    def test_012_dfs_two_connected_vertices_and_one_not(self):
        V = 3
        G = Digraph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 2) # itself and `v1`
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 1) # itself
        
        dfs_v2 = self.DFS(G, v2)
        self.assertEqual(dfs_v2.count, 1) # only `v2` itself
    
    def test_013_dfs_many_connected(self):
        V = 3
        G = Digraph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        
        dfs_v0 = self.DFS(G, v0)
        self.assertEqual(dfs_v0.count, 3) # itself + others
        
        dfs_v1 = self.DFS(G, v1)
        self.assertEqual(dfs_v1.count, 2) # itself + others
        
        dfs_v2 = self.DFS(G, v2)
        self.assertEqual(dfs_v2.count, 1) # itself + others
    
    def test_020_has_path_from_source__a_vertex_not_in_graph(self):
        V = 1
        G = Digraph(V)
        v0, v_not_in_graph = 0, 1
        dfs = self.DFS(G, v0)
        
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            dfs.has_path_from_source(v_not_in_graph)
    
    def test_021_has_path_from_source__a_vertex_not_connected(self):
        V = 2
        G = Digraph(V)
        v0, v_not_connected = 0, 1
        dfs = self.DFS(G, v0)
        
        self.assertFalse(dfs.has_path_from_source(v_not_connected))

    def test_022_has_path_from_source__a_strictly_outgoing_vertex(self):
        V = 2
        G = Digraph(V)
        source, strictly_outgoing_v = 0, 1
        G.add_edge(strictly_outgoing_v, source)
        dfs = self.DFS(G, source)
        
        self.assertFalse(dfs.has_path_from_source(strictly_outgoing_v))
    
    def test_023_has_path_from_source(self):
        V = 3
        G = Digraph(V)
        source = 0
        adjacent_outgoing_v = 1
        farther_outgoing_v  = 2
        # outgoing edges
        G.add_edge(source, adjacent_outgoing_v)
        G.add_edge(adjacent_outgoing_v, farther_outgoing_v)
        
        dfs = self.DFS(G, source)
        
        self.assertTrue(dfs.has_path_from_source(adjacent_outgoing_v))
        self.assertTrue(dfs.has_path_from_source(farther_outgoing_v))
