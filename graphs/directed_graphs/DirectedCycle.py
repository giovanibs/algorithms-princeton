from digraph import Digraph
from tests_digraph import TestsDigraph

class DirectedCycle:
    """
    Directed cycle detection: does a given digraph
    have a directed cycle? If so, find such a cycle.
    """
    NOT_A_DIGRAPH = "First argument must be a Digraph object."
    NO_CYCLE      = "There is no cycle in the given Digraph."
    
    def __init__(self, DG: Digraph) -> None:
        # --- VALIDATION --- #
        if not isinstance(DG, Digraph):
            raise TypeError(DirectedCycle.NOT_A_DIGRAPH)
        
        # --- INIT --- #
        self._visited: list[bool]     = [ False for _ in range(DG.vertex_count)]
        self._edge_to: list[int|None] = [ None  for _ in range(DG.vertex_count)]
        
        self._on_stack: list[bool] = self._visited.copy()
        self._cycle   : list|None  = None
        
        # --- SEARCH --- #
        for v in range(DG.vertex_count):
            if not self._visited[v] and not self._cycle:
                self._dfs(DG, v)

    def _dfs(self, DG: Digraph, v: int):
        """
        """
        self._visited [v] = True
        self._on_stack[v] = True

        for w in DG.directed_out_of(v):
            if not self._visited[w]:
                self._edge_to[w] = v
                self._dfs(DG, w)

            elif self._on_stack[w]: # closed the directed cycle, trace it back
                self._cycle = []
                
                x = v
                while x != w:
                    self._cycle.insert(0, x)
                    x = self._edge_to[x]
            
                self._cycle.insert(0, w)
                self._cycle.insert(0, v)

                return

        self._on_stack[v] = False   # reset stack

    # ------------------------------- #
    # --- PUBLIC API
    @property
    def has_cycle(self) -> bool:
        """Does the digraph have a directed cycle?"""
        return self._cycle is not None
    
    def cycle(self) -> list | None:
        """
        Returns a directed cycle if the digraph has
        a directed cycle, and `None` otherwise.
        """
        return self._cycle
    

# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest
from random import random

class TestsDirectedCycle(unittest.TestCase):
    class DirectedCycleDouble(DirectedCycle):
        def _dfs(self, DG, v):
            return
    
    def setUp(self) -> None:
        dg = Digraph(1)
        self.dc_double = self.DirectedCycleDouble(dg)

    def test_000_init__type_error_not_a_digraph(self):
        with self.assertRaisesRegex(TypeError, DirectedCycle.NOT_A_DIGRAPH):
            DirectedCycle("G")

    # ------------------------------- #
    # --- PUBLIC API TESTING USING DOUBLE
    def test_001_has_no_cycle(self):
        self.dc_double._cycle = None
        self.assertFalse(self.dc_double.has_cycle)

    def test_001_has_cycle(self):
        self.dc_double._cycle = [random()]
        self.assertTrue(self.dc_double.has_cycle)

    def test_002_cycle__has_no_cycle(self):
        self.dc_double._cycle = None
        self.assertIsNone(self.dc_double.cycle())
    
    def test_003_cycle__has_cycle(self):
        self.dc_double._cycle = [random()]
        self.assertIs(self.dc_double.cycle(), self.dc_double._cycle)

    def test_100_no_cycle(self):
        dg = Digraph(3)
        dg.add_edge(0, 1)
        dg.add_edge(1, 2)

        dc = DirectedCycle(dg)

        self.assertFalse(dc.has_cycle)
    
    def test_101_has_a_cycle__double_link(self):
        dg = Digraph(2)
        dg.add_edge(0, 1)
        dg.add_edge(1, 0)
        dc = DirectedCycle(dg)
        
        expected_cycle = [1, 0, 1]
        self.assertEqual(dc.cycle(), expected_cycle)
    
    def test_102_has_a_cycle(self):
        dg = Digraph(3)
        dg.add_edge(0, 1)
        dg.add_edge(1, 2)
        dg.add_edge(2, 0)
        dc = DirectedCycle(dg)
        
        expected_cycle = [2, 0, 1, 2]
        self.assertEqual(dc.cycle(), expected_cycle)
    
    def test_103_reset_stack_and_keep_looking(self):
        dg = Digraph(4)
        dg.add_edge(0, 1)
        dg.add_edge(2, 3)
        dg.add_edge(3, 2)
        dc = DirectedCycle(dg)
        
        expected_cycle = [3, 2, 3]
        self.assertEqual(dc.cycle(), expected_cycle)
    