from digraph import Digraph
from tests_digraph import TestsDigraph

class DigraphDFS:
    """
    The class DirectedDFS serves as a data structure
    designed to identify the vertices that can be
    reached from a specified source vertex (or a
    group of source vertices) within a directed graph.

    This approach employs a depth-first search technique.
    """
    CONNECTED     = True
    NOT_A_DIGRAPH = "First argument must be a Digraph object."

    def __init__(self, DG: Digraph, source: int|set[int]) -> None:
        # validation
        if not isinstance(DG, Digraph):
            raise TypeError(DigraphDFS.NOT_A_DIGRAPH)
        
        if not isinstance(source, set):
            source = {source}

        for s in source:
            if not DG.has_vertex(s):
                raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        # init
        self._S : int|set = source
        self._DG: Digraph = DG

        self._marked : list[bool]     = [ False for _ in range(DG.vertex_count)]
        self._edge_to: list[int|None] = [ None  for _ in range(DG.vertex_count)]
        
        # search
        for s in source:
            if not self._marked[s]:
                self._dfs(DG, s)
    
    # ------------------------------- #
    # --- SEARCH
    def _dfs(self, DG: Digraph, v: int) -> None:
        self._marked[v] = True

        for w in DG.directed_out_of(v):
            if not self._marked[w]:
                self._edge_to[w] = v
                self._dfs(DG, w)

    # ------------------------------- #
    # --- PUBLIC API
    def is_reachable(self, v: int) -> bool:
        """ Is there a directed path from source to vertex `v`?"""
        if not self._DG.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return self._marked[v]
    
    @property
    def count(self) -> int:
        """Returns number of vertices with an incoming
        path from source `s`.
        Considers the source itself."""
        return self._marked.count(DigraphDFS.CONNECTED)
    

import unittest

class TestsDigraphDFS(unittest.TestCase):
    def setUp(self) -> None:
        V = 7
        self.G = Digraph(V)
        (   self.source,
            self.strictly_into,
            self.strictly_out_of,
            self.double_linked,
            self.one_from_source,
            self.two_from_source,
            self.not_connected      ) = range(V) 
        
        self.not_in_graph = V

        # strictly in/outbound
        self.G.add_edge( self.source         , self.strictly_into )
        self.G.add_edge( self.strictly_out_of, self.source        )
        
        # double link
        self.G.add_edge( self.source       , self.double_linked )
        self.G.add_edge( self.double_linked, self.source        )
        
        # directed path
        self.G.add_edge( self.source         , self.one_from_source )
        self.G.add_edge( self.one_from_source, self.two_from_source )

        self.dfs = DigraphDFS(self.G, self.source)

    def test_000_init__type_error_not_a_digraph(self):
        with self.assertRaisesRegex(TypeError, DigraphDFS.NOT_A_DIGRAPH):
            DigraphDFS("G", 0)
    
    def test_001_init__type_error_not_a_integer(self):
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            DigraphDFS(self.G, "0")
    
    def test_002_init__value_error_negative_integer(self):
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            DigraphDFS(self.G, -1)

    def test_003_init__source_not_in_graph(self):
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            DigraphDFS(self.G, self.not_in_graph)
    
    def test_004_init__expected_attrs_without_dfs(self):
        class DigraphDFSDouble(DigraphDFS):
            def _dfs(self, DG: Digraph, v: int) -> None:
                return
        
        source = {0}

        for V in range(1, 10):
            dg  = Digraph(V)
            dfs = DigraphDFSDouble(dg, source)

            self.assertEqual( dfs._S           , source )
            self.assertEqual( dfs._DG          , dg     )
            self.assertEqual( len(dfs._marked) , V      )
            self.assertEqual( len(dfs._edge_to), V      )
    
    def test_005_init__expected_attrs(self):
        source = {0}

        for V in range(1, 10):
            dg  = Digraph(V)
            dfs = DigraphDFS(dg, source)

            self.assertEqual( dfs._S           , source )
            self.assertEqual( dfs._DG          , dg     )
            self.assertEqual( len(dfs._marked) , V      )
            self.assertEqual( len(dfs._edge_to), V      )
    
    def test_100_dfs__graph_with_no_edges(self):
        V = 5
        G = Digraph(V)
        
        for v in range(G.vertex_count):
            dfs = DigraphDFS(G, v)
            self.assertEqual(dfs.count, 1) # only the vertex itself
    
    def test_101_dfs(self):
        self.assertTrue ( self.dfs._marked[ self.one_from_source ] )
        self.assertTrue ( self.dfs._marked[ self.two_from_source ] )
        self.assertTrue ( self.dfs._marked[ self.strictly_into   ] )
        self.assertTrue ( self.dfs._marked[ self.double_linked   ] )
        self.assertFalse( self.dfs._marked[ self.strictly_out_of ] )
        self.assertFalse( self.dfs._marked[ self.not_connected   ] )
        
    def test_102_dfs__source_is_strictly_inbound_vertex(self):
        self.assertTrue     ( self.dfs._marked [self.strictly_into] )
        self.assertIsNotNone( self.dfs._edge_to[self.strictly_into] )

        dfs = DigraphDFS(self.G, self.strictly_into)
        self.assertTrue( any(dfs._marked[1:]) )         # except itself 

    def test_103_dfs__source_is_strictly_outbound_vertex(self):
        self.assertFalse ( self.dfs._marked [self.strictly_out_of] )
        self.assertIsNone( self.dfs._edge_to[self.strictly_out_of] )

        dfs = DigraphDFS(self.G, self.strictly_out_of)
        self.assertTrue( all(dfs._marked[:-1]) )     # all except not_connected
        
    def test_104_dfs__source_is_double_linked(self):
        original_source = self.source
        double_linked   = self.double_linked

        dfs = DigraphDFS(self.G, double_linked)
        self.assertTrue ( dfs._marked[original_source] )
        self.assertEqual( dfs._edge_to[original_source], double_linked )
    
    def test_105_dfs__source_is_directed_path(self):
        old_source      = self.source
        two_from_source = self.two_from_source
        one_from_source = self.one_from_source
        
        dfs = DigraphDFS(self.G, one_from_source)
        self.assertFalse( dfs._marked[old_source]           )
        self.assertTrue ( dfs._marked[two_from_source] )
        
        dfs = DigraphDFS(self.G, two_from_source)
        self.assertFalse( dfs._marked[old_source]           )
        self.assertFalse( dfs._marked[self.one_from_source] )

    def test_200_is_reachable__a_vertex_not_in_graph(self):
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            self.dfs.is_reachable(self.not_in_graph)
    
    def test_201_is_reachable(self):
        self.assertTrue ( self.dfs.is_reachable( self.one_from_source ) )
        self.assertTrue ( self.dfs.is_reachable( self.two_from_source ) )
        self.assertTrue ( self.dfs.is_reachable( self.strictly_into   ) )
        self.assertTrue ( self.dfs.is_reachable( self.double_linked   ) )
        self.assertFalse( self.dfs.is_reachable( self.strictly_out_of ) )
        self.assertFalse( self.dfs.is_reachable( self.not_connected   ) )
