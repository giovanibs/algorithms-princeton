import colored_traceback.auto
from pathlib import Path
from typing import Iterable
from collections import deque

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
        that `w` is a hypernym of `v`;
        
    ### Corner cases.
    
    Raise an exception in the following situations:

        - Any argument to the constructor or
        an instance method is null;

        - The input to the constructor does not
        correspond to a rooted DAG;

        - Any of the noun arguments in distance()
        or sap() is not a WordNet noun. 

    """
    NOT_A_STRING = "Noun must be a string."

    def __init__(
            self,
            synsets  :  Path | Iterable[ tuple[int, set[str] ]],
            hypernyms:  Path | Iterable[ tuple[int, set[int] ]]
    ):
        """
        Constructor takes an iterable or the name of the two input files (CSV):
        
        - List of synsets: contains all noun synsets in WordNet,
        one per line (VERTICES). The fields are:
                - `synset_id`, `synset`, `gloss`
        
        - List of hypernyms: contains the hypernym relationships (the EDGES).
        The fields are:
                - `synset_id`, `hypernym_0`, `hypernym_1`, ... `hypernym_n`
        
        """
        
        # --- IF ANY ARGUMENT IS A PATH:
        try:
            synsets_path = Path(synsets)
            synsets = self._synsets_from_path(synsets_path)
        except TypeError as e:
            if "expected str, bytes or os.PathLike object" not in str(e):
                raise e
        
        try:
            hypernyms_path = Path(hypernyms)
            hypernyms = self._hypernyms_from_path(hypernyms_path)
        except TypeError as e:
            if "expected str, bytes or os.PathLike object" not in str(e):
                raise e

        # --- INIT INSTANCE VARIABLES
        self._synsets  : dict[int, set[str]] = dict(synsets)
        self._hypernyms: dict[int, set[int]] = dict(hypernyms)
        self._hyponyms : dict[int, set[int]] = dict()
        self._synset_count  : int = len(self._synsets)

        # gather the hyponyms
        self._set_hyponyms(self._hypernyms, self._hyponyms)


    @classmethod
    def _set_hyponyms(cls, hypernyms: dict, hyponyms: dict):
        hyponyms.clear()
        for synset_id, hypernym_set in hypernyms.items():

            for hypernym_id in hypernym_set:
                try:
                    hyponyms[hypernym_id].add(synset_id)
                except KeyError:
                    hyponyms[hypernym_id] = {synset_id}


    @classmethod
    def _synsets_from_path(cls, synsets_path):
        synsets = []
            
        with open(synsets_path) as f:
            for line in f:
                    # read from line
                synset_id, synonyms, *_ = line.strip().split(',')
                    # cast to appropriate type
                synset = int(synset_id), set(synonyms.split())
                synsets.append(synset)
        return synsets


    @classmethod
    def _hypernyms_from_path(cls, hypernyms_path):
        hypernyms = []
            
        with open(hypernyms_path) as f:
            for line in f:
                    # read from file
                synset_id, *hypernym_list = line.strip().split(',')
                    # cast to appropriate type
                hypernym_list = map(int, hypernym_list)
                hypernym = int(synset_id), set(hypernym_list)
                    # add to set
                hypernyms.append(hypernym)
        return hypernyms

    @classmethod
    def _validate_noun(self, noun):
        if not isinstance(noun, str):
            raise TypeError(WordNet.NOT_A_STRING)

    # ---------------------------------
    # --- HELPERS
    def _id_of(self, noun: str, first: bool = True) -> int|None:
        self._validate_noun(noun)

        if not self.is_noun(noun): return None
        ids = [id for id, synset in self._synsets.items() if noun in synset]
        
        return ids[0] if first else ids
    
    def _connected_to(self, synset_id):
        connected_synsets = self.hyper_of(synset_id) \
                                .union(self.hypo_of(synset_id))
                            
        return connected_synsets

    # ---------------------------------
    # PUBLIC API
    @property
    def nouns(self) -> list:
        """
        returns all WordNet nouns
        """
        return [noun for nouns in self._synsets.values() for noun in nouns]
    
    def is_noun(self, word):
        """
        is the word a WordNet noun?
        """
        return word in self.nouns
    
    def hyper_of(self, synset_id: int) -> set[int]:
        return self._hypernyms.get(synset_id) or set()
    
    def hypo_of(self, synset_id: int) -> set[int]:
        return self._hyponyms.get(synset_id) or set()

    def distance(self, noun_a: str, noun_b: str):
        """
        Measuring the semantic relatedness of two nouns:
        Semantic relatedness refers to the degree to which
        two concepts are related.

        Returns the length of shortest ancestral path of subsets A and B.
        """
    
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
        
        
        self._validate_noun(noun_a)
        self._validate_noun(noun_b)

        # get synset_id of noun_a and noun_b, they could be different nouns,
        # but synonyms (i.e. part of the same synset.)
        a = self._id_of(noun_a)
        b = self._id_of(noun_b)

        if a == b:
            return [a], 0, a
        
        
        dist_to, edge_to, visited = self._bfs(a, b)
        
        # ----------- #
        # --- SAP --- #
        # Since we found a UNDIRECT path from `a` to `b`, let's trace back
        # each synset `s` starting from `b` by making use of the `edge_to`:
        sap = self._traceback_path(a, b, edge_to)
        
        # -------------------------------- #
        # --- Shortest Common Ancestor --- #
        sca    = None
        sca = self._sca(sap)         

        # FINALLY, we return the sap AND the distance from `a` to `b`
        return sap, dist_to[b], sca

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

    def _traceback_path(self, a: int, b: int, edge_to: dict[int, int]):
        sap    = [b]
        synset = b
        while True:
            synset = edge_to[synset]     # we keep following the path
            sap.append(synset)           # and recording it.

            if synset == a:
                break
        return sap
    
    def _sca(self, sap: iter) -> int:
        """
        Let's go through the sap until we reach the highest
        hypernym on the `sap`, that is either:
            - the synset whose successor is one of its hyponyms;
            - OR the last synset on the path.
        """
        for i, synset in enumerate(sap):
            is_last = i == len(sap)-1

            if is_last or sap[i+1] in self.hypo_of(synset):
                # keep sap[i+1] after is_last to prevent index overflow
                return synset

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
            
            synsets_ids.update(self._id_of(noun, first = False))

        return synsets_ids

            
    def _dfs(self,
             _id:      int,
             stack:   list[int],
             visited: dict[int, bool]) -> list:
        
        for synset_id in self.hyper_of(_id):
            if not visited[synset_id]:
                stack.append(self._dfs(synset_id, stack, visited))

        return _id


# ------------------------------------------------------------------------------
# --- UNIT TESTS
# ------------------------------------------------------------------------------
import unittest
import os

class TestsInitWordNet(unittest.TestCase):
    def test_000_init_with_iterables(self):
        synsets = [
            # synset_id, {nouns}
            (0, {"a_specific_noun", "another_specific_noun"}),
            (1, {"a_general_noun" , "another_general_noun"}),
            (2, {"a_more_general_noun" }),
        ]
        
        hypernyms = [
            # synset_id, {hypernyms}
            ( 0, {1, 2} ),
            ( 1, {2}    ),
        ]
        wn = WordNet(synsets, hypernyms)
        
        expected_hyponyms = dict([
            # synset_id, {hyponyms}
            ( 1, {0}    ),
            ( 2, {0, 1} ),
        ])

        self.assertDictEqual(wn._synsets  , dict(synsets)    )
        self.assertDictEqual(wn._hypernyms, dict(hypernyms)  )
        self.assertDictEqual(wn._hyponyms , expected_hyponyms)

    def test_001_init_from_path(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        synsets_path   = os.path.join(cwd, 'examples', 'synsets_sample.txt')
        hypernyms_path = os.path.join(cwd, 'examples', 'hypernyms_sample.txt')

        wn = WordNet(synsets_path, hypernyms_path)

        expected_synsets = dict([
            (0, {"a_specific_noun", "another_specific_noun"}),
            (1, {"a_general_noun" , "another_general_noun"}),
            (2, {"a_more_general_noun" }),
        ])
        
        expected_hypernyms = dict([
            (0, {1, 2}),
            (1, {2})
        ])
        expected_hyponyms  = dict([
            (1, {0}),
            (2, {0, 1})
        ])

        self.assertDictEqual(wn._synsets  , expected_synsets  )
        self.assertDictEqual(wn._hypernyms, expected_hypernyms)
        self.assertDictEqual(wn._hyponyms , expected_hyponyms )


class TestsPublicAPI(unittest.TestCase):
    class WordNetDouble(WordNet):
        def __init__(self):
            self._synsets      = None
            self._hypernyms    = None
            self._hyponyms     = dict()
            self._synset_count = None

    def setUp(self) -> None:
        self.synsets = [
            (0, {"a_specific_noun", "another_specific_noun"}),
            (1, {"a_general_noun" , "another_general_noun"}),
            (2, {"THE_Root"}),
            (3, {"whatever"}),
        ]
        
        self.hypernyms = [
            ( 0, {1, 2} ),
            ( 1, {2}    ),
            ( 3, {1, 2} ),
        ]

        self.wn = self.WordNetDouble()
        self.wn._synsets   = dict(self.synsets)
        self.wn._hypernyms = dict(self.hypernyms)
        self.wn._set_hyponyms(self.wn._hypernyms, self.wn._hyponyms)

    def test_000_nouns(self):
        expected = [noun for _, nouns in self.synsets for noun in nouns]
        self.assertEqual(self.wn.nouns, expected)

    def test_001_is_noun(self):
        for noun in self.wn.nouns:
            self.assertTrue(self.wn.is_noun(noun))

        self.assertFalse(self.wn.is_noun("not in this wordnet"))

    def test_002_hyper_of(self):
        EMPTY_SET = set()
        self.assertSetEqual(self.wn.hyper_of(0), {2, 1})
        self.assertSetEqual(self.wn.hyper_of(1), {2})
        self.assertSetEqual(self.wn.hyper_of(2), EMPTY_SET)
        self.assertSetEqual(self.wn.hyper_of(3), {1, 2})
    
    def test_003_hypo_of(self):
        EMPTY_SET = set()
        self.assertSetEqual(self.wn.hypo_of(0), EMPTY_SET)
        self.assertSetEqual(self.wn.hypo_of(1), {3, 0})
        self.assertSetEqual(self.wn.hypo_of(2), {1, 3, 0})
        self.assertSetEqual(self.wn.hypo_of(3), EMPTY_SET)


class TestsSAP(unittest.TestCase):
    WordNetDouble = TestsPublicAPI.WordNetDouble

    def setUp(self):
        wn = self.wn = self.WordNetDouble()
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
    

    def test_000__validation(self):
        with self.assertRaisesRegex(TypeError, WordNet.NOT_A_STRING):
            self.wn.sap(1, "0")
            self.wn.sap("1", 0)
            self.wn.sap("1", "0")
    

    def test_001__reflexive_sap(self):
        wn = self.wn
        
        for noun in range(self.n):
            output = wn.sap(str(noun), str(noun))
            target = [noun], 0, noun
            self.assertTupleEqual(output, target)
    

    def test_002__sap__from_hyper_to_hyponym(self):
        output = self.wn.sap('1', '4')
        target = [4, 1], 1, 1
        self.assertTupleEqual(output, target)
    

    def test_003__sap__from_hypo_to_hypernym(self):
        output = self.wn.sap('4', '1')
        target = ( path:=[1, 4], len(path)-1, 1 )
        self.assertTupleEqual(output, target)
        
    
    def test_004__sap__shortest_of_two(self):
        output = self.wn.sap('5', '9')
        target = ( path:=[9, 0, 1, 5], len(path)-1, 0)
        # longer:        [9, 8, 6, 2, 5]
        self.assertTupleEqual(output, target)
    
        output = self.wn.sap('9', '2')
        target = ( path:=[2, 0, 9], len(path)-1, 0)
        # longer:        [2, 6, 8, 9]
        self.assertTupleEqual(output, target)
    
    def test_005__sap__two_shortest(self):
        output = self.wn.sap('4', '8')
        targets = (
             (path:=[8, 9, 0, 1, 4], len(path)-1, 0),
             (path:=[8, 6, 0, 1, 4], len(path)-1, 0),
        )
        
        output = self.wn.sap('8', '4')
        targets = (
             (path:=[4, 1, 0, 9, 8], len(path)-1, 0),
             (path:=[4, 1, 0, 6, 8], len(path)-1, 0),
        )
        self.assertIn(output, targets)
        

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



if __name__ == "__main__":
    from timeit import timeit
    from os import path

    root           = path.dirname(path.abspath(__file__))
    synset_path    = path.join(root, r"examples/synsets10000-subgraph.txt"  )
    hypernyms_path = path.join(root, r"examples/hypernyms10000-subgraph.txt")
    
    wn = WordNet(synset_path, hypernyms_path)
    
    outcast_nouns = ['apple', 'banana']
    n = 10
    average_time = timeit(lambda: wn.outcast(outcast_nouns), number=n)/n
    print(f"Average time per execution: {average_time} seconds")
