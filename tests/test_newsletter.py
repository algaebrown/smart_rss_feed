import unittest
from datetime import datetime
from src.newsletter import Newsletter


class TestNewsletter(unittest.TestCase):
    def test_newsletter_fields(self):
        n = Newsletter(
            title="Weekly Update",
            content="This is the newsletter content.",
            publication_date=datetime(2025, 8, 22),
        )
        self.assertEqual(n.title, "Weekly Update")
        self.assertEqual(n.content, "This is the newsletter content.")
        self.assertEqual(n.publication_date, datetime(2025, 8, 22))

    def test_publication_date_type(self):
        n = Newsletter(
            title="Test", content="Test content", publication_date=datetime.now()
        )
        self.assertIsInstance(n.publication_date, datetime)


if __name__ == "__main__":
    unittest.main()
