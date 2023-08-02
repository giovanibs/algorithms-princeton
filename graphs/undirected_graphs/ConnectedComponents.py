from undirected_graph import Graph
from tests_undirected_graph import TestsUndirectedGraph


class CC:
    """
    Connected components: A connected component is
    a maximal set of connected vertices.

    Goal: Preprocess graph to answer queries of the
    form "is v connected to w?" in constant time.

    Attributes:
        _G      : Graph         = graph to preprocess
        _count  : int           = number of connected components groups
        _id     : list[int]     = component group identifier
        _marked : list[bool]    = visited vertices are marked as `True`

    Steps:

    1) Initialize all vertices as unmarked;
    2) For each unmarked vertex, run DFS to identify all
    vertices discovered as part of the same component.
    That is:
            - mark vertex `v` as visited.
            - recursively visit all unmarked vertices
            ADJACENT to `v`.
            - all vertices discovered in the same DFS
            have same id.
    """
    NOT_A_GRAPH = "First argument must be a Graph object."
    EMPTY_GRAPH = "Graph is empty."

    def __init__(self, G: Graph) -> None:
        """Find connected components in G"""

        self._G      : Graph = G
        self._count  : int   = 0
        self._marked = [ False for _ in range(G.vertices_count) ]
        self._id     = [ None  for _ in range(G.vertices_count) ]

        for v in range(G.vertices_count):
            if not self._marked[v]:
                self._dfs(G, v)    # all vertices discovered have same id
                self._count += 1

    def _dfs(self, G: Graph, v):
        self._marked[v] = True
        self._id[v]     = self._count

        for w in G.adjacent_to(v):
            if not self._marked[w]:
                self._dfs(self._G, w)

    @property
    def count(self):
        """Returns number of components."""
        return self._count
    
    def id(self, v):
        """Returns the id of component containing `v`."""
        return self._id[v]


import unittest

class TestsCC(unittest.TestCase):
    def test_cc(self):
        V = 5
        G = Graph(V)
        v0, v1, v2, v3, v4 = range(V)

        # no connected vertices
        cc = CC(G)
        self.assertEqual(cc.count, 5)
        self.assertEqual(cc.id(v0), 0)
        self.assertEqual(cc.id(v1), 1)
        self.assertEqual(cc.id(v2), 2)
        self.assertEqual(cc.id(v3), 3)
        self.assertEqual(cc.id(v4), 4)

        G.add_edge(v0, v1)
        cc = CC(G)
        self.assertEqual(cc.count, 4)
        self.assertEqual(cc.id(v0), 0)
        self.assertEqual(cc.id(v1), 0)
        self.assertEqual(cc.id(v2), 1)
        self.assertEqual(cc.id(v3), 2)
        self.assertEqual(cc.id(v4), 3)

        G.add_edge(v0, v2)
        cc = CC(G)
        self.assertEqual(cc.count, 3)
        self.assertEqual(cc.id(v0), 0)
        self.assertEqual(cc.id(v1), 0)
        self.assertEqual(cc.id(v2), 0)
        self.assertEqual(cc.id(v3), 1)
        self.assertEqual(cc.id(v4), 2)
        
        G.add_edge(v3, v4)
        cc = CC(G)
        self.assertEqual(cc.count, 2)
        self.assertEqual(cc.id(v0), 0)
        self.assertEqual(cc.id(v1), 0)
        self.assertEqual(cc.id(v2), 0)
        self.assertEqual(cc.id(v3), 1)
        self.assertEqual(cc.id(v4), 1)
