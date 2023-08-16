from wordnet import WordNet
from collections import deque
from sap import SAP


class Outcast:

    def __init__(self, wn: WordNet) -> None:
        self._wn = wn
        self._visited: dict
        self._dist_from_to: dict[int, dict[int, int]]
        
        #   _dist_from_to = {
        #                   from: {
        #                       { to_0: distance_0 },
        #                       { to_1: distance_1 }
        #                   }
        #   }
        

    def outcast(self, nouns: iter[str]|None = None) -> list[int]:
        """
        To identify an outcast, compute the sum of the distances
        between each noun and every other one and return a noun
        (or nouns) for which the distance is maximum.

        ### TOPOLOGICAL-FIRST APPROACH:

        Specialized algorithm for identifying THE outcast of a graph.

        The assumption for this algorithm is that the outcast must
        be a hypernym from the top of the topologically sorted graph
        or a pure hyponym at its bottom. 

        Based on assumption, the time complexity is reduced since we
        are not checking the all of the synsets for its distances to
        other synsets.

        The topological order is the reversed post-order of a graph.
        Alternatively, we could use the normal postorder of a graph
        as well, but taking the hypernyms from its bottom and the
        hyponyms from its top.

        Steps:

        1) Preparing the topological order:
            - run `dfs` for any noun and return its postorder
            
        2) Picking candidates
            - iterate from the top of the topological order and enqueue
            each synset until you find the first hyponym;
            - iterate from the bottom enqueue each synset until you find
            the first hypernym;

        3) Calculate the SAP from each candidate to every other synset.

        4) Get the synset from canditates that have the largest distance.
        """
        
        

    def _bfs(self, q: deque, previous_dist: int = 0):
        """
        """

        s = q.popleft()
        self._dist_from_to[s] = { s: previous_dist }
        self._visited[s] = True
        
        connected_synsets = self._wn._connected_to(s)

        for cs in connected_synsets:
            
            if cs in q or self._visited.get(cs, False):
                continue

            q.append(cs)
            self._visited[cs] = True

            dist = previous_dist + 1
            self._dist_from_to[s][cs] = dist
            self._dist_from_to[cs] = {  cs: 0    ,  # initiate
                                        s : dist }  # save reflexive dist
            
        
        previous_dist += 1
    

    def _validate_nouns(self, nouns):
        # ========== OLD ============
        # if nouns is None:
        #     return self._wn._synsets.keys()
        
        # synsets_ids = set()

        # for noun in nouns:
            
        #     if not self._wn.is_noun(noun):
        #         raise ValueError(f"{noun!r} is not in the WordNet.")
            
        #     synsets_ids.update(self._wn._id_of(noun, first = False))

        # return synsets_ids
        # ========== END OLD ============
        
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
