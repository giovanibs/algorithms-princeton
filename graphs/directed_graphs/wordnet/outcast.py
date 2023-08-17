import colored_traceback.auto
from wordnet import WordNet
from collections import deque
from typing import Iterable


class Outcast:

    def __init__(self, wn: WordNet) -> None:
        self._wn = wn
        self._visited: dict = dict()


    def outcast(self, nouns: Iterable[str]|None = None) -> set[int]:
        """
        Returns  a list containing synsets for which the total
        distance to all other synsets is highest among the
        provided nouns or every noun in the graph.

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

        3) Recursively call `outcast` with the candidates.
        """
        
        if nouns is None:
            # get all pure hyper/hyponyms, which are candidates to
            # be the outcast
            synsets_id = self._pure_hypernyms() | self._pure_hyponyms() 
        else:
            # use the nouns given by the client
            synsets_id = self._validate_nouns(nouns)
        
        return self._outcast(synsets_id)
        

    def _outcast(self, synsets_id: set[int]):
        remoteness = dict()
        
        for synset_id in synsets_id:
            remoteness[synset_id] = self._bfs(synset_id)

        max_dist = max(remoteness.values())

        return set( k for k, v in remoteness.items() if v == max_dist )
    

    def _pure_hypernyms(self):
        """
            Returns a set with synsets that has no hypernyms (a source).
        """
        synsets = set(self._wn._synsets)
        hypernyms = set(self._wn._hypernyms.keys())
        
        return synsets.difference(hypernyms)


    def _pure_hyponyms(self):
        """
            Returns a set with synsets that has no hyponyms (a leaf).
        """
        synsets = set(self._wn._synsets)
        hyponyms = set(self._wn._hyponyms.keys())
        
        return synsets.difference(hyponyms)


    def _validate_nouns(self, nouns):
        """
        Asserts that the given `nouns` are in the graph and
        returns the id of their respective synset.
        """
        synsets_ids = set()

        for noun in nouns:
            
            if not self._wn.is_noun(noun):
                raise ValueError(f"{noun!r} is not in the WordNet.")
            
            synsets_ids.update(self._wn._id_of(noun, first = False))

        return synsets_ids
    

    def _bfs(self, source: int):
        """
        """
        self._visited = {source: True}
        
        q = deque([source])
        
        dist_sum = 0
        current_dist = 1
        
        while q:
            s = q.popleft()
            connected = self._wn._connected_to(s)

            for c in connected:
                
                if c in q or self._visited.get(c, False):
                    continue

                self._visited[c] = True
                q.append(c)
                dist_sum += current_dist
        
            current_dist += 1

        return dist_sum
    

# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest


class TestsOutcastImplementation(unittest.TestCase):

    def test_000_validate_nouns(self):
        # --- SET UP --- #
        n = 10
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = []
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        nouns = {str(id) for id in range(n)}
        expected = {id for id in range(n)}
        ids = oc._validate_nouns(nouns)
        self.assertSetEqual(ids, expected)
    

    def test_101_pure_hyper_and_hyponyms__single_vertex(self):
        # --- SET UP --- #
        n = 1
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = []
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- TEST --- #
        pure_hyper = oc._pure_hypernyms()
        pure_hypo  = oc._pure_hyponyms()
        expected   = {0}
        
        self.assertSetEqual(pure_hyper, expected)
        self.assertSetEqual(pure_hypo, expected)
    

    def test_102_pure_hyper_and_hyponyms__two_vertices(self):
        # --- SET UP --- #
        n = 2
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [ (0, {1}) ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- TEST --- #
        pure_hyper = oc._pure_hypernyms()
        pure_hypo  = oc._pure_hyponyms()
        expected_hyper = {1}
        expected_hypo  = {0}
        
        self.assertSetEqual(pure_hyper, expected_hyper)
        self.assertSetEqual(pure_hypo, expected_hypo)
    

    def test_103_pure_hyper_and_hyponyms__binary_tree(self):
        # --- SET UP --- #
        n = 3
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [ (1, {0}), (2, {0}) ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- TEST --- #
        pure_hyper = oc._pure_hypernyms()
        pure_hypo  = oc._pure_hyponyms()
        expected_hyper = {0}
        expected_hypo  = {1, 2}
        
        self.assertSetEqual(pure_hyper, expected_hyper)
        self.assertSetEqual(pure_hypo, expected_hypo)
    

    def test_104_pure_hyper_and_hyponyms__three_on_directed_path(self):
        # --- SET UP --- #
        n = 3
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [ (0, {1}), (1, {2}) ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- TEST --- #
        pure_hyper = oc._pure_hypernyms()
        pure_hypo  = oc._pure_hyponyms()
        expected_hyper = {2}
        expected_hypo  = {0}
        
        self.assertSetEqual(pure_hyper, expected_hyper)
        self.assertSetEqual(pure_hypo, expected_hypo)
    

    def test_105_pure_hyper_and_hyponyms__two_from_top_and_two_from_bot(self):
        # --- SET UP --- #
        n = 5
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            (2, {1, 0}  ),
            (3, {2}     ),
            (4, {2}     )
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- TEST --- #
        pure_hyper = oc._pure_hypernyms()
        pure_hypo  = oc._pure_hyponyms()
        expected_hyper = {0, 1}
        expected_hypo  = {3, 4}
        
        self.assertSetEqual(pure_hyper, expected_hyper)
        self.assertSetEqual(pure_hypo, expected_hypo)
    

class TestsOutcast(unittest.TestCase):
    def test_000__outcast__reflexive(self):
        
        # --- SET UP --- #
        n = 1
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [  ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)
        
        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = {0}
        self.assertEqual(actual, target)
    
        
        # --- ASSERT BY NOUN --- #
        nouns = set()
        for noun_set in wn._synsets.values():
            nouns.add(list(noun_set)[0])
            
        actual = oc.outcast(nouns)
        target = {0}
        self.assertEqual(actual, target)
    

    def test_001__outcast__of_two_synsets(self):
        
        # --- SET UP --- #
        n = 2
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            (1, {0} )
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = {0, 1}
        self.assertEqual(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = set()
        for noun_set in wn._synsets.values():
            nouns.add(list(noun_set)[0])

        actual = oc.outcast(nouns)
        target = {0, 1}
        self.assertEqual(actual, target)
    

    def test_002__outcast__of_three_synsets_in_a_sequence(self):
        
        # --- SET UP --- #
        n = 3
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            ( 1, {0} ),
            ( 2, {1} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = {0, 2}
        self.assertEqual(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'0', '1'}
        actual = oc.outcast(nouns)
        target = {0}
        self.assertEqual(actual, target)
    
        nouns = {'2', '1'}
        actual = oc.outcast(nouns)
        target = {2}
        self.assertEqual(actual, target)
    

    def test_003__outcast__of_three_synsets_in_a_binary_tree(self):
        
        # --- SET UP --- #
        n = 3
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            ( 1, {0} ),
            ( 2, {0} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = {1, 2}
        self.assertEqual(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'0', '1'}
        actual = oc.outcast(nouns)
        target = {1}
        self.assertEqual(actual, target)

        nouns = {'0', '2'}
        actual = oc.outcast(nouns)
        target = {2}
        self.assertEqual(actual, target)
    
        nouns = {'2', '1'}
        actual = oc.outcast(nouns)
        target = {1, 2}
        self.assertEqual(actual, target)


    def test_004__outcast__one_specific_outcast(self):
        
        # --- SET UP --- #
        n = 5
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
            ( 1, {0} ),
            ( 2, {0} ),
            ( 3, {1} ),
            ( 4, {1} ),
        ]
        wn = WordNet(synsets, hypernyms)
        oc = Outcast(wn)

        
        # --- ASSERT BY ID --- #
        actual = oc.outcast()
        target = {2}
        self.assertEqual(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'1', '4'}
        actual = oc.outcast(nouns)
        target = {4}
        self.assertEqual(actual, target)
    
        nouns = {'0', '1'}
        actual = oc.outcast(nouns)
        target = {0}
        self.assertEqual(actual, target)


    def test_005__outcast(self):
        
        # --- SET UP --- #
        n = 10
        synsets = [ (id, {str(id)}) for id in range(n) ]
        hypernyms = [
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
        target = {7, 8}
        self.assertEqual(actual, target)

        
        # --- ASSERT BY NOUN --- #
        nouns = {'9', '4', '3'}
        actual = oc.outcast(nouns)
        target = {4}
        self.assertEqual(actual, target)
    
        nouns = {'0', '1', '2'}
        actual = oc.outcast(nouns)
        target = {2}
        self.assertEqual(actual, target)
        
        nouns = {'5', '6', '2'}
        actual = oc.outcast(nouns)
        target = {6}
        self.assertEqual(actual, target)
        
        nouns = {'7', '9'}
        actual = oc.outcast(nouns)
        target = {7}
        self.assertEqual(actual, target)
