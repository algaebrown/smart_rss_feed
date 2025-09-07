import unittest
from unittest.mock import patch
import web_search


class TestWebSearch(unittest.TestCase):
    @patch("newspaper.Article")
    def test_fetch_article_full_text_success(self, mock_article):
        mock_instance = mock_article.return_value
        mock_instance.download.return_value = None
        mock_instance.parse.return_value = None
        mock_instance.text = "Test article text."
        result = web_search.fetch_article_full_text("http://example.com")
        self.assertEqual(result, "Test article text.")

    @patch("newspaper.Article")
    def test_fetch_article_full_text_no_text(self, mock_article):
        mock_instance = mock_article.return_value
        mock_instance.download.return_value = None
        mock_instance.parse.return_value = None
        mock_instance.text = ""
        result = web_search.fetch_article_full_text("http://example.com")
        self.assertEqual(result, "No article text found.")

    @patch("ddgs.DDGS")
    @patch("web_search.fetch_article_full_text")
    def test_duckduckgo_search_similar_news_prnewswire(self, mock_fetch, mock_ddgs):
        # Simulate PR Newswire result
        mock_ddgs.return_value.__enter__.return_value.text.return_value = [
            {
                "title": "PR News",
                "href": "https://www.prnewswire.com/news",
                "body": "snippet",
            }
        ]
        mock_fetch.return_value = "PR Newswire full text"
        result = web_search.duckduckgo_search_similar_news("query")
        self.assertEqual(result, "PR Newswire full text")

    @patch("ddgs.DDGS")
    @patch("web_search.fetch_article_full_text")
    def test_duckduckgo_search_similar_news_scrape_others(self, mock_fetch, mock_ddgs):
        # Simulate no PR Newswire, scrape 2 articles
        mock_ddgs.return_value.__enter__.return_value.text.return_value = [
            {"title": "Other1", "href": "https://other1.com", "body": "snippet1"},
            {"title": "Other2", "href": "https://other2.com", "body": "snippet2"},
        ]
        mock_fetch.side_effect = ["Full text 1", "Full text 2"]
        result = web_search.duckduckgo_search_similar_news("query", max_results=2)
        self.assertIn("Full text 1", result)
        self.assertIn("Full text 2", result)

    @patch("web_search.fetch_article_full_text")
    def test_find_full_text_success(self, mock_fetch):
        mock_fetch.return_value = "Some article text."
        result = web_search.find_full_text("http://example.com", "title")
        self.assertEqual(result, "Some article text.")

    @patch("web_search.fetch_article_full_text")
    @patch("web_search.duckduckgo_search_similar_news")
    def test_find_full_text_fallback(self, mock_duck, mock_fetch):
        mock_fetch.side_effect = Exception("forbidden")
        mock_duck.return_value = "DuckDuckGo fallback text"
        result = web_search.find_full_text("http://example.com", "title")
        self.assertEqual(result, "DuckDuckGo fallback text")


if __name__ == "__main__":
    unittest.main()
