from digraph import Digraph
from tests_digraph import TestsDigraph
from DepthFirstOrder import (
    DepthFirstOrder,
    TestsDepthFirstOrderAPI,
    TestsDepthFirstOrderInternals
)

class KosarajuSharirSCC:
    """
    ### Intro

    Strong connectivity is an equivalence relation on the set of vertices:

        - Reflexive: Every vertex v is
        strongly connected to itself.

        - Symmetric: If v is strongly connected
        to w, then w is strongly connected to v.

        - Transitive: If v is strongly connected
        to w and w is strongly connected to x,
        then v is also strongly connected to x. 

    A strong component is a maximal subset of strongly-connected vertices.

    ### This class

    The KosarajuSharirSCC class represents a data type for
    determining the strong components in a digraph.

        - The `id` operation determines in which strong component
        a given vertex lies;
        
        - The `are_strongly_connected` operation determines whether
        two vertices are in the same strong component;

        - And the `count` operation determines the number of strong
        components.
    
    The `component identifier` of a component is one of the
    vertices in the strong component: two vertices have the same component
    identifier if and only if they are in the same strong component.
    
    This implementation uses the Kosaraju-Sharir algorithm:

        1) Given a digraph `DG`, use DepthFirstOrder to compute
        the reverse postorder of its reverse, DG-R.

        2) Run standard DFS on `DG`, but consider the unmarked
        vertices in the order just computed instead of the
        standard numerical order. 

        3) All vertices reached on a call to the recursive `_dfs()`
        from the constructor are in a strong component (!), so
        identify them.
    """

    NOT_A_DIGRAPH = "First argument must be a Digraph object."
    
    def __init__(self, DG: Digraph) -> None:
        if not isinstance(DG, Digraph):
            raise TypeError(KosarajuSharirSCC.NOT_A_DIGRAPH)
        
        self._count: int = 0
        self._visited: list[bool] = [ False for _ in range(DG.vertex_count)]
        self._id: list[int|None]  = [ None  for _ in range(DG.vertex_count)]

        # PHASE 1
        dfo = DepthFirstOrder( DG.reverse() )

        # PHASE 2
        for v in dfo.reversed_postorder:
            if not self._visited[v]:
                self._dfs(DG, v)
                self._count += 1
        

    def _dfs(self, DG: Digraph, v: int) -> None:
        self._visited[v] = True
        self._id[v]      = self._count

        for w in DG.directed_out_of(v):
            if not self._visited[w]:
                self._dfs(DG, w)

    # ---------------------------------
    # --- PUBLIC API
    @property
    def count(self):
        """Returns the number of strong components."""
        return self._count
    

    def are_strongly_connected(self, v: int, w: int):
        """Are vertices `v` and `w` in the same strong component?"""
        return self._id[v] == self._id[w]
    

    def id(self, v: int):
        """
        Returns the component id of the strong
        component containing vertex `v`.
        """
        return self._id[v]


# ------------------------------------------------------------------------------
# --- UNIT TESTS
import unittest
from random import randrange

class TestsPublicAPI(unittest.TestCase):
    """
    Class for testing the public API
    """
    
    def setUp(self) -> None:
        dg = Digraph(2)
        self.scc = KosarajuSharirSCC(dg)
    

    def test_000_init_not_a_digraph(self):
        with self.assertRaisesRegex(TypeError, KosarajuSharirSCC.NOT_A_DIGRAPH):
            KosarajuSharirSCC("Not a digraph")


    def test_001_count_scc(self):
        self.scc._count = randrange(100)
        self.assertEqual(self.scc.count, self.scc._count)


    def test_002_are_strongly_connected(self):
        v0, v1 = 0, 1
        
        self.scc._id[v0] = 0
        self.scc._id[v1] = 0
        self.assertTrue(self.scc.are_strongly_connected(v0, v1))

        self.scc._id[v1] = 1
        self.assertFalse(self.scc.are_strongly_connected(v0, v1))


    def test_003_id(self):
        v = 0
        self.scc._id[v] = randrange(100)
        self.assertEqual(self.scc.id(v), self.scc._id[v])


class TestsKosarajuSharirSCC(unittest.TestCase):
    
    def test_000_unitary_scc(self):
        V = 3
        dg = Digraph(V)
        self.scc = KosarajuSharirSCC(dg)

        self.assertEqual(self.scc.count, V)

        for v in range(V):
            # reflexive
            self.assertTrue(self.scc.are_strongly_connected(v, v))
            self.assertEqual(self.scc.id(v), V-v-1) # id in reversed postorder
    

    def test_001_two_scc(self):
        V = 3
        v0, v1, v2 = range(V)
        dg = Digraph(V)
        dg.add_edge(v0, v1)
        dg.add_edge(v1, v0)
        dg.add_edge(v1, v2)

        scc = KosarajuSharirSCC(dg)

        self.assertEqual(scc.count, 2)
        self.assertTrue (scc.are_strongly_connected(v0, v1))
        self.assertFalse(scc.are_strongly_connected(v0, v2))
        self.assertFalse(scc.are_strongly_connected(v1, v2))


    def test_002_many_scc(self):
        V = 6
        v0, v1, v2, v3, v4, v5 = range(V)
        dg = Digraph(V)
        
        # SCC 01
        dg.add_edge(v0, v1)
        dg.add_edge(v0, v2)
        dg.add_edge(v1, v0)
        dg.add_edge(v1, v2)
        dg.add_edge(v2, v0)
        dg.add_edge(v2, v1)
        # SCC 02
        dg.add_edge(v3, v4)
        dg.add_edge(v4, v3)
        # SCC 03
        dg.add_edge(v4, v5)
        dg.add_edge(v2, v5)
        scc = KosarajuSharirSCC(dg)

        self.assertEqual(scc.count, 3)
        
        # assert SCC 01
        self.assertTrue(scc.are_strongly_connected(v0, v1))
        self.assertTrue(scc.are_strongly_connected(v0, v2))
        self.assertTrue(scc.are_strongly_connected(v1, v2))
        # assert SCC 02
        self.assertTrue(scc.are_strongly_connected(v3, v4))
        # assert SCC 03
        self.assertTrue(scc.are_strongly_connected(v5, v5))
        
        # assert not scc
        self.assertFalse(scc.are_strongly_connected(v0, v3))
        self.assertFalse(scc.are_strongly_connected(v0, v5))
        self.assertFalse(scc.are_strongly_connected(v3, v5))
