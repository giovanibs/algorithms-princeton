from digraph         import Digraph
from tests_digraph   import TestsDigraph
from DepthFirstOrder import ( 
                                DepthFirstOrder,
                                TestsDepthFirstOrderAPI,
                                TestsDepthFirstOrderInternals
                                                                )
from DirectedCycle import DirectedCycle, TestsDirectedCycle

class TopologicalSort:
    """
    Given a digraph, put the vertices in order such that all its
    directed edges point from a vertex earlier in the order to a
    vertex later in the order (or report that doing so is not possible).

    - A digraph has a topological order if and only if it is a DAG.
    - Reverse postorder in a DAG is a topological sort.
    """
    NOT_A_DIGRAPH = "First argument must be a Digraph object."
    
    def __init__(self, DG: Digraph) -> None:
        if not isinstance(DG, Digraph):
            raise TypeError(TopologicalSort.NOT_A_DIGRAPH)
        
        dc = DirectedCycle(DG)

        if not dc.has_cycle:
            dfo = DepthFirstOrder(DG)
            self._order = dfo.reversed_postorder
        else:
            self._order = None

    # ------------------------------- #
    # --- PUBLIC API
    @property
    def topological_order(self) -> list[int]:
        """Returns a topological order if the
        digraph has it; and None otherwise.
        """
        return self._order
    
    @property
    def has_order(self):
        """Does the digraph have a topological order?"""
        return self._order is not None
    
    def rank(self, v: int):
        """
        Returns the rank of vertex `v` in the topological
        order; or `None` if the digraph is not a DAG.
        """
        return self._order.index(v) if self.has_order else None


# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest

class TestsTopologicalSort_SingleVertex(unittest.TestCase):
    def setUp(self) -> None:
        dg = Digraph(1)
        self.ts = TopologicalSort(dg)
    
    def test_has_order(self):
        self.assertTrue(self.ts.has_order)

    def test_order(self):
        result   = self.ts.topological_order
        expected = [0]
        self.assertEqual(result, expected)
    
    def test_rank(self):
        self.assertEqual(self.ts.rank(0), 0)
        
class TestsTopologicalSort_2Vertices(unittest.TestCase):
    def setUp(self) -> None:
        dg = Digraph(2)
        dg.add_edge(0, 1)
        self.ts = TopologicalSort(dg)
    
    def test_has_order(self):
        self.assertTrue(self.ts.has_order)

    def test_order(self):
        result   = self.ts.topological_order
        expected = [0, 1]
        self.assertEqual(result, expected)
    
    def test_rank(self):
        self.assertEqual(self.ts.rank(0), 0)
        self.assertEqual(self.ts.rank(1), 1)
        
class TestsTopologicalSort_3Vertices(unittest.TestCase):
    def setUp(self) -> None:
        dg = Digraph(3)
        dg.add_edge(0, 1)
        dg.add_edge(0, 2)
        dg.add_edge(1, 2)
        self.ts = TopologicalSort(dg)
    
    def test_has_order(self):
        self.assertTrue(self.ts.has_order)

    def test_order(self):
        result   = self.ts.topological_order
        expected = [0, 1, 2]
        self.assertEqual(result, expected)
    
    def test_rank(self):
        self.assertEqual(self.ts.rank(0), 0)
        self.assertEqual(self.ts.rank(1), 1)
        self.assertEqual(self.ts.rank(2), 2)
        
class TestsTopologicalSort_NotDAG(unittest.TestCase):
    def setUp(self) -> None:
        dg = Digraph(3)
        dg.add_edge(0, 1)
        dg.add_edge(1, 2)
        dg.add_edge(2, 0)
        self.ts = TopologicalSort(dg)
    
    def test_has_order(self):
        self.assertFalse(self.ts.has_order)

    def test_order(self):
        self.assertIsNone(self.ts.topological_order)
    
    def test_rank(self):
        self.assertIsNone(self.ts.rank(0))
        self.assertIsNone(self.ts.rank(1))
        self.assertIsNone(self.ts.rank(2))
        
class TestsTopologicalSort_Other(unittest.TestCase):
    def test_000_type_error_not_a_digraph(self):
            with self.assertRaisesRegex(TypeError, DirectedCycle.NOT_A_DIGRAPH):
                TopologicalSort("G")

