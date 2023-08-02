from queue import SimpleQueue

from undirected_graph import Graph
from tests_undirected_graph import TestsUndirectedGraph

class BFP:
    """
    Shortest path: path from source vertex `s` to another
    vertex `v` that uses fewest number of edges.

    Steps:
    1) Put `s` onto a FIFO queue, and mark `s` as visited.
    2) Repeat until the queue is empty:
            - remove the least recently added vertex `v`
            - add each of `v`'s UNMARKED neighbors to
            the queue, and mark them as visited.

    
    INIT        
    public BreadthFirstPaths(Graph G, Iterable<Integer> sources) {
    
    SEARCH
    private void bfs(Graph G, int s) {
    
    API - PATH
    public boolean hasPathTo(int v) {
    public int distTo(int v) {
    public Iterable<Integer> pathTo(int v) {
    
    HELPERS
    private boolean check(Graph G, int s) {
    private void validateVertex(int v) {


    """
    NOT_A_GRAPH = "First argument must be a Graph object."
    EMPTY_GRAPH = "Graph is empty."

    def __init__(self, G: Graph, s: int) -> None:
        # VALIDATIONS
        if not isinstance(G, Graph):
            raise TypeError(BFP.NOT_A_GRAPH)
        
        if not G.vertices_count:
            raise IndexError(BFP.EMPTY_GRAPH)

        if not G.has_vertex(s):
            raise IndexError(G.VERTEX_NOT_IN_GRAPH)
        
        # INIT INSTANCE ATTRS
        self._G = G
        self._s = s
        
        self._marked  = [ False          for _ in range(G.vertices_count) ]
        self._edge_to = [ None           for _ in range(G.vertices_count) ]
        self._dist_to = [ float("inf")   for _ in range(G.vertices_count) ]

        # SEARCH
        self._bfs(G, s)
    
    # ------------------------------- #
    # --- SEARCH

    def _bfs(self, G: Graph, s: int) -> None:
        q = SimpleQueue()
        q.put(s)
        self._marked[s]  = True
        self._dist_to[s] = 0

        while not q.empty():
            v = q.get()
            
            for w in G.adjacent_to(v):
                if not self._marked[w]:
                    q.put(w)
                    self._marked[w]  = True
                    self._edge_to[w] = v
                    self._dist_to[w] = self._dist_to[v] + 1

    # ------------------------------- #
    # --- HELPER METHODS/PROPERTIES

    def _validate_vertex(self, v) -> None:
        if not self._G.has_vertex(v):
            raise IndexError(self._G.VERTEX_NOT_IN_GRAPH)
    
    @property
    def _count(self) -> int:
        """Returns the count of connected vertices to source `s`."""
        return self._marked.count(True)

    # ------------------------------- #
    # --- PUBLIC API

    def has_path_to(self, v) -> bool:
        """Is vertex `v` connected to source `s`?"""
        self._validate_vertex(v)
        return self._marked[v]
    
    def path_to(self, v) -> list:
        """Returns the sortest path from `s` to `v`"""
        if not self.has_path_to(v):
            return None
        
        this_v = v
        path = []
        
        while this_v != self._s and self._edge_to[this_v] is not None:
            path.append(this_v)
            this_v = self._edge_to[this_v]
        
        path.append(self._s)
        path.reverse()
        return path

    def dist_to(self, v) -> int:
        self._validate_vertex(v)
        return self._dist_to[v]
    
#-------------------------------------------------------------------------------
# UNIT TESTING
#-------------------------------------------------------------------------------
import unittest

class TestsBFP(unittest.TestCase):
    def setUp(self) -> None:
        self.BFP = BFP

    # --- TESTS FOR INSTANTIATION 000
    def test_000_init_type_error_not_a_graph(self):
        with self.assertRaisesRegex(TypeError, self.BFP.NOT_A_GRAPH):
            self.BFP("G", 0)
    
    def test_001_init_empty_graph(self):
        G = Graph(0)
        with self.assertRaisesRegex(IndexError, BFP.EMPTY_GRAPH):
            self.BFP(G, 1)
    
    def test_002_init_type_error_not_a_integer(self):
        G = Graph(1)
        with self.assertRaisesRegex(TypeError, Graph.VERTEX_NOT_INTEGER):
            self.BFP(G, "0")
    
    def test_003_init_value_error_negative_integer(self):
        G = Graph(1)
        with self.assertRaisesRegex(ValueError, Graph.VERTEX_NOT_POSITIVE):
            self.BFP(G, -1)

    def test_004_init_vertex_not_in_graph(self):
        G = Graph(1)
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            self.BFP(G, 1)
    
    def test_005_init_instance_attrs_with_no_search(self):
        
        class BFP_DOUBLE(BFP):
            def _bfs(self, G: Graph, s: int) -> None:
                return
            
        s = 0
        for V in range(1, 10):
            G = Graph(V)
            bfp = BFP_DOUBLE(G, s)
            
            # assert graph `G` and source `s`
            self.assertIs(bfp._G, G)
            self.assertEqual(bfp._s, s)
            
            vertices_count = G.vertices_count

            # assert `_marked`
            self.assertEqual(len(bfp._marked), vertices_count)
            self.assertFalse(bfp._marked.count(True))

            # assert `_edge_to`
            self.assertEqual(len(bfp._edge_to), vertices_count)
            self.assertIsNone(*set(bfp._edge_to)) # only contains `None`
            
            # assert `_dist_to``
            self.assertEqual(len(bfp._dist_to), vertices_count)
            self.assertEqual(set(bfp._dist_to), {float("inf")})
    
    # --- TESTS FOR HELPER METHODS 100
    def test_100_validate_vertex(self):
        G = Graph(1)
        with self.assertRaisesRegex(TypeError, Graph.VERTEX_NOT_INTEGER):
            self.BFP(G, "0")
    
        with self.assertRaisesRegex(ValueError, Graph.VERTEX_NOT_POSITIVE):
            self.BFP(G, -1)

        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            self.BFP(G, 1)

    def test_101_count(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2

        bfp = self.BFP(G, v0)
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        bfp = self.BFP(G, v1)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        bfp = self.BFP(G, v2)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        
        G.add_edge(v0, v1)
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        bfp = self.BFP(G, v1)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        bfp = self.BFP(G, v2)
        self.assertEqual(bfp._count, bfp._marked.count(True))

        G.add_edge(v1, v2)
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        bfp = self.BFP(G, v1)
        self.assertEqual(bfp._count, bfp._marked.count(True))
        bfp = self.BFP(G, v2)
        self.assertEqual(bfp._count, bfp._marked.count(True))

    # --- TESTS FOR SEARCH 200
    def test_200_search_graph_with_no_edges(self):
        V = 5
        G = Graph(V)
        
        for s in range(G.vertices_count):
            bfp = self.BFP(G, s)

            vertices_count = G.vertices_count

            # assert `_marked`
            self.assertEqual(len(bfp._marked), vertices_count)
            self.assertEqual(bfp._count, 1) # `s` itself

            # assert `_edge_to`
            self.assertEqual(len(bfp._edge_to), vertices_count)
            self.assertIsNone(*set(bfp._edge_to)) # only contains `None`
            
            # assert `_dist_to``
            self.assertEqual(len(bfp._dist_to), vertices_count)
            self.assertEqual(set(bfp._dist_to), {0, float("inf")})
    
    def test_201_search_graph_with_only_one_edge(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        
        # source == v0
        bfp0 = self.BFP(G, v0)
        self.assertEqual(bfp0._count, 2)
        # v0
        self.assertIsNone(bfp0._edge_to[v0])
        self.assertEqual(bfp0._dist_to[v0], 0)
        # v1
        self.assertEqual(bfp0._edge_to[v1], v0)
        self.assertEqual(bfp0._dist_to[v1], 1)
        # v2
        self.assertIsNone(bfp0._edge_to[v2])
        self.assertEqual(bfp0._dist_to[v2], float("inf"))
        
        # source == v1
        bfp1 = self.BFP(G, v1)
        self.assertEqual(bfp1._count, 2)
        # v1
        self.assertIsNone(bfp1._edge_to[v1])
        self.assertEqual(bfp1._dist_to[v1], 0)
        # v0
        self.assertEqual(bfp1._edge_to[v0], v1)
        self.assertEqual(bfp1._dist_to[v0], 1)
        # v2
        self.assertEqual(bfp1._edge_to[v2], None)
        self.assertEqual(bfp1._dist_to[v2], float("inf"))
        
        # source == v2
        bfp2 = self.BFP(G, v2)
        self.assertEqual(bfp2._count, 1) # `v2` itself
        # v2
        self.assertIsNone(bfp2._edge_to[v2])
        self.assertEqual(bfp2._dist_to[v2], 0)
        # v0
        self.assertEqual(bfp2._edge_to[v0], None)
        self.assertEqual(bfp2._dist_to[v0], float("inf"))
        # v1
        self.assertEqual(bfp2._edge_to[v1], None)
        self.assertEqual(bfp2._dist_to[v1], float("inf"))
        
    def test_202_search_cyclic_graph(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        G.add_edge(v2, v0)
        
        # source == v0
        bfp0 = self.BFP(G, v0)
        self.assertEqual(bfp0._count, 3)
        # to v0
        self.assertIsNone(bfp0._edge_to[v0])
        self.assertEqual(bfp0._dist_to[v0], 0)
        # to v1
        self.assertIn(bfp0._edge_to[v1], [v0, v1])
        self.assertEqual(bfp0._dist_to[v1], 1)
        # to v2
        self.assertIn(bfp0._edge_to[v2], [v0, v1])
        self.assertEqual(bfp0._dist_to[v2], 1)
        
        # source == v1
        bfp1 = self.BFP(G, v1)
        self.assertEqual(bfp1._count, 3)
        # v1
        self.assertIsNone(bfp1._edge_to[v1])
        self.assertEqual(bfp1._dist_to[v1], 0)
        # v0
        self.assertEqual(bfp1._edge_to[v0], v1)
        self.assertEqual(bfp1._dist_to[v0], 1)
        # v2
        self.assertEqual(bfp1._edge_to[v2], v1)
        self.assertEqual(bfp1._dist_to[v2], 1)
        
        # source == v2
        bfp2 = self.BFP(G, v2)
        self.assertEqual(bfp2._count, 3)
        # v2
        self.assertIsNone(bfp2._edge_to[v2])
        self.assertEqual(bfp2._dist_to[v2], 0)
        # v0
        self.assertEqual(bfp2._edge_to[v0], v2)
        self.assertEqual(bfp2._dist_to[v0], 1)
        # v1
        self.assertEqual(bfp2._edge_to[v1], v2)
        self.assertEqual(bfp2._dist_to[v1], 1)
    
        # TESTS FOR PATH

    def test_203_search_graph_sequentially_connected_vertices(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        
        # source == v0
        bfp0 = self.BFP(G, v0)
        self.assertEqual(bfp0._count, 3)
        # to v0
        self.assertIsNone(bfp0._edge_to[v0])
        self.assertEqual(bfp0._dist_to[v0], 0)
        # to v1
        self.assertEqual(bfp0._edge_to[v1], v0)
        self.assertEqual(bfp0._dist_to[v1], 1)
        # to v2
        self.assertEqual(bfp0._edge_to[v2], v1)
        self.assertEqual(bfp0._dist_to[v2], 2)
        
        # source == v1
        bfp1 = self.BFP(G, v1)
        self.assertEqual(bfp1._count, 3)
        # v1
        self.assertIsNone(bfp1._edge_to[v1])
        self.assertEqual(bfp1._dist_to[v1], 0)
        # v0
        self.assertEqual(bfp1._edge_to[v0], v1)
        self.assertEqual(bfp1._dist_to[v0], 1)
        # v2
        self.assertEqual(bfp1._edge_to[v2], v1)
        self.assertEqual(bfp1._dist_to[v2], 1)
        
        # source == v2
        bfp2 = self.BFP(G, v2)
        self.assertEqual(bfp2._count, 3)
        # v2
        self.assertIsNone(bfp2._edge_to[v2])
        self.assertEqual(bfp2._dist_to[v2], 0)
        # v0
        self.assertEqual(bfp2._edge_to[v0], v1)
        self.assertEqual(bfp2._dist_to[v0], 2)
        # v1
        self.assertEqual(bfp2._edge_to[v1], v2)
        self.assertEqual(bfp2._dist_to[v1], 1)
    
        # TESTS FOR PATH

    # --- TESTS FOR API 300
    def test_300_has_path_to_vertex_not_in_graph(self):
        V = 2
        G = Graph(V)
        v0, v_not_in_graph = 0, 2
        bfp = self.BFP(G, v0)
        
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            bfp.has_path_to(v_not_in_graph)

    def test_301_has_path_to(self):
        V = 3
        G = Graph(V)
        v0, v1, v2 = 0, 1, 2
        G.add_edge(v0, v1)
        
        bfp0 = self.BFP(G, v0)
        self.assertTrue(bfp0.has_path_to(v0))      # itself
        self.assertTrue(bfp0.has_path_to(v1))      # v1 connected
        self.assertFalse(bfp0.has_path_to(v2))     # v2 not connected
        
        bfp1 = self.BFP(G, v1)
        self.assertTrue(bfp1.has_path_to(v0))      # v0 connected
        self.assertTrue(bfp1.has_path_to(v1))      # itself
        self.assertFalse(bfp1.has_path_to(v2))     # v2 not connected
        
        bfp2 = self.BFP(G, v2)
        self.assertFalse(bfp2.has_path_to(v0))     # v0 not connected
        self.assertFalse(bfp2.has_path_to(v1))     # v1 not connected
        self.assertTrue(bfp2.has_path_to(v2))      # itself
    
    def test_302_path_to_vertex_not_in_graph(self):
        V = 2
        G = Graph(V)
        v0, v_not_in_graph = 0, 2
        bfp = self.BFP(G, v0)
        
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            bfp.path_to(v_not_in_graph)
    
    def test_303_path_to_vertex_not_connected(self):
        V = 2
        G = Graph(V)
        v0, v_not_connected = 0, 1
        bfp = self.BFP(G, v0)
        self.assertIsNone(bfp.path_to(v_not_connected))

    def test_304_path_to_sequentially_connected_vertices(self):
        V = 4
        G = Graph(V)
        v0, v1, v2, v3 = range(V)
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        G.add_edge(v2, v3)
        
        # source == v0
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp.path_to(v0), [v0])
        self.assertEqual(bfp.path_to(v1), [v0, v1])
        self.assertEqual(bfp.path_to(v2), [v0, v1, v2])
        self.assertEqual(bfp.path_to(v3), [v0, v1, v2, v3])

        # source == v1
        bfp = self.BFP(G, v1)
        self.assertEqual(bfp.path_to(v0), [v1, v0])
        self.assertEqual(bfp.path_to(v1), [v1])
        self.assertEqual(bfp.path_to(v2), [v1, v2])
        self.assertEqual(bfp.path_to(v3), [v1, v2, v3])

        # source == v2
        bfp = self.BFP(G, v2)
        self.assertEqual(bfp.path_to(v0), [v2, v1, v0])
        self.assertEqual(bfp.path_to(v1), [v2, v1])
        self.assertEqual(bfp.path_to(v2), [v2])
        self.assertEqual(bfp.path_to(v3), [v2, v3])

        # source == v3
        bfp = self.BFP(G, v3)
        self.assertEqual(bfp.path_to(v0), [v3, v2, v1, v0])
        self.assertEqual(bfp.path_to(v1), [v3, v2, v1])
        self.assertEqual(bfp.path_to(v2), [v3, v2])
        self.assertEqual(bfp.path_to(v3), [v3])

    def test_305_path_to_cyclic_graph(self):
        V = 4
        G = Graph(V)
        v0, v1, v2, v3 = range(V)
        G.add_edge(v0, v1)
        G.add_edge(v1, v2)
        G.add_edge(v2, v3)
        G.add_edge(v3, v0)
        
        # source == v0
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp.path_to(v0), [v0])
        self.assertEqual(bfp.path_to(v1), [v0, v1])
        self.assertEqual(bfp.path_to(v2), [v0, v1, v2])
        self.assertIn(bfp.path_to(v2), ([v0, v1, v2], [v0, v3, v2]))
        self.assertEqual(bfp.path_to(v3), [v0, v3])

        # source == v1
        bfp = self.BFP(G, v1)
        self.assertEqual(bfp.path_to(v0), [v1, v0])
        self.assertEqual(bfp.path_to(v1), [v1])
        self.assertEqual(bfp.path_to(v2), [v1, v2])
        self.assertIn(bfp.path_to(v3), ([v1, v2, v3], [v1, v0, v3]))

        # source == v2
        bfp = self.BFP(G, v2)
        self.assertEqual(bfp.path_to(v0), [v2, v1, v0])
        self.assertEqual(bfp.path_to(v1), [v2, v1])
        self.assertEqual(bfp.path_to(v2), [v2])
        self.assertEqual(bfp.path_to(v3), [v2, v3])

        # source == v3
        bfp = self.BFP(G, v3)
        self.assertEqual(bfp.path_to(v0), [v3, v0])
        self.assertIn(bfp.path_to(v1), ([v3, v2, v1], [v3, v0, v1]))
        self.assertEqual(bfp.path_to(v2), [v3, v2])
        self.assertEqual(bfp.path_to(v3), [v3])
    
        # TESTS FOR PATH
    
    def test_306_path_to_many_paths(self):
        V = 6
        G = Graph(V)
        v0, v1, v2, v3, v4, v5 = range(V)
        G.add_edge(v0, v1)
        G.add_edge(v1, v3)
        G.add_edge(v3, v4)
        G.add_edge(v0, v2)
        G.add_edge(v2, v4)
        G.add_edge(v4, v5)

        """
            (v1)--(v3)
            /         \
        (v0)---(v2)----(v4)--(v5)
        
        """
        
        # source == v0
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp.path_to(v3), [v0, v1, v3])
        self.assertEqual(bfp.path_to(v4), [v0, v2, v4])
        self.assertEqual(bfp.path_to(v5), [v0, v2, v4, v5])

    def test_307_dist_to_vertex_not_connected(self):
        V = 2
        G = Graph(V)
        v0, v_not_connected = range(V)
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp.dist_to(v_not_connected), float("inf"))

    def test_308_dist_to_many_vertices(self):
        V = 9
        G = Graph(V)
        v0, v1, v2, v3, v4, v5, v6, v7, v8 = range(V)
        G.add_edge(v0, v1)
        G.add_edge(v1, v3)
        G.add_edge(v3, v4)
        G.add_edge(v0, v2)
        G.add_edge(v2, v4)
        G.add_edge(v4, v5)
        G.add_edge(v3, v7)
        G.add_edge(v7, v8)
        G.add_edge(v5, v6)
        G.add_edge(v6, v8)

        """
            (v1)--(v3)--------------(v7)
            /         \                 \
        (v0)---(v2)----(v4)--(v5)--(v6)--(v8)
        
        """
        # source == v0
        bfp = self.BFP(G, v0)
        self.assertEqual(bfp.dist_to(v3), 2)
        self.assertEqual(bfp.dist_to(v4), 2)
        self.assertEqual(bfp.dist_to(v5), 3)
        self.assertEqual(bfp.dist_to(v6), 4)
        self.assertEqual(bfp.dist_to(v7), 3)
        self.assertEqual(bfp.dist_to(v8), 4)
