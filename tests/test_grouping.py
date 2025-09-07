import unittest
from src.grouping import group_by_cosine_similarity, render_similar_articles
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


class TestRenderSimilarArticles(unittest.TestCase):
    def setUp(self):
        from types import SimpleNamespace

        # Create mock articles with embeddings
        self.selected_article = SimpleNamespace(
            title="Selected Article", embedding=[1.0, 0.0], user_selected=True
        )
        self.other_article_1 = SimpleNamespace(
            title="Similar Article", embedding=[0.9, 0.1], user_selected=False
        )
        self.other_article_2 = SimpleNamespace(
            title="Dissimilar Article", embedding=[0.0, 1.0], user_selected=False
        )
        self.other_article_3 = SimpleNamespace(
            title="Already Selected", embedding=[1.0, 0.0], user_selected=True
        )
        self.articles = [
            self.other_article_1,
            self.other_article_2,
            self.other_article_3,
        ]

    def test_similar_articles_above_threshold(self):
        # Should return only the similar article above threshold
        results = render_similar_articles(
            self.selected_article, self.articles, threshold=0.7
        )
        self.assertIn("Similar Article", results)
        self.assertNotIn("Dissimilar Article", results)
        self.assertNotIn("Already Selected", results)
        art, sim = results["Similar Article"]
        self.assertEqual(art.title, "Similar Article")
        self.assertTrue(sim > 0.7)

    def test_no_similar_articles(self):
        # High threshold, should return nothing
        results = render_similar_articles(
            self.selected_article, self.articles, threshold=0.9999
        )
        self.assertEqual(len(results), 0)

    def test_selected_article_excluded(self):
        # The selected article should never appear in results
        results = render_similar_articles(
            self.selected_article,
            [self.selected_article] + self.articles,
            threshold=0.5,
        )
        self.assertNotIn("Selected Article", results)


if __name__ == "__main__":
    unittest.main()
