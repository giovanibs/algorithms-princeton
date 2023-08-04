import unittest
from digraph import Digraph

class TestsUndirectedDigraph(unittest.TestCase):
    def test_000_init_graph(self):
        V = 3
        graph = Digraph(V)
        self.assertEqual(graph._vertex_count, V)
        self.assertEqual(len(graph._outgoing), V)
    
    def test_001_init_graph_not_int(self):
        V = "3"
        with self.assertRaisesRegex(ValueError, Digraph.INIT_V_NOT_INTEGER):
            Digraph(V)
            
    def test_002_init_graph_negative_int(self):
        V = -3
        with self.assertRaisesRegex(ValueError, Digraph.INIT_V_NOT_POSITIVE):
            Digraph(V)

    def test_010_add_vertex(self):
        V = 3
        graph = Digraph(V)
        graph.add_vertex()
        self.assertEqual(graph._vertex_count, V+1)

    def test_020_add_edge(self):
        V = 3
        graph = Digraph(V)
        v = 0
        w = 1
        graph.add_edge(v, w) # v -> w
        self.assertEqual(graph._edge_count, 1)
        self.assertTrue(w in graph._outgoing[v])
        self.assertFalse(v in graph._outgoing[w])
        
        graph.add_edge(w, v) # w -> v
        self.assertEqual(graph._edge_count, 2)
        self.assertTrue(w in graph._outgoing[v])
        self.assertTrue(v in graph._outgoing[w])

    def test_021_add_edge_vertex_not_in_graph(self):
        V = 3
        graph = Digraph(V)
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            graph.add_edge(0, 3)
        self.assertEqual(graph._edge_count, 0)
    
    def test_022_add_edge_vertex_not_integer(self):
        V = 3
        graph = Digraph(V)
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            graph.add_edge(0, "2")
    
    def test_022_add_edge_vertex_not_positive_integer(self):
        V = 3
        graph = Digraph(V)
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            graph.add_edge(0, -1)

    def test_030_vertex_count(self):
        V = 3
        graph = Digraph(V)
        self.assertEqual(graph.vertex_count, V)
    
    def test_040_edge_count(self):
        V = 3
        graph = Digraph(V)
        self.assertEqual(graph.edge_count, 0)
        graph.add_edge(0, 1)
        self.assertEqual(graph.edge_count, 1)
        graph.add_edge(0, 2)
        self.assertEqual(graph.edge_count, 2)

    def test_050_outgoing_from(self):
        V = 3
        graph = Digraph(V)
        empty_set = set()
        expected_0 = empty_set
        expected_1 = empty_set
        expected_2 = empty_set
        self.assertEqual(expected_0, graph.outgoing_from(0))
        self.assertEqual(expected_1, graph.outgoing_from(1))
        self.assertEqual(expected_2, graph.outgoing_from(2))

        graph.add_edge(0, 1) # 0 -> 1
        expected_0 = {1}
        expected_1 = empty_set
        expected_2 = empty_set
        self.assertEqual(expected_0, graph.outgoing_from(0))
        self.assertEqual(expected_1, graph.outgoing_from(1))
        self.assertEqual(expected_2, graph.outgoing_from(2))
        
        graph.add_edge(1, 2) # 1 -> 2
        expected_0 = {1}
        expected_1 = {2}
        expected_2 = empty_set
        self.assertEqual(expected_0, graph.outgoing_from(0))
        self.assertEqual(expected_1, graph.outgoing_from(1))
        self.assertEqual(expected_2, graph.outgoing_from(2))
        
        graph.add_edge(2, 0) # 2 -> 0
        expected_0 = {1}
        expected_1 = {2}
        expected_2 = {0}
        self.assertEqual(expected_0, graph.outgoing_from(0))
        self.assertEqual(expected_1, graph.outgoing_from(1))
        self.assertEqual(expected_2, graph.outgoing_from(2))

        graph.add_edge(0, 2) # 0 -> 2
        expected_0 = {1, 2}
        expected_1 = {2}
        expected_2 = {0}
        self.assertEqual(expected_0, graph.outgoing_from(0))
        self.assertEqual(expected_1, graph.outgoing_from(1))
        self.assertEqual(expected_2, graph.outgoing_from(2))

    def test_051_outgoing_from_vertex_not_in_graph(self):
        V = 3
        graph = Digraph(V)
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            graph.outgoing_from(3)
