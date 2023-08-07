from digraph import Digraph
from tests_digraph import TestsDigraph

class DigraphBFP:
    """
    The class DirectedBFP serves as a data structure
    designed to identify the shortest paths from a
    specified source vertex (or a group of source
    vertices) to every other vertex in a digraph.

    It is the same method as for undirected graphs,
    given that every undirected graph is a digraph
    with edges in both directions.
    
    BFS is a digraph algorithm.
    """
    CONNECTED     = True
    NOT_A_DIGRAPH = "First argument must be a Digraph object."

    def __init__(self, DG: Digraph, sources: int|set[int]) -> None:
        # --- VALIDATION --- #
        if not isinstance(DG, Digraph):
            raise TypeError(DigraphBFP.NOT_A_DIGRAPH)
        
        if not isinstance(sources, set):
            sources = {sources}
        
        for s in sources:
            # positive integer validation is in `DG.has_vertex``
            if not DG.has_vertex(s):
                raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        # --- INIT --- #
        self._S : set[int]= sources
        self._DG: Digraph = DG

        self._marked : list[bool]     = [ False for _ in range(DG.vertex_count)]
        self._edge_to: list[int|None] = [ None  for _ in range(DG.vertex_count)]
        self._dist_to: list[int|None] = self._edge_to.copy()
        
        # --- SEARCH --- #
        self._bfs(DG, sources)

    def _bfs(self, DG: Digraph, sources: set[int]):
        """
        Put `sources` onto a FIFO queue and mark them as visited.
        Repeat until the queue is empty:
            - remove the least recently added vertex `v`
            - for each unmarked vertex pointing from `v`:
            add to queue and mark it as visited.
        """
        # FIFO qeeue
        q = []

        for s in sources:
            q.append(s)
            self._marked[s]  = True
            self._dist_to[s] = 0

        while q: # until the queue is empty
            v = q.pop(0)
            
            for w in self._DG.directed_out_of(v):
                if not self._marked[w]:
                    self._marked[w]  = True
                    self._edge_to[w] = v
                    self._dist_to[w] = self._dist_to[v] + 1
                    q.append(w)

    # ------------------------------- #
    # --- PUBLIC API
    def is_reachable(self, v: int) -> bool:
        """ Is there a directed path from source to vertex `v`?"""
        if not self._DG.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return self._marked[v]
    
    def shortest_path_to(self, v: int) -> None | list:
        if not self._DG.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        if not self.is_reachable(v):
            return None
        
        shortest_path = [v]
        w = v

        while w not in self._S:
            w = self._edge_to[w]
            shortest_path.append(w)

        return shortest_path[::-1]

    @property
    def count(self) -> int:
        """Returns number of vertices with an incoming
        path from source `s`.
        Considers the source itself."""
        return self._marked.count(DigraphBFP.CONNECTED)
    

# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest

class TestsDigraphBFP(unittest.TestCase):
    def setUp(self) -> None:
        V = 7
        self.G = Digraph(V)
        (   self.source             ,
            self.strictly_inbound   ,
            self.strictly_outbound  ,
            self.double_linked      ,
            self.one_from_source    ,
            self.two_from_source    ,
            self.not_connected      ) = range(V) 
        
        self.not_in_graph = V

        # strictly in/outbound
        self.G.add_edge( self.source           , self.strictly_inbound )
        self.G.add_edge( self.strictly_outbound, self.source           )
        # double link
        self.G.add_edge( self.source       , self.double_linked )
        self.G.add_edge( self.double_linked, self.source        )
        # directed path
        self.G.add_edge( self.source         , self.one_from_source )
        self.G.add_edge( self.one_from_source, self.two_from_source )

        self.bfp = DigraphBFP(self.G, self.source)

    def test_000_init__type_error_not_a_digraph(self):
        with self.assertRaisesRegex(TypeError, DigraphBFP.NOT_A_DIGRAPH):
            DigraphBFP("G", 0)

    def test_001_init__type_error_sources_not_integer(self):
        with self.assertRaisesRegex(TypeError, Digraph.VERTEX_NOT_INTEGER):
            DigraphBFP(self.G, "0")
    
    def test_002_init__value_error_sources_negative_integer(self):
        with self.assertRaisesRegex(ValueError, Digraph.VERTEX_NOT_POSITIVE):
            DigraphBFP(self.G, -1)

    def test_003_init__source_not_in_graph(self):
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            DigraphBFP(self.G, self.not_in_graph)
    
    def assertBFPConsistency(self, dg: Digraph, sources, bfp: DigraphBFP):
        self.assertEqual( bfp._S , sources )
        self.assertEqual( bfp._DG, dg     )
        # assert collection attrs length
        self.assertEqual( len(bfp._marked) , dg.vertex_count )
        self.assertEqual( len(bfp._edge_to), dg.vertex_count )
        self.assertEqual( len(bfp._dist_to), dg.vertex_count )

    def test_004_init__attrs_without_bfp(self):
        class DigraphBFPDouble(DigraphBFP):
            def _bfs(self, DG: Digraph, v: int) -> None:
                return
        
        sources = {0}

        for V in range(1, 10):
            dg  = Digraph(V)
            bfp = DigraphBFPDouble(dg, sources)
            
            self.assertBFPConsistency(dg, sources, bfp)
            # assert collection attrs initial state
            self.assertEqual( set(bfp._marked) , {False} )
            self.assertEqual( set(bfp._edge_to), {None}  )
            self.assertEqual( set(bfp._dist_to), {None}  )
    
    def test_005_init__monosource_no_edges(self):
        source = {0}
        s = 0

        for V in range(1, 10):
            dg  = Digraph(V)
            bfp = DigraphBFP(dg, source)

            self.assertBFPConsistency(dg, source, bfp)
            
            # marked[source] == True
            self.assertTrue ( bfp._marked[s])
            # marked[others] == False
            self.assertFalse( any(bfp._marked[1:]))

            # edge_to[source and others] == None
            self.assertEqual( set(bfp._edge_to), {None}  )
            
            # dist_to[source] == 0
            self.assertEqual( bfp._dist_to[s], 0 )
            # dist_to[others] == None
            if V > 1:
                self.assertEqual( set(bfp._dist_to[1:]), {None}  )

    def test_006_init__multisource_no_edges(self):
        sources = {0, 1}

        for V in range(2, 10):
            dg  = Digraph(V)
            bfp = DigraphBFP(dg, sources)

            self.assertBFPConsistency(dg, sources, bfp)
            
            # marked[others] == False
            self.assertFalse( any(bfp._marked[2:]))
            
            # edge_to[sources and others] == None
            self.assertEqual( set(bfp._edge_to), {None}  )
            
            # dist_to[others] == None
            if V > 2:
                self.assertEqual( set(bfp._dist_to[2:]), {None}  )

            # check sources
            for s in sources:
                # marked[sources] == True
                self.assertTrue ( bfp._marked[s])
                
                # dist_to[sources] == 0
                self.assertEqual( bfp._dist_to[s], 0 )
    
    def test_007_init__multisource_with_edges(self):
        multisource = {self.not_connected, self.strictly_outbound}

        bfp = DigraphBFP(self.G, multisource)
        self.assertBFPConsistency(self.G, multisource, bfp)

        self.assertTrue( bfp._marked[ self.one_from_source  ] )
        self.assertTrue( bfp._marked[ self.two_from_source  ] )
        self.assertTrue( bfp._marked[ self.strictly_inbound ] )
        self.assertTrue( bfp._marked[ self.double_linked    ] )
        self.assertTrue( bfp._marked[ self.strictly_outbound] )
        self.assertTrue( bfp._marked[ self.not_connected    ] )
    
    def test_100_bfs__graph_with_no_edges(self):
        V = 5
        G = Digraph(V)
        
        for v in range(G.vertex_count):
            bfp = DigraphBFP(G, v)
            self.assertEqual(bfp.count, 1) # only the vertex itself
    
    def test_101_bfs(self):
        self.assertTrue ( self.bfp._marked[ self.one_from_source  ] )
        self.assertTrue ( self.bfp._marked[ self.two_from_source  ] )
        self.assertTrue ( self.bfp._marked[ self.strictly_inbound ] )
        self.assertTrue ( self.bfp._marked[ self.double_linked    ] )
        self.assertFalse( self.bfp._marked[ self.strictly_outbound] )
        self.assertFalse( self.bfp._marked[ self.not_connected    ] )
        
    def test_102_bfs__strictly_inbound_vertex(self):
        self.assertTrue     ( self.bfp._marked [self.strictly_inbound] )
        self.assertIsNotNone( self.bfp._edge_to[self.strictly_inbound] )
        
        self.assertEqual( self.bfp._dist_to[self.strictly_inbound], 1 )

        bfp = DigraphBFP(self.G, self.strictly_inbound)
        self.assertTrue( any(bfp._marked[1:]) )         # except itself 

    def test_103_bfs__strictly_outbound_vertex(self):
        self.assertFalse ( self.bfp._marked [self.strictly_outbound] )
        self.assertIsNone( self.bfp._edge_to[self.strictly_outbound] )
        self.assertIsNone( self.bfp._dist_to[self.strictly_outbound] )

        bfp = DigraphBFP(self.G, self.strictly_outbound)
        self.assertTrue( all(bfp._marked[:-1]) )     # all except not_connected
        
    def test_104_bfs__double_linked_vertex(self):
        original_source = self.source
        original_bfp    = self.bfp
        new_source      = self.double_linked

        self.assertTrue ( original_bfp._marked [new_source] )
        self.assertEqual( original_bfp._edge_to[new_source], original_source )
        self.assertEqual( original_bfp._dist_to[new_source], 1 )

        new_bfp = DigraphBFP(self.G, new_source)
        self.assertTrue ( new_bfp._marked[original_source] )
        self.assertEqual( new_bfp._edge_to[original_source], new_source )
        self.assertEqual( new_bfp._dist_to[original_source], 1 )
    
    def test_105_bfs__vertices_on_directed_path(self):
        bfp = self.bfp
        s   = self.source
        two_from_s = self.two_from_source
        one_from_s = self.one_from_source
        
        self.assertTrue( bfp._marked [one_from_s] )
        self.assertTrue( bfp._marked [two_from_s] )
        
        self.assertEqual( bfp._edge_to[one_from_s], s )
        self.assertEqual( bfp._edge_to[two_from_s], one_from_s )
        
        self.assertEqual( bfp._dist_to[one_from_s], 1 )
        self.assertEqual( bfp._dist_to[two_from_s], 2 )
        
    def test_200_is_reachable__a_vertex_not_in_graph(self):
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            self.bfp.is_reachable(self.not_in_graph)
    
    def test_201_is_reachable(self):
        self.assertTrue ( self.bfp.is_reachable( self.one_from_source  ) )
        self.assertTrue ( self.bfp.is_reachable( self.two_from_source  ) )
        self.assertTrue ( self.bfp.is_reachable( self.strictly_inbound ) )
        self.assertTrue ( self.bfp.is_reachable( self.double_linked    ) )
        self.assertFalse( self.bfp.is_reachable( self.strictly_outbound) )
        self.assertFalse( self.bfp.is_reachable( self.not_connected    ) )

    def test_300_shortest_path_to__vertex_not_in_graph(self):
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            self.bfp.shortest_path_to(self.not_in_graph)

    def test_301_shortest_path_to__vertex_not_connected(self):
        self.assertIsNone(self.bfp.shortest_path_to(self.not_connected))

    def test_302_shortest_path_to__strictly_inbound_vertex(self):
        result   = self.bfp.shortest_path_to(self.strictly_inbound)
        expected = [ self.source, self.strictly_inbound ]
        self.assertEqual(result, expected)

    def test_303_shortest_path_to__strictly_outbound_vertex(self):
        result   = self.bfp.shortest_path_to(self.strictly_outbound)
        expected = None
        self.assertEqual(result, expected)

    def test_304_shortest_path_to__double_linked_vertex(self):
        result   = self.bfp.shortest_path_to(self.double_linked)
        expected = [ self.source, self.double_linked ]
        self.assertEqual(result, expected)

    def test_305_shortest_path_to__vertices_on_directed_path(self):
        result   = self.bfp.shortest_path_to(self.one_from_source)
        expected = [ self.source, self.one_from_source ]
        self.assertEqual(result, expected)

        result   = self.bfp.shortest_path_to(self.two_from_source)
        expected = [ self.source, self.one_from_source, self.two_from_source ]
        self.assertEqual(result, expected)

    def test_306_shortest_path_to(self):
        dg              = self.G
        source          = self.source
        one_from_source = self.one_from_source
        two_from_source = self.two_from_source
        
        farther_vertex  = dg.add_vertex()

        dg.add_edge(two_from_source, farther_vertex)
        
        bfp      = DigraphBFP(dg, source)
        result   = bfp.shortest_path_to(farther_vertex)
        expected = [source, one_from_source, two_from_source, farther_vertex]
        self.assertEqual(result, expected)
        
        dg.add_edge(one_from_source, farther_vertex)
        
        bfp      = DigraphBFP(dg, source)
        result   = bfp.shortest_path_to(farther_vertex)
        expected = [source, one_from_source, farther_vertex]
        self.assertEqual(result, expected)
        
        dg.add_edge(source, farther_vertex)
        
        bfp      = DigraphBFP(dg, source)
        result   = bfp.shortest_path_to(farther_vertex)
        expected = [source, farther_vertex]
        self.assertEqual(result, expected)
        
