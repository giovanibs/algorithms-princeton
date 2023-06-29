import unittest
from UnionFind import UnionFind
from QuickFind import QuickFind


class TestUnionFind(unittest.TestCase):
    def test_valid_object_creation(self):
        n = 3
        uf = UnionFind(3)
        self.assertEqual(uf.sets_count, n)

    def test_invalid_object_creation(self):
        negative_n = -1
        zero_n = 0
        with self.assertRaises(ValueError):
            UnionFind(negative_n)
        with self.assertRaises(ValueError):
            UnionFind(zero_n)

    def test_find(self):
        n = 3
        uf = UnionFind(n)

        for element in range(3):
            self.assertEqual(uf.find(element), element)

    def test_find_argument_not_in_range(self):
        n = 3
        uf = UnionFind(n)

        with self.assertRaises(IndexError):
            uf.find(-n)
        with self.assertRaises(IndexError):
            uf.find(n)

    def test_union(self):
        n = 3
        uf = UnionFind(n)

        # store return value to test
        sets_count = uf.union(0, 1)
        self.assertEqual(uf.sets_count, 2)
        self.assertEqual(uf.sets_count, sets_count)
        
        # test connections
        self.assertTrue(uf.are_connected(0,1))  # 0 and 1 are connected
        self.assertFalse(uf.are_connected(0,2)) # 0 and 2 are not connected
        self.assertFalse(uf.are_connected(1,2)) # 1 and 2 are not connected

    def test_union_argument_not_in_range(self):
        n = 3
        uf = UnionFind(n)

        with self.assertRaises(IndexError):
            uf.union(0, -n)
        with self.assertRaises(IndexError):
            uf.union(0, n)

    def test_relation_transitive(self):
        n = 3
        uf = UnionFind(n)

        union_operations = [
            (0, 1),
            (0, 2),
        ]

        for element1, element2 in union_operations:
            uf.union(element1, element2)

        self.assertTrue(uf.are_connected(1, 2))


class TestQuickFind(TestUnionFind):
    def test_union(self):
        n = 3
        qf = QuickFind(n)

        # store return value to test
        sets_count = qf.union(0, 1)
        self.assertEqual(qf.sets_count, 2)
        self.assertEqual(qf.sets_count, sets_count)
        
        # test connections
        self.assertTrue(qf.are_connected(0,1))  # 0 and 1 are connected
        self.assertFalse(qf.are_connected(0,2)) # 0 and 2 are not connected
        self.assertFalse(qf.are_connected(1,2)) # 1 and 2 are not connected
        
        sets_count = qf.union(0, 2)
        self.assertEqual(qf.find(0), qf.find(2))
        self.assertEqual(qf.find(1), qf.find(2))
        self.assertEqual(qf.find(0), 2)
        
        


if __name__ == "__main__":
    unittest.main()
