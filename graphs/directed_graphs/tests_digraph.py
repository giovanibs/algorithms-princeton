import unittest
from digraph import Digraph

class TestsDigraph(unittest.TestCase):
    def test_000_init_graph(self):
        V = 3
        dg = Digraph(V)
        self.assertEqual( dg._vertex_count        , V)
        self.assertEqual( len(dg._directed_out_of), V)
        self.assertEqual( len(dg._directed_into)  , V)
    
    def test_001_init_graph__not_integer(self):
        V = "3"
        with self.assertRaisesRegex(ValueError, Digraph.INIT_V_NOT_INTEGER):
            Digraph(V)
            
    def test_002_init_graph__negative_integer(self):
        V = -3
        with self.assertRaisesRegex(ValueError, Digraph.INIT_V_NOT_POSITIVE):
            Digraph(V)

    def test_010_add_vertex(self):
        V = 0
        dg = Digraph(V)
        len_old_outgoing = len(dg._directed_out_of)
        len_old_incoming = len(dg._directed_into  )
        old_vertex_count = dg.vertex_count

        new_vertex       = dg.add_vertex()
        len_new_outgoing = len(dg._directed_out_of)
        len_new_incoming = len(dg._directed_into  )
        new_vertex_count = dg.vertex_count

        self.assertEqual( new_vertex        , old_vertex_count     )
        self.assertEqual( len_new_outgoing  , len_old_outgoing  + 1)
        self.assertEqual( len_new_outgoing  , len_old_outgoing  + 1)
        self.assertEqual( len_new_incoming  , len_old_incoming  + 1)
        self.assertEqual( new_vertex_count  , old_vertex_count  + 1)
    
    def test_020_add_edge(self):
        V = 2
        dg = Digraph(V)
        v, w = 0, 1
        
        # NO EDGE
        self.assertFalse( w in dg._directed_out_of[v] )
        self.assertFalse( w in dg._directed_into  [v] )
        self.assertFalse( v in dg._directed_out_of[w] )
        self.assertFalse( v in dg._directed_into  [w] )

        self.assertEqual( dg._edge_count , 0 )
        self.assertEqual( dg.outdegree(v), 0 )
        self.assertEqual( dg.outdegree(w), 0 )
        self.assertEqual( dg.indegree(v) , 0 )
        self.assertEqual( dg.indegree(w) , 0 )

        # ADD EDGE v -> w
        dg.add_edge(v, w)
        self.assertTrue ( w in dg._directed_out_of[v] )
        self.assertTrue ( v in dg._directed_into  [w] )
        self.assertFalse( w in dg._directed_into  [v] )
        self.assertFalse( v in dg._directed_out_of[w] )

        self.assertEqual( dg._edge_count , 1 )
        self.assertEqual( dg.outdegree(v), 1 )
        self.assertEqual( dg.indegree (v), 0 )
        self.assertEqual( dg.outdegree(w), 0 )
        self.assertEqual( dg.indegree (w), 1 )
        
        # ADD EDGE w -> v
        dg.add_edge(w, v)
        self.assertTrue( w in dg._directed_out_of[v] )
        self.assertTrue( w in dg._directed_into  [v] )
        self.assertTrue( v in dg._directed_out_of[w] )
        self.assertTrue( v in dg._directed_into  [w] )

        self.assertEqual( dg._edge_count , 2 )
        self.assertEqual( dg.outdegree(v), 1 )
        self.assertEqual( dg.outdegree(w), 1 )
        self.assertEqual( dg.indegree(v) , 1 )
        self.assertEqual( dg.indegree(w) , 1 )

    def test_021_add_edge__vertex_not_in_graph(self):
        V = 1
        graph = Digraph(V)
        vertex_not_in_graph = 1
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            graph.add_edge(0, vertex_not_in_graph)

        self.assertEqual(graph._edge_count, 0)
    
    def test_022_add_edge__vertex_not_integer(self):
        V = 3
        graph = Digraph(V)
        vertex_not_integer = "1"
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            graph.add_edge(0, vertex_not_integer)
    
    def test_022_add_edge__vertex_not_positive_integer(self):
        V = 3
        graph = Digraph(V)
        vertex_not_positive = -1
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            graph.add_edge(0, vertex_not_positive)

    def test_023_add_edge__existing_edge(self):
        V = 2
        dg = Digraph(V)
        v, w = 0, 1
        dg.add_edge(v, w) # v -> w

        old_edge_count  = dg._edge_count
        old_outdegree_v = dg.outdegree(v)
        old_indegree_w  = dg.indegree(w)
        
        dg.add_edge(v, w) # ADD SAME EDGE AS BEFORE
        
        new_edge_count  = dg._edge_count
        new_outdegree_v = dg.outdegree(v)
        new_indegree_w  = dg.indegree(w)
        
        self.assertEqual( new_edge_count , old_edge_count )
        self.assertEqual( new_outdegree_v, old_outdegree_v)
        self.assertEqual( new_indegree_w , old_indegree_w )

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

    def test_050_outdegree__vertex_not_in_graph(self):
        V = 1
        dg = Digraph(V)
        vertex_not_in_graph = 1
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            dg.outdegree(vertex_not_in_graph)

    def test_051_outdegree__vertex_not_positive_integer(self):
        V = 3
        dg = Digraph(V)
        vertex_not_positive = -1
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            dg.outdegree(vertex_not_positive)
    
    def test_052_outdegree__vertex_not_integer(self):
        V = 3
        dg = Digraph(V)
        vertex_not_integer = "1"
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            dg.outdegree(vertex_not_integer)

    def test_053_outdegree(self):
        V = 3
        dg = Digraph(V)
        v0, v1, v2 = range(3)
        self.assertEqual(dg.outdegree(v0), 0)
        dg.add_edge(v0, v1)
        self.assertEqual(dg.outdegree(v0), 1)
        dg.add_edge(v0, v2)
        self.assertEqual(dg.outdegree(v0), 2)
        dg.add_edge(v2, v0)
        self.assertEqual(dg.outdegree(v0), 2)

    def test_060_indegree__vertex_not_in_graph(self):
        V = 1
        dg = Digraph(V)
        vertex_not_in_graph = 1
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            dg.indegree(vertex_not_in_graph)

    def test_061_indegree__vertex_not_positive_integer(self):
        V = 3
        dg = Digraph(V)
        vertex_not_positive = -1
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            dg.indegree(vertex_not_positive)
    
    def test_062_indegree__vertex_not_integer(self):
        V = 3
        dg = Digraph(V)
        vertex_not_integer = "1"
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            dg.indegree(vertex_not_integer)

    def test_063_indegree(self):
        V = 3
        dg = Digraph(V)
        v0, v1, v2 = range(3)
        self.assertEqual(dg.indegree(v0), 0)
        dg.add_edge(v1, v0)
        self.assertEqual(dg.indegree(v0), 1)
        dg.add_edge(v2, v0)
        self.assertEqual(dg.indegree(v0), 2)
        dg.add_edge(v0, v1)
        self.assertEqual(dg.indegree(v0), 2)

    def test_070_directed_out_of(self):
        V = 3
        dg = Digraph(V)
        empty_set = set()
        expected_0 = empty_set
        expected_1 = empty_set
        expected_2 = empty_set
        self.assertEqual(expected_0, dg.directed_out_of(0))
        self.assertEqual(expected_1, dg.directed_out_of(1))
        self.assertEqual(expected_2, dg.directed_out_of(2))

        dg.add_edge(0, 1) # 0 -> 1
        expected_0 = {1}
        expected_1 = empty_set
        expected_2 = empty_set
        self.assertEqual(expected_0, dg.directed_out_of(0))
        self.assertEqual(expected_1, dg.directed_out_of(1))
        self.assertEqual(expected_2, dg.directed_out_of(2))
        
        dg.add_edge(1, 2) # 1 -> 2
        expected_0 = {1}
        expected_1 = {2}
        expected_2 = empty_set
        self.assertEqual(expected_0, dg.directed_out_of(0))
        self.assertEqual(expected_1, dg.directed_out_of(1))
        self.assertEqual(expected_2, dg.directed_out_of(2))
        
        dg.add_edge(2, 0) # 2 -> 0
        expected_0 = {1}
        expected_1 = {2}
        expected_2 = {0}
        self.assertEqual(expected_0, dg.directed_out_of(0))
        self.assertEqual(expected_1, dg.directed_out_of(1))
        self.assertEqual(expected_2, dg.directed_out_of(2))

        dg.add_edge(0, 2) # 0 -> 2
        expected_0 = {1, 2}
        expected_1 = {2}
        expected_2 = {0}
        self.assertEqual(expected_0, dg.directed_out_of(0))
        self.assertEqual(expected_1, dg.directed_out_of(1))
        self.assertEqual(expected_2, dg.directed_out_of(2))

    def test_071_directed_out_of__vertex_not_in_graph(self):
        V = 3
        graph = Digraph(V)
    
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            graph.directed_out_of(3)
    
    def test_080_directed_into(self):
        V = 3
        dg = Digraph(V)
        empty_set = set()
        expected_0 = empty_set
        expected_1 = empty_set
        expected_2 = empty_set
        self.assertEqual(expected_0, dg.directed_into(0))
        self.assertEqual(expected_1, dg.directed_into(1))
        self.assertEqual(expected_2, dg.directed_into(2))

        dg.add_edge(1, 0) # 1 -> 0
        expected_0 = {1}
        self.assertEqual(expected_0, dg.directed_into(0))
        self.assertEqual(expected_1, dg.directed_into(1))
        self.assertEqual(expected_2, dg.directed_into(2))
        
        dg.add_edge(2, 1) # 2 -> 1
        expected_1 = {2}
        self.assertEqual(expected_0, dg.directed_into(0))
        self.assertEqual(expected_1, dg.directed_into(1))
        self.assertEqual(expected_2, dg.directed_into(2))
        
        dg.add_edge(0, 2) # 0 -> 2
        expected_2 = {0}
        self.assertEqual(expected_0, dg.directed_into(0))
        self.assertEqual(expected_1, dg.directed_into(1))
        self.assertEqual(expected_2, dg.directed_into(2))

        dg.add_edge(2, 0) # 2 -> 0
        expected_0 = {1, 2}
        self.assertEqual(expected_0, dg.directed_into(0))
        self.assertEqual(expected_1, dg.directed_into(1))
        self.assertEqual(expected_2, dg.directed_into(2))

    def test_081_directed_into__vertex_not_in_graph(self):
        V = 3
        graph = Digraph(V)
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            graph.directed_into(3)

    def test_090_reverse__no_edges(self):
        V = 2
        v0, v1 = range(V)
        dg = Digraph(V)
        dg_r = dg.reverse()
        self.assertEqual( dg_r.vertex_count, dg.vertex_count )
        self.assertEqual( dg_r.edge_count  , dg.edge_count   )
        
        self.assertListEqual(dg_r._directed_out_of, dg._directed_out_of)
        self.assertListEqual(dg_r._directed_into  , dg._directed_into  )
    
    def test_091_reverse__single_edge(self):
        V = 2
        v0, v1 = range(V)
        dg = Digraph(V)
        dg.add_edge(v0, v1)
        dg_r = dg.reverse()
        
        # not changed
        self.assertEqual( dg_r.edge_count           , dg.edge_count            )
        self.assertEqual( dg_r.vertex_count         , dg.vertex_count          )
        self.assertEqual( len(dg_r._directed_into)  , len(dg._directed_into)   )
        self.assertEqual( len(dg_r._directed_out_of), len(dg._directed_out_of) )
        
        # changed
        self.assertEqual( dg_r.outdegree(v0)      , dg.outdegree(v1)       )
        self.assertEqual( dg_r.indegree (v0)      , dg.indegree (v1)       )
        self.assertEqual( dg_r.outdegree(v1)      , dg.outdegree(v0)       )
        self.assertEqual( dg_r.indegree (v1)      , dg.indegree (v0)       )
        self.assertEqual( dg_r.directed_out_of(v0), dg.directed_into(v0) )
        self.assertEqual( dg_r.directed_out_of(v1), dg.directed_into(v1) )
    
    def test_092_reverse__parallel_edges(self):
        V = 2
        v0, v1 = range(V)
        dg = Digraph(V)
        dg.add_edge(v0, v1)
        dg.add_edge(v1, v0)
        dg_r = dg.reverse()
        
        # not changed
        self.assertEqual( dg_r.edge_count           , dg.edge_count            )
        self.assertEqual( dg_r.vertex_count         , dg.vertex_count          )
        self.assertEqual( len(dg_r._directed_into)  , len(dg._directed_into)   )
        self.assertEqual( len(dg_r._directed_out_of), len(dg._directed_out_of) )

        # "changed"
        self.assertEqual( dg_r.indegree (v0), dg.outdegree(v0))
        self.assertEqual( dg_r.indegree (v1), dg.outdegree(v1))
        self.assertEqual( dg_r.outdegree(v0), dg.indegree (v0) )
        self.assertEqual( dg_r.outdegree(v1), dg.indegree (v1) )
    
    def test_093_reverse__simple_directed_path(self):
        V = 3
        v0, v1, v2= range(V)
        dg = Digraph(V)
        dg.add_edge(v0, v1)
        dg.add_edge(v1, v2)
        dg_r = dg.reverse()
        
        # "changed"
        self.assertEqual( dg_r.outdegree(v0), dg.indegree(v0) )
        self.assertEqual( dg_r.outdegree(v1), dg.indegree(v1) )
        self.assertEqual( dg_r.outdegree(v2), dg.indegree(v2) )
        self.assertEqual( dg_r.indegree(v0) , dg.outdegree(v0) )
        self.assertEqual( dg_r.indegree(v1) , dg.outdegree(v1) )
        self.assertEqual( dg_r.indegree(v2) , dg.outdegree(v2) )
