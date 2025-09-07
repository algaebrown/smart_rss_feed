import unittest
import numpy as np
from clustering import tsne_cluster


class TestTSNEClustering(unittest.TestCase):
    def test_tsne_cluster_shape(self):
        # Create dummy embeddings
        embeddings = [[0.1 * i, 0.2 * i, 0.3 * i] for i in range(10)]
        X_embedded = tsne_cluster(embeddings, perplexity=3)
        self.assertIsInstance(X_embedded, np.ndarray)
        self.assertEqual(X_embedded.shape[1], 2)
        self.assertEqual(X_embedded.shape[0], len(embeddings))


if __name__ == "__main__":
    unittest.main()
