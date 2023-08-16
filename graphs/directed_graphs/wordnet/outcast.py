from wordnet import WordNet, TestsInitWordNet, TestsPublicAPI
from collections import deque

class Outcast:

    def __init__(self, wn: WordNet) -> None:
        self._wn = wn
        self._visited: dict
        self._dist_to: dict
        self._edge_to: dict
        

    def outcast(self, nouns: list[str]|None = None) -> list[int]:
        """
        To identify an outcast, compute the sum of the distances
        between each noun and every other one and return a noun
        (or nouns) for which the distance is maximum.

        ### Brute force implementation

            - run `_bfs` for a noun and every other one.
        """
        synsets = self._validate_nouns(nouns)

        if len(synsets) == 1:
            return next(iter(self._wn._synsets))
        
        distances: dict[int, int] = {}

        # get the distances from every given noun (or all nouns
        # if None is given) to every other synset.
        
        for synset in synsets:
            self._bfs(synset)
            distances[synset] = sum(self._dist_to.values())

        return max(distances.items(), key=max)[0]


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


    def _validate_nouns(self, nouns):
        if nouns is None:
            return self._wn._synsets.keys()
        
        synsets_ids = set()

        for noun in nouns:
            
            if not self._wn.is_noun(noun):
                raise ValueError(f"{noun!r} is not in the WordNet.")
            
            synsets_ids.update(self._wn._id_of(noun, first = False))

        return synsets_ids


# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest


class TestsOutcast(unittest.TestCase):
    def test_000__outcast__reflexive(self):
        
        # --- SET UP --- #
        n = 1
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [ (0, {}) ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = 0
        self.assertEqual(actual, target)
    
        
        # --- ASSERT BY NOUN --- #
        nouns = set()
        for noun_set in wn._synsets.values():
            nouns.add(list(noun_set)[0])
            
        actual = oc.outcast(nouns)
        target = 0, 1
        self.assertIn(actual, target)
    

    def test_001__outcast__of_two_synsets(self):
        
        # --- SET UP --- #
        n = 2
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            (0,  {} ) ,
            (1, {0} )
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = 0, 1
        self.assertIn(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = set()
        for noun_set in wn._synsets.values():
            nouns.add(list(noun_set)[0])

        actual = oc.outcast(nouns)
        target = 0, 1
        self.assertIn(actual, target)
    

    def test_002__outcast__of_three_synsets_in_a_sequence(self):
        
        # --- SET UP --- #
        n = 3
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            ( 0, {}  ),
            ( 1, {0} ),
            ( 2, {1} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = 0, 2
        self.assertIn(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'0', '1'}
        actual = oc.outcast(nouns)
        target = 0
        self.assertEqual(actual, target)
    
        nouns = {'2', '1'}
        actual = oc.outcast(nouns)
        target = 2
        self.assertEqual(actual, target)
    

    def test_003__outcast__of_three_synsets_in_a_binary_tree(self):
        
        # --- SET UP --- #
        n = 3
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            ( 0, {}  ),
            ( 1, {0} ),
            ( 2, {0} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = 1, 2
        self.assertIn(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'0', '1'}
        actual = oc.outcast(nouns)
        target = 1
        self.assertEqual(actual, target)

        nouns = {'0', '2'}
        actual = oc.outcast(nouns)
        target = 2
        self.assertEqual(actual, target)
    
        nouns = {'2', '1'}
        actual = oc.outcast(nouns)
        target = 1, 2
        self.assertIn(actual, target)


    def test_004__outcast__one_specific_outcast(self):
        
        # --- SET UP --- #
        n = 5
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            ( 0, {}  ),
            ( 1, {0} ),
            ( 2, {0} ),
            ( 3, {1} ),
            ( 4, {1} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = 2
        self.assertEqual(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'1', '4'}
        actual = oc.outcast(nouns)
        target = 4
        self.assertEqual(actual, target)
    
        nouns = {'0', '1'}
        actual = oc.outcast(nouns)
        target = 0
        self.assertEqual(actual, target)


    def test_005__outcast(self):
        
        # --- SET UP --- #
        n = 10
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            (0, {}     ),
            (1, {0}    ),
            (2, {0}    ),
            (3, {1, 5} ),
            (4, {1}    ),
            (5, {1, 2} ),
            (6, {2, 0} ),
            (7, {5}    ),
            (8, {6}    ),
            (9, {8, 0} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        """distance sum
        {   
            0: 55,
            1: 55,
            2: 65,
            3: 76,
            4: 85,
            5: 61,
            6: 69,
            7: 93,
            8: 93,
            9: 76
        }
        """

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = [7, 8]
        self.assertIn(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'9', '4', '3'}
        actual = oc.outcast(nouns)
        target = 4
        self.assertEqual(actual, target)
    
        nouns = {'0', '1', '2'}
        actual = oc.outcast(nouns)
        target = 2
        self.assertEqual(actual, target)
        
        nouns = {'5', '6', '2'}
        actual = oc.outcast(nouns)
        target = 6
        self.assertEqual(actual, target)
        
        nouns = {'7', '9'}
        actual = oc.outcast(nouns)
        target = 7
        self.assertEqual(actual, target)
