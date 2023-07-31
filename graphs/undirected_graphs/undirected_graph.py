class Graph:
    """
    Undirected graph implementation using an adjacency-lists
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
        Initializes an graph with V vertices and 0 edges.
        """
        if not isinstance(V, int):
            raise ValueError(Graph.INIT_V_NOT_INTEGER)
        
        if V < 0:
            raise ValueError(Graph.INIT_V_NOT_POSITIVE)
        
        self._V = V
        self._E = 0

        self._adj = []
        for _ in range(self._V):
            self._adj.append(set())

    def add_vertex(self):
        """
        Adds a new vertex to the graph and returns its name.
        """
        self._adj.append(set())
        self._V += 1
        return self.vertices_count

    def add_edge(self, v: int, w: int):
        """Adds v-w edge to the graph."""
        if not (self.has_vertex(v) and self.has_vertex(w)):
            raise IndexError(Graph.VERTEX_NOT_IN_GRAPH)
        
        self._adj[v].add(w)
        self._adj[w].add(v)
        self._E += 1

    def has_vertex(self, v):
        """
        Check if the graph contains vertex `v`.
        """
        self._validate_vertex(v)
        
        return 0 <= v < self._V
    
    @property
    def vertices_count(self):
        return self._V
    
    @property
    def edges_count(self):
        return self._E
    
    def adjacent_to(self, v):
        """Returns all vertices adjacent to `v`, that is,
        all vertices with an edge to `v`.
        """
        if not self.has_vertex(v):
            raise IndexError(Graph.VERTEX_NOT_IN_GRAPH)
        
        return self._adj[v]
    
    def _validate_vertex(self, v):
        if not isinstance(v, int):
            raise ValueError(Graph.VERTEX_NOT_INTEGER)
        if not isinstance(v, int) or v < 0:
            raise ValueError(Graph.VERTEX_NOT_POSITIVE)
