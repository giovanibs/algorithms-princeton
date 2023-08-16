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
    def _connected_to(self, synset_id):
        connected_synsets = self.hyper_of(synset_id) \
                                .union(self.hypo_of(synset_id))
                            
        return connected_synsets


    def _id_of(self, noun: str, first: bool = True) -> int|None:
            self._validate_noun(noun)

            if not self.is_noun(noun):
                return None
            
            ids = [
                id for id, synset in self._synsets.items() if noun in synset
            ]
            
            return ids[0] if first else ids


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
