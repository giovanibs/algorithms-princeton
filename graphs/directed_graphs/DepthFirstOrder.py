from digraph import Digraph
from tests_digraph import TestsDigraph

class DepthFirstOrder:
    """
    The DepthFirstOrder class represents a data type for
    determining depth-first search ordering of the vertices
    in a digraph, including:
        
        - preorder;
        - postorder;
        - and reverse postorder.
    """
    NOT_A_DIGRAPH = "First argument must be a Digraph object."

    def __init__(self, DG: Digraph) -> None:
        if not isinstance(DG, Digraph):
            raise TypeError(DepthFirstOrder.NOT_A_DIGRAPH)
        
        # --- INIT --- #
        self._DG = DG

        self._pre_of : list[int|None] = [ None  for _ in range(DG.vertex_count)]
        self._post_of: list[int|None] = self._pre_of.copy()
        self._visited: list[bool] = [ False for _ in range(DG.vertex_count)]
        
        self._preorder_vertices : list[int] = []
        self._postorder_vertices: list[int] = []
        
        self._pre_counter : int = 0     # counter or preorder numbering
        self._post_counter: int = 0     # counter for postorder numbering
        
        # --- SEARCH --- #
        for v in range(DG.vertex_count):
            if not self._visited[v]:
                self._dfs(DG, v)

    # ------------------------------- #
    # --- SEARCH
    def _dfs(self, DG: Digraph, v: int) -> None:
        """
        Depth-first search search visits each vertex
        exactly once. Three vertex orderings are of
        interest in typical applications:

        - Preorder: Put the vertex on a
        QUEUE BEFORE the recursive calls.

        - Postorder: Put the vertex on a
        QUEUE AFTER the recursive calls.

        - Reverse postorder: Put the vertex
        on a STACK AFTER the recursive calls. 
        """
        self._visited[v] = True
        
        # --- update preorder
        self._pre_of [v] = self._pre_counter
        self._preorder_vertices.append(v)
        self._pre_counter += 1

        for w in DG.directed_out_of(v):
            if not self._visited[w]:
                self._dfs(DG, w)
        
        # --- update postorder
        self._post_of [v] = self._post_counter
        self._postorder_vertices.append(v)
        self._post_counter += 1

    def _validate_vertex(self, v: int):
        if not self._DG.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
    # ------------------------------- #
    # --- PUBLIC API
    def preorder_of(self, v: int) -> int:
        """
        Returns the preorder of `v`.
        """
        self._validate_vertex(v)
        return self._pre_of[v]
    
    def postorder_of(self, v: int) -> int:
        """
        Returns the postorder of `v`.
        """
        self._validate_vertex(v)
        return self._post_of[v]

    @property    
    def preorder(self) -> list[int]:
        """
        Returns the vertices in preorder.
        """
        return self._preorder_vertices

    @property    
    def postorder(self) -> list[int]:
        """
        Returns the vertices in postder.
        """
        return self._postorder_vertices
    
    @property    
    def reversed_postorder(self) -> list[int]:
        """
        Returns the vertices in reversed preorder.
        """
        return list(reversed(self._postorder_vertices))

# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest
from random import random

class TestsDepthFirstOrderAPI(unittest.TestCase):
    """
    Test the public API methods using a test double. 
    """
    class DepthFirstOrderDouble(DepthFirstOrder):
        def _dfs(self, DG, v):
            return
        
    def setUp(self) -> None:
        self.dg  = Digraph(1)
        self.v   = 0
        self.dfo = self.DepthFirstOrderDouble(self.dg)
    
    def test_001_preorder_of(self) -> int:
        expected = self.dfo._pre_of[self.v] = random()
        self.assertEqual(self.dfo.preorder_of(self.v), expected)
    
    def test_002_postorder_of(self) -> int:
        expected = self.dfo._post_of[self.v] = random()
        self.assertEqual(self.dfo.postorder_of(self.v), expected)

    def test_003_preorder(self) -> int:
        expected = self.dfo._preorder_vertices = [random()]
        self.assertEqual(self.dfo.preorder, expected)
    
    def test_004_postorder(self) -> int:
        expected = self.dfo._postorder_vertices = [random()]
        self.assertEqual(self.dfo.postorder, expected)
    
    def test_005_reversed_postorder(self):
        self.dfo._postorder_vertices = [random()]
        expected = list(reversed( self.dfo._postorder_vertices))
        self.assertEqual(self.dfo.reversed_postorder, expected)

class TestsDepthFirstOrderInternals(unittest.TestCase):
    def test_000_init__type_error_not_a_digraph(self):
        with self.assertRaisesRegex(TypeError, DepthFirstOrder.NOT_A_DIGRAPH):
            DepthFirstOrder("G")

    def test_000_validate_vertex(self):
        dg = Digraph(1)
        dfo = DepthFirstOrder(dg)
        
        # good vertex
        dfo.preorder_of(0)
        
        # bad vertex
        with self.assertRaisesRegex(IndexError, Digraph.VERTEX_NOT_IN_GRAPH):
            dfo.preorder_of(1)

    def test_001_single_vertex(self):
        dg = Digraph(1)
        v = 0
        dfo = DepthFirstOrder(dg)

        self.assertEqual(dfo.preorder_of (v), 0)
        self.assertEqual(dfo.postorder_of(v), 0)
        
        self.assertEqual(dfo.preorder, [0])
        self.assertEqual(dfo.postorder, [0])
        self.assertEqual(dfo.reversed_postorder, [0])
    
    def test_002_two_vertices(self):
        dg = Digraph(2)
        v0, v1 = 0, 1
        dg.add_edge(v0, v1)
        dfo = DepthFirstOrder(dg)

        self.assertEqual(dfo.preorder_of (v0), 0)
        self.assertEqual(dfo.preorder_of (v1), 1)
        self.assertEqual(dfo.postorder_of(v0), 1)
        self.assertEqual(dfo.postorder_of(v1), 0)
        
        self.assertEqual(dfo.preorder, [0, 1])
        self.assertEqual(dfo.postorder, [1, 0])
        self.assertEqual(dfo.reversed_postorder, [0, 1])
    
    def test_003_binary_tree(self):
        V = 3
        dg = Digraph(V)
        v0, v1, v2 = range(V)
        dg.add_edge(v0, v1)
        dg.add_edge(v0, v2)
        dfo = DepthFirstOrder(dg)

        self.assertEqual(dfo.preorder_of (v0), 0)
        self.assertEqual(dfo.preorder_of (v1), 1)
        self.assertEqual(dfo.preorder_of (v2), 2)
        
        self.assertEqual(dfo.postorder_of(v0), 2)
        self.assertEqual(dfo.postorder_of(v1), 0)
        self.assertEqual(dfo.postorder_of(v2), 1)
        
        self.assertEqual(dfo.preorder, [0, 1, 2])
        self.assertEqual(dfo.postorder, [1, 2, 0])
        self.assertEqual(dfo.reversed_postorder, [0, 2, 1])

    def test_004_three_on_directed_path(self):
        V = 3
        dg = Digraph(V)
        v0, v1, v2 = range(V)
        dg.add_edge(v0, v1)
        dg.add_edge(v1, v2)
        dfo = DepthFirstOrder(dg)

        self.assertEqual(dfo.preorder_of (v0), 0)
        self.assertEqual(dfo.preorder_of (v1), 1)
        self.assertEqual(dfo.preorder_of (v2), 2)
        
        self.assertEqual(dfo.postorder_of(v0), 2)
        self.assertEqual(dfo.postorder_of(v1), 1)
        self.assertEqual(dfo.postorder_of(v2), 0)
        
        self.assertEqual(dfo.preorder, [0, 1, 2])
        self.assertEqual(dfo.postorder, [2, 1, 0])
        self.assertEqual(dfo.reversed_postorder, [0, 1, 2])

