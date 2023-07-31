import unittest
from undirected_graph import Graph

class TestsUndirectedGraph(unittest.TestCase):
    def test_000_init_graph(self):
        V = 3
        graph = Graph(V)
        self.assertEqual(graph._V, V)
        self.assertEqual(len(graph._adj), V)
    
    def test_001_init_graph_not_int(self):
        V = "3"
        with self.assertRaisesRegex(ValueError, Graph.INIT_V_NOT_INTEGER):
            Graph(V)
            
    def test_002_init_graph_negative_int(self):
        V = -3
        with self.assertRaisesRegex(ValueError, Graph.INIT_V_NOT_POSITIVE):
            Graph(V)

    def test_010_add_vertex(self):
        V = 3
        graph = Graph(V)
        graph.add_vertex()
        self.assertEqual(graph._V, V+1)

    def test_020_add_edge(self):
        V = 3
        graph = Graph(V)
        v = 0
        w = 1
        graph.add_edge(v, w)
        self.assertEqual(graph._E, 1)
        self.assertTrue(w in graph._adj[v])
        self.assertTrue(v in graph._adj[w])

    def test_021_add_edge_vertex_not_in_graph(self):
        V = 3
        graph = Graph(V)
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            graph.add_edge(0, 3)
        self.assertEqual(graph._E, 0)
    
    def test_022_add_edge_vertex_not_integer(self):
        V = 3
        graph = Graph(V)
        with self.assertRaisesRegex(ValueError, Graph.VERTEX_NOT_INTEGER):
            graph.add_edge(0, "2")
    
    def test_022_add_edge_vertex_not_positive_integer(self):
        V = 3
        graph = Graph(V)
        with self.assertRaisesRegex(ValueError, Graph.VERTEX_NOT_POSITIVE):
            graph.add_edge(0, -1)

    def test_030_vertices_count(self):
        V = 3
        graph = Graph(V)
        self.assertEqual(graph.vertices_count, V)
    
    def test_040_edges_count(self):
        V = 3
        graph = Graph(V)
        self.assertEqual(graph.edges_count, 0)
        graph.add_edge(0, 1)
        self.assertEqual(graph.edges_count, 1)
        graph.add_edge(0, 2)
        self.assertEqual(graph.edges_count, 2)

    def test_050_adjacent_to(self):
        V = 3
        graph = Graph(V)
        empty_set = set()
        expected_0 = empty_set
        expected_1 = empty_set
        expected_2 = empty_set
        self.assertEqual(expected_0, graph.adjacent_to(0))
        self.assertEqual(expected_1, graph.adjacent_to(1))
        self.assertEqual(expected_2, graph.adjacent_to(2))

        graph.add_edge(0, 1)
        expected_0 = {1}
        expected_1 = {0}
        expected_2 = empty_set
        self.assertEqual(expected_0, graph.adjacent_to(0))
        self.assertEqual(expected_1, graph.adjacent_to(1))
        self.assertEqual(expected_2, graph.adjacent_to(2))
        
        graph.add_edge(1, 2)
        expected_0 = {1}
        expected_1 = {0, 2}
        expected_2 = {1}
        self.assertEqual(expected_0, graph.adjacent_to(0))
        self.assertEqual(expected_1, graph.adjacent_to(1))
        self.assertEqual(expected_2, graph.adjacent_to(2))

    def test_051_adjacent_to_vertex_not_in_graph(self):
        V = 3
        graph = Graph(V)
        with self.assertRaisesRegex(IndexError, Graph.VERTEX_NOT_IN_GRAPH):
            graph.adjacent_to(3)
