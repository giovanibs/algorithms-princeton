class Digraph:
    """
    Set of vertices connected pairwise by DIRECTED edges.

    Directed graph implementation using an adjacency-lists
    representation (vertex-indexed array bags).
    
    Vertices are named `0` through `V-1`, where `V` is the
    count of vertices in the present graph.
    """
    VERTEX_NOT_IN_GRAPH = "Vertices must be in the graph."
    VERTEX_NOT_INTEGER  = "Vertex must be a integer!"
    VERTEX_NOT_POSITIVE = "Vertex must be a positive integer!"
    INIT_V_NOT_INTEGER  = "Number of vertices must be a integer!"
    INIT_V_NOT_POSITIVE = "Number of vertices must be a positive integer!"

    def __init__(self, V: int):
        """
        Initializes a digraph with V vertices and 0 edges.
        """
        if not isinstance(V, int):
            raise ValueError(Digraph.INIT_V_NOT_INTEGER)
        if V < 0:
            raise ValueError(Digraph.INIT_V_NOT_POSITIVE)
        
        self._vertex_count = V
        self._edge_count   = 0

        # adjacency lists for outgoing vertices
        self._outgoing = [set() for _ in range(V)]

    def add_vertex(self):
        """
        Adds a new vertex to the digraph and returns its name.
        """
        self._outgoing.append(set())
        self._vertex_count += 1
        return self._vertex_count

    def add_edge(self, v: int, w: int):
        """Adds `v -> w` edge to the digraph."""
        if not (self.has_vertex(v) and self.has_vertex(w)):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        self._outgoing[v].add(w)
        self._edge_count += 1

    def has_vertex(self, v):
        """
        Check if the digraph contains vertex `v`.
        """
        self._validate_vertex(v)
        return 0 <= v < self._vertex_count
    
    @property
    def vertex_count(self):
        return self._vertex_count
    
    @property
    def edge_count(self):
        return self._edge_count
    
    def outgoing_from(self, v):
        """Returns all vertices adjacent to `v`, that is,
        all vertices pointing out from `v`.
        """
        if not self.has_vertex(v):
            raise IndexError(Digraph.VERTEX_NOT_IN_GRAPH)
        
        return self._outgoing[v]
    
    def _validate_vertex(self, v):
        if not isinstance(v, int):
            raise TypeError(Digraph.VERTEX_NOT_INTEGER)
        if not isinstance(v, int) or v < 0:
            raise ValueError(Digraph.VERTEX_NOT_POSITIVE)