from __future__ import annotations

class Digraph:
    """
    Set of vertices connected pairwise by DIRECTED edges. 

    Directed graph implementation using an adjacency-lists
    representation (vertex-indexed array bags).
    
    Vertices are named `0` through `V-1`, where `V` is the
    count of vertices in the present graph.

    This implementation tries to focus more on efficiency in
    detriment to space.
    """
    VERTEX_NOT_IN_GRAPH = "Vertices must be in the graph."
    VERTEX_NOT_INTEGER  = "Vertex must be a integer!"
    VERTEX_NOT_POSITIVE = "Vertex must be a positive integer!"
    INIT_V_NOT_INTEGER  = "Number of vertices must be a integer!"
    INIT_V_NOT_POSITIVE = "Number of vertices must be a positive integer!"

    def __init__(self, V: int) -> None:
        """
        Initializes a digraph with V vertices and 0 edges.
        """
        if not isinstance(V, int):
            raise ValueError(Digraph.INIT_V_NOT_INTEGER)
        if V < 0:
            raise ValueError(Digraph.INIT_V_NOT_POSITIVE)
        
        self._edge_count   : int = 0
        self._vertex_count : int = V

        # adjacency lists for OUTGOING vertices
        self._directed_out_of : list[set] = [set() for _ in range(V)]
        # adjacency lists for INCOMING vertices
        self._directed_into   : list[set] = [set() for _ in range(V)]

    # ------------------------------- #
    # --- PUBLIC API
    def add_vertex(self) -> int:
        """
        Adds a new vertex to the
        digraph and returns its name.
        """
        self._directed_out_of.append(set())
        self._directed_into  .append(set())
        self._vertex_count += 1

        return self._vertex_count - 1

    def add_edge(self, v: int, w: int) -> None:
        """Adds `v -> w` edge to the digraph."""
        if not (self.has_vertex(v) and self.has_vertex(w)):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        if w in self._directed_out_of[v]:
            return
        
        self._directed_out_of[v].add(w)
        self._directed_into  [w].add(v)
        self._edge_count   += 1

    def has_vertex(self, v: int) -> bool:
        """
        Check if the digraph contains vertex `v`.
        """
        self._validate_vertex(v)
        return 0 <= v < self._vertex_count
    
    @property
    def vertex_count(self) -> int:
        return self._vertex_count
    
    @property
    def edge_count(self) -> int:
        return self._edge_count
    
    def directed_out_of(self, v: int) -> set:
        """Returns all adjacent vertices
        that has an edge DIRECTED FROM `v`"""
        if not self.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return self._directed_out_of[v]
    
    def directed_into(self, v: int) -> set:
        """Returns all adjacent vertices
        that has an edge DIRECTED TO `v`"""
        if not self.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return self._directed_into[v]
    
    def outdegree(self, v: int) -> int:
        """Returns the number of directed
        edges incident FROM `v`"""
        if not self.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return len(self._directed_out_of[v]) 

    def indegree(self, v: int) -> int:
        """Returns the number of directed
        edges incident TO `v`"""
        if not self.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return len(self._directed_into[v])
    
    def reverse(self) -> Digraph:
        """Returns a reversed (deep-)copy
        of the instance digraph.
        
        "FROM BECOMES TO,
        TO BECOMES FROM."
        (unknown)
        """
        r = Digraph(self._vertex_count)

        r._edge_count = self._edge_count

        r._directed_out_of = [ edge.copy() for edge in self._directed_into   ]
        r._directed_into   = [ edge.copy() for edge in self._directed_out_of ]

        return r

    # ------------------------------- #
    # --- HELPER METHODS/PROPERTIES
    def _validate_vertex(self, v: int):
        if not isinstance(v, int):
            raise TypeError(Digraph.VERTEX_NOT_INTEGER)
        if not isinstance(v, int) or v < 0:
            raise ValueError(Digraph.VERTEX_NOT_POSITIVE)