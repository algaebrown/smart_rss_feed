import unittest
from src.embedding import compute_embeddings

class TestEmbedding(unittest.TestCase):
    def test_embedding_shape(self):
        texts = ["Hello world!", "Test sentence."]
        embeddings = compute_embeddings(texts)
        self.assertEqual(len(embeddings), 2)
        self.assertTrue(all(isinstance(vec, list) for vec in embeddings))
        self.assertTrue(all(len(vec) > 0 for vec in embeddings))

if __name__ == "__main__":
    unittest.main()
