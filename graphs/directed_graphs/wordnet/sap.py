from digraph import Digraph

class SAP:
    """
    # Shortest ancestral path.
    
    ### Definition

    An ancestral path between two vertices `v` and `w` in a digraph is:
        
        - a directed path from `v` to a common ancestor `ancestor`,
        together with;
        
        - a directed path from `w` to the same ancestor `ancestor`.
    
    A shortest ancestral path is an ancestral path of minimum total length.
    
    We refer to the common ancestor in a shortest ancestral path as a
    shortest common ancestor.

    Note also that an ancestral path is a path, but not a directed path.

    ###  Corner cases.
    
    Throw an IllegalArgumentException in the following situations:

        - Any argument is null
        - Any vertex argument is outside its prescribed range
        - Any iterable argument contains a null item 
    
    """

    def __init__(self, dg: Digraph) -> None:
        pass

    # ---------------------------------
    # --- PUBLIC API

    def length(self, v, w):
        """
        length of shortest ancestral path between v and w; -1 if no such path
        """

    def ancestor(self, v, w):
        """
        a common ancestor of v and w that participates
        in a shortest ancestral path; -1 if no such path
        """

    def length(self, v, w):
        """
        length of shortest ancestral path between any
        vertex in v and any vertex in w; -1 if no such path
        """

    def ancestor(self, v, w):
        """
        a common ancestor that participates in shortest
        ancestral path; -1 if no such path
        """