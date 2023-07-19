class TwoThreeTree:
    """
    ## 2-3 Trees
    
    ### Definition.
    A 2-3 search tree is a tree that either is empty or:

    - A 2-node, with one key (and associated value) and two links,
    a left link to a 2-3 search tree with smaller keys, and a
    right link to a 2-3 search tree with larger keys
    
    - A 3-node, with two keys (and associated values) and three
    links:
        - a left link to a 2-3 search tree with smaller keys
        - a middle link to a 2-3 search tree with keys between
        the node's keys
        - a right link to a 2-3 search tree with larger keys.
    
    A perfectly balanced 2-3 search tree (or 2-3 tree for short)
    is one whose null links are all the same distance from the root. 
    """