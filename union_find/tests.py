import unittest
from QuickUnion import QuickUnion
from QuickFind import QuickFind
from WeightedQuickUnion import WeightedQuickUnionSize, WeightedQuickUnionHeight, WeightedQuickUnionHeightPathCompression

class TestQuickUnion(unittest.TestCase):
    def setUp(self) -> None:
        self.new_union_find = QuickUnion
        
    
    def test_valid_object_creation(self):
        self.n = 3
        uf = self.new_union_find(self.n)
        self.assertEqual(uf.sets_count, self.n)

    def test_invalid_object_creation(self):
        negative_n = -1
        zero_n = 0
        with self.assertRaises(ValueError):
            self.new_union_find(negative_n)
        with self.assertRaises(ValueError):
            self.new_union_find(zero_n)

    def test_find(self):
        n = 3
        uf = self.new_union_find(n)

        for node in range(3):
            self.assertEqual(uf.find(node), node)

    def test_find_argument_not_in_range(self):
        n = 3
        uf = self.new_union_find(n)

        with self.assertRaises(IndexError):
            uf.find(-n)
        with self.assertRaises(IndexError):
            uf.find(n)

    def test_union(self):
        n = 3
        uf = self.new_union_find(n)

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
        uf = self.new_union_find(n)

        with self.assertRaises(IndexError):
            uf.union(0, -n)
        with self.assertRaises(IndexError):
            uf.union(0, n)

    def test_relation_transitive(self):
        n = 3
        uf = self.new_union_find(n)

        union_operations = [
            (0, 1),
            (0, 2),
        ]

        for node1, node2 in union_operations:
            uf.union(node1, node2)

        self.assertTrue(uf.are_connected(1, 2))


class TestQuickFind(TestQuickUnion):
    def setUp(self) -> None:
        self.new_union_find = QuickFind
        
    
    def test_union(self):
        n = 3
        qf = self.new_union_find(n)

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
        

class TestWeightedQuickUnionSize(TestQuickUnion):
    def setUp(self) -> None:
        self.new_union_find = WeightedQuickUnionSize
    
    def test_size_init(self):
        n = 3
        uf = self.new_union_find(n)
        
        for size in uf.size:
            self.assertEqual(size, 1)
        
    def test_size(self):
        n = 5
        uf = self.new_union_find(n)
        uf.union(0, 1)
        self.assertEqual(uf.size[0], 2)
        uf.union(2, 0)
        self.assertEqual(uf.size[0], 3)
        uf.union(3, 4)
        self.assertEqual(uf.size[3], 2)
        uf.union(3, 0)
        self.assertEqual(uf.size[0], 5)

        
class TestWeightedQuickUnionHeight(TestQuickUnion):
    def setUp(self) -> None:
        self.new_union_find = WeightedQuickUnionHeight
    
    def test_height_init(self):
        n = 3
        uf = self.new_union_find(n)
        
        for height in uf.height:
            self.assertEqual(height, 0)
        
    def test_same_height(self):
        n = 2
        uf = self.new_union_find(n)
        uf.union(0, 1)
        self.assertEqual(uf.height[0], 1)
    
    def test_different_height(self):
        n = 9
        uf = self.new_union_find(n)
        uf.union(0, 1)
        self.assertEqual(uf.height[uf.find(0)], 1)
        uf.union(1, 2)
        self.assertEqual(uf.height[uf.find(0)], 1)
        uf.union(3, 4)
        uf.union(4, 0)
        self.assertEqual(uf.height[uf.find(0)], 2)
        uf.union(5, 6)
        uf.union(7, 8)
        uf.union(8, 5)
        self.assertEqual(uf.height[uf.find(5)], 2)
        uf.union(5, 0)
        self.assertEqual(uf.height[uf.find(5)], 3)
        self.assertEqual(max(uf.height), 3)


class TestWeightedQuickUnionHeightPathCompression(TestQuickUnion):
    def setUp(self) -> None:
        self.new_union_find = WeightedQuickUnionHeightPathCompression
    
    def test_height_init(self):
        n = 3
        uf = self.new_union_find(n)
        
        for height in uf.height:
            self.assertEqual(height, 0)
        
    def test_same_height(self):
        n = 2
        uf = self.new_union_find(n)
        uf.union(0, 1)
        self.assertEqual(uf.height[0], 1)
    
    def test_different_height(self):
        n = 9
        uf = self.new_union_find(n)
        uf.union(0, 1)
        self.assertEqual(uf.height[uf.find(0)], 1)
        uf.union(1, 2)
        self.assertEqual(uf.height[uf.find(0)], 1)
        uf.union(3, 4)
        uf.union(4, 0)
        self.assertEqual(uf.height[uf.find(0)], 2)
        uf.union(5, 6)
        uf.union(7, 8)
        uf.union(8, 5)
        self.assertEqual(uf.height[uf.find(5)], 2)
        uf.union(5, 0)
        self.assertEqual(uf.height[uf.find(5)], 3)
        self.assertEqual(max(uf.height), 3)
        

if __name__ == "__main__":
    unittest.main()
