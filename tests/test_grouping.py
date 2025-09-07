import unittest
from src.grouping import group_by_cosine_similarity
import numpy as np


class TestGrouping(unittest.TestCase):
    def test_group_by_cosine_similarity(self):
        # Create dummy embeddings: 3 similar, 2 different
        emb = [[1, 0, 0], [0.99, 0.01, 0], [0.98, 0.02, 0], [0, 1, 0], [0, 0.99, 0.01]]
        groups = group_by_cosine_similarity(emb, threshold=0.95)
        # There should be 2 groups: first 3 together, last 2 together
        group_sizes = sorted([len(g) for g in groups.values()])
        self.assertEqual(group_sizes, [2, 3])
        # Check that all indices are present
        all_indices = sorted([i for group in groups.values() for i in group])
        self.assertEqual(all_indices, list(range(5)))


if __name__ == "__main__":
    unittest.main()
