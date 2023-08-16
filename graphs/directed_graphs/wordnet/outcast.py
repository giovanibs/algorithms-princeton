from wordnet import WordNet, TestsInitWordNet, TestsPublicAPI

class Outcast:
    def __init__(self, wn: WordNet) -> None:
        self.wn = wn
        self.visited = dict()
        self.dist_to = dict()
        self.edge_to = dict()

    def _bfs(self, a: int, b: int|None = None):

        q = deque([a])              # let's start a FIFO queue with `a` (could be `b`)
        visited = {a: False} # and  keep track of the visited synsets.
        dist_to = {a: 0}     # The distance from `a` to itself is zero.
        edge_to = {a: a}     # The edge_to `a` is itself.
        

        # --- NON-RECURSIVE
        while q:
            synset = q.popleft() # first round it is `a`
            
            # let's mark the `synset` as visited
            visited[synset] = True

            # we're gonna run an UNDIRECTED search, so BOTH hypernyms AND
            # hyponyms of `synset` are modeled as (undirectly) connected:
            connected_synsets = self._connected_to(synset)

            # if, by any chance, `b` is connected to `synset`,
            # we're done: we found the last synset to `b` so...
            if b and b in connected_synsets:
                edge_to[b] = synset              # let's put it as edge_to `b`,
                dist_to[b] = dist_to[synset] + 1 # update its dist_to `a`
                
                break # search is done.

            # Now, let's put every connected synset `cs` in the queue...
            for cs in connected_synsets:
                # ...except for those already in the queue / visited in the loop
                if cs not in q and not visited.get(cs, False):
                    q.append(cs)
                    visited[cs] = True                  # mark it as visited
                    edge_to[cs] = synset                # undirected edge!!!
                    dist_to[cs] = dist_to[synset] + 1   # `previous dist.` + 1

        return dist_to, edge_to, visited

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
            return next(iter(self._synsets))
        
        distances: dict[int, int] = {}

        # get the distances from every given noun (or all nouns
        # if None is given) to every other synset.
        for synset in synsets:
            dist_to = self._bfs(synset)[0]
            distances[synset] = sum(dist_to.values())

        return max(distances.items(), key=max)[0]

    def _validate_nouns(self, nouns):
        if nouns is None:
            return self._synsets.keys()
        
        synsets_ids = set()

        for noun in nouns:
            
            if not self.is_noun(noun):
                raise ValueError(f"{noun!r} is not in the WordNet.")
            
            synsets_ids.update(self.wn._id_of(noun, first = False))

        return synsets_ids


# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest


class TestsOutcast(unittest.TestCase):
    WordNetDouble = TestsPublicAPI.WordNetDouble

    def test_000__outcast__reflexive(self):
        # --- set up
        wn = TestsOutcast.WordNetDouble()
        n = 1
        wn._synset_count = n
        
        wn._synsets = { id: {str(id)} for id in range(n) }
        wn._hypernyms = {
            0: {}     ,
        }
        wn._set_hyponyms(wn._hypernyms, wn._hyponyms)

        # --- assert by id
        actual = wn.outcast()
        target = 0
        self.assertEqual(actual, target)
    
        # --- by noun
        # assert by noun
        nouns = set()
        for noun_set in wn._synsets.values():
            nouns.add(list(noun_set)[0])
            
        actual = wn.outcast(nouns)
        target = 0, 1
        self.assertIn(actual, target)
    
    def test_001__outcast__of_two_synsets(self):
        wn = TestsOutcast.WordNetDouble()
        n = 2
        wn._synset_count = n

        wn._synsets = { id: {str(id)} for id in range(n) }
        wn._hypernyms = {
            0: {}     ,
            1: {0}     ,
        }
        wn._set_hyponyms(wn._hypernyms, wn._hyponyms)
        
        actual = wn.outcast()
        target = 0, 1
        self.assertIn(actual, target)

        # assert by noun
        nouns = set()
        for noun_set in wn._synsets.values():
            nouns.add(list(noun_set)[0])

        actual = wn.outcast(nouns)
        target = 0, 1
        self.assertIn(actual, target)
    
    def test_002__outcast__of_three_synsets_in_a_sequence(self):
        wn = TestsOutcast.WordNetDouble()
        n = 3
        wn._synset_count = n

        wn._synsets = { id: {str(id)} for id in range(n) }
        wn._hypernyms = {
            0: {}     ,
            1: {0}     ,
            2: {1}     ,
        }
        wn._set_hyponyms(wn._hypernyms, wn._hyponyms)
        
        actual = wn.outcast()
        target = 0, 2
        self.assertIn(actual, target)

        # assert by noun
        nouns = {'0', '1'}
            
        actual = wn.outcast(nouns)
        target = 0
        self.assertEqual(actual, target)
    
        # assert by noun
        nouns = {'2', '1'}
            
        actual = wn.outcast(nouns)
        target = 2
        self.assertEqual(actual, target)
    
    def test_003__outcast__of_three_synsets_in_a_binary_tree(self):
        wn = TestsOutcast.WordNetDouble()
        n = 3
        wn._synset_count = n

        wn._synsets = { id: {str(id)} for id in range(n) }
        wn._hypernyms = {
            0: {}     ,
            1: {0}     ,
            2: {0}     ,
        }
        wn._set_hyponyms(wn._hypernyms, wn._hyponyms)

        actual = wn.outcast()
        target = 1, 2
        self.assertIn(actual, target)

        # assert by noun
        nouns = {'0', '1'}
            
        actual = wn.outcast(nouns)
        target = 1
        self.assertEqual(actual, target)
    
        # assert by noun
        nouns = {'0', '2'}
            
        actual = wn.outcast(nouns)
        target = 2
        self.assertEqual(actual, target)
    
        # assert by noun
        nouns = {'2', '1'}
            
        actual = wn.outcast(nouns)
        target = 1, 2
        self.assertIn(actual, target)

    def test_004__outcast__one_specific_outcast(self):
        wn = TestsOutcast.WordNetDouble()
        n = 5
        wn._synset_count = n

        wn._synsets = { id: {str(id)} for id in range(n) }
        wn._hypernyms = {
            0: {}     ,
            1: {0}     ,
            2: {0}     ,
            3: {1}     ,
            4: {1}     ,
        }
        wn._set_hyponyms(wn._hypernyms, wn._hyponyms)

        actual = wn.outcast()
        target = 2
        self.assertEqual(actual, target)

        # assert by noun
        nouns = {'1', '4'}
            
        actual = wn.outcast(nouns)
        target = 4
        self.assertEqual(actual, target)
    
        # assert by noun
        nouns = {'0', '1'}
            
        actual = wn.outcast(nouns)
        target = 0
        self.assertEqual(actual, target)

    def test_005__outcast(self):
        wn = self.WordNetDouble()
        n  = 10
        wn._synset_count = n
        
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

        # outcast from all
        actual = wn.outcast()
        target = [7,
        8]
        self.assertIn(actual, target)

        # outcast by nouns
        nouns = {'9', '4', '3'}
            
        actual = wn.outcast(nouns)
        target = 4
        self.assertEqual(actual, target)
    
        # assert by noun
        nouns = {'0', '1', '2'}
            
        actual = wn.outcast(nouns)
        target = 2
        self.assertEqual(actual, target)
        
        # assert by noun
        nouns = {'5', '6', '2'}
            
        actual = wn.outcast(nouns)
        target = 6
        self.assertEqual(actual, target)
        
        # assert by noun
        nouns = {'7', '9'}
            
        actual = wn.outcast(nouns)
        target = 7
        self.assertEqual(actual, target)
