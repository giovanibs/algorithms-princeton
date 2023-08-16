from collections import deque
from wordnet import WordNet, TestsInitWordNet, TestsPublicAPI

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

    def __init__(self, wn: WordNet) -> None:
        self._wn = wn
        self._visited: dict
        self._dist_to: dict
        self._edge_to: dict
        

    # ---------------------------------
    # --- PUBLIC API
    def sap(
            self,
            noun_a: str|set[str],
            noun_b: str|set[str] 
        ) -> tuple[list[int], int, str]:
        """
        Measuring the semantic relatedness of two nouns:
        Semantic relatedness refers to the degree to which
        two concepts are related.

        Returns the path and length of shortest
        ancestral path of `noun_a` and `noun_b`.
        """
        if isinstance(noun_a, set):
            noun_a = noun_a.pop() # get any noun from the set
        
        if isinstance(noun_b, set):
            noun_b = noun_b.pop() # get any noun from the set
        
        
        self._wn._validate_noun(noun_a)
        self._wn._validate_noun(noun_b)

        # get synset_id of noun_a and noun_b, they could be different nouns,
        # but synonyms (i.e. part of the same synset.)
        a = self._wn._id_of(noun_a)
        b = self._wn._id_of(noun_b)

        if a == b:
            return [a], 0, a
        
        
        self._bfs(a, b)

        
        # ----------- #
        # --- SAP --- #
        # Since we found a UNDIRECT path from `a` to `b`, let's trace back
        # each synset `s` starting from `b` by making use of the `edge_to`:
        sap = self._traceback_path(from_=b, to_=a)
        
        # -------------------------------- #
        # --- Shortest Common Ancestor --- #
        sca = self._sca(sap)         

        # FINALLY, we return the sap AND the distance from `a` to `b`
        return sap, self._dist_to[b], sca


    def _traceback_path(self, *, from_: int, to_: int):
        """Traceback the path from `b` to `a` and return it"""

        sap    = []
        synset = from_

        # if to_ == 5 and from_ == 9:
        #     breakpoint()

        while synset != to_:
            sap.append(synset)
            synset = self._edge_to[synset]

        sap.append(to_)
        return sap
    

    def _bfs(self, a: int, b: int|None = None):

        q = deque([a])       # let's start a FIFO queue with `a` (could be `b`)
      
        # initiate dicts
        self._visited = {a: False}
        self._dist_to = {a: 0}
        self._edge_to = {a: a}

        while q:
            synset = q.popleft()
            
            self._visited[synset] = True

            connected_synsets = self._wn._connected_to(synset)

            if b and b in connected_synsets:
                self._edge_to[b] = synset
                self._dist_to[b] = self._dist_to[synset] + 1
                
                break # search is done.

            # Now, let's put every connected synset `cs` in the queue...
            for cs in connected_synsets:
                # ...except for those already in the queue / visited in the loop
                if cs not in q and not self._visited.get(cs, False):
                    q.append(cs)
                    self._visited[cs] = True
                    self._edge_to[cs] = synset
                    self._dist_to[cs] = self._dist_to[synset] + 1

       

    
    def _sca(self, sap: iter) -> int:
        """
        Let's go through the sap until we reach the highest
        hypernym on the `sap`, that is either:
            - the synset whose successor is one of its hyponyms;
            - OR the last synset on the path.
        """
        for i, synset in enumerate(sap):
            is_last = i == len(sap)-1

            if is_last or sap[i+1] in self._wn.hypo_of(synset):
                # keep sap[i+1] after is_last to prevent index overflow
                return synset


    

# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest


class WordNetDouble(WordNet):
    def __init__(self):
        self._synsets      = None
        self._hypernyms    = None
        self._hyponyms     = dict()
        self._synset_count = None


class TestsSAP(unittest.TestCase):

    def setUp(self):
        wn = self._wn = WordNetDouble()
        n  = self.n  = 10
        
        wn._synsets = { id: {str(id)} for id in range(n) }
        
        wn._hypernyms = {
            0: {}     ,
            1: {0}    ,
            2: {0}    ,
            3: {1, 5} ,
            4: {1}    ,
            5: {1, 2} ,
            6: {2, 0} ,
            7: {5}    ,
            8: {6}    ,
            9: {8, 0} ,
        }
        wn._set_hyponyms(wn._hypernyms, wn._hyponyms)
        self.sap = SAP(wn)

    def test_000__validation(self):
        with self.assertRaisesRegex(TypeError, WordNet.NOT_A_STRING):
            self.sap.sap(1, "0")
            self.sap.sap("1", 0)
            self.sap.sap("1", "0")
    

    def test_001__reflexive_sap(self):
        sap = self.sap
        
        for noun in range(self.n):
            output = sap.sap(str(noun), str(noun))
            target = [noun], 0, noun
            self.assertTupleEqual(output, target)
    

    def test_002__sap__from_hyper_to_hyponym(self):
        output = self.sap.sap('1', '4')
        target = [4, 1], 1, 1
        self.assertTupleEqual(output, target)
    

    def test_003__sap__from_hypo_to_hypernym(self):
        output = self.sap.sap('4', '1')
        target = ( path:=[1, 4], len(path)-1, 1 )
        self.assertTupleEqual(output, target)
        
    
    def test_004__sap__shortest_of_two(self):
        output = self.sap.sap('5', '9')
        target = ( path:=[9, 0, 1, 5], len(path)-1, 0)
        # longer:        [9, 8, 6, 2, 5]
        self.assertTupleEqual(output, target)
    
        output = self.sap.sap('9', '2')
        target = ( path:=[2, 0, 9], len(path)-1, 0)
        # longer:        [2, 6, 8, 9]
        self.assertTupleEqual(output, target)
    

    def test_005__sap__two_shortest(self):
        output = self.sap.sap('4', '8')
        targets = (
             (path:=[8, 9, 0, 1, 4], len(path)-1, 0),
             (path:=[8, 6, 0, 1, 4], len(path)-1, 0),
        )
        
        output = self.sap.sap('8', '4')
        targets = (
             (path:=[4, 1, 0, 9, 8], len(path)-1, 0),
             (path:=[4, 1, 0, 6, 8], len(path)-1, 0),
        )
        self.assertIn(output, targets)
