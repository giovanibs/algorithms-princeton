class WordNet:
    """
    WordNet is a semantic lexicon for the English language that computational
    linguists and cognitive scientists use extensively.
    
    ### Some definitions:

        - `synset`  : set of synonym(s)
        - `hyponym` : more specific synset 
        - `hypernym`: more general synset 

    ### The WordNet digraph:

        - each vertex `v` is an integer that
        represents a synset;
        
        - each directed edge `v → w` represents
        that `w` is a hypernym of `v`;Any argument to the constructor or an instance method is null
    The input to the constructor does not correspond to a rooted DAG.
    

    ### Corner cases.
    
    Raise an exception in the following situations:

        - Any argument to the constructor or
        an instance method is null;

        - The input to the constructor does not
        correspond to a rooted DAG;

        - Any of the noun arguments in distance()
        or sap() is not a WordNet noun. 

    """

    def __init__(self, synsets, hypernyms):
        """constructor takes the name of the two input files (CSV):
        
        - List of synsets: contains all noun synsets in WordNet,
        one per line (VERTICES). The fields are:
                - `synset_id`, `synset`, `gloss`    
        
        - List of hypernyms: contains the hypernym relationships (the EDGES).
        The fields are:
                - `synset_id`, `hypernym_0`, `hypernym_1`, ... `hypernym_n`
        """

    # ---------------------------------
    # PUBLIC API
    
    def nouns():
        """
        returns all WordNet nouns
        """
    
    def isNoun(self, word):
        """
        is the word a WordNet noun?
        """
    
    def distance(self, nounA, nounB):
        """
        distance between nounA and nounB (defined below)
        """
    
    def sap(self, nounA, nounB):
        """
        a synset (second field of synsets.txt) that is the common ancestor
        of nounA and nounB in a shortest ancestral path (defined below)
        """
