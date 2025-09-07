import unittest
from datetime import datetime
from src.newsletter import Newsletter
from src.formatter import format_newsletter_for_email, format_multiple_newsletters


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.newsletter = Newsletter(
            title="Test Title",
            content="This is the test content.",
            publication_date=datetime(2025, 8, 22, 10, 0),
            url="https://example.com/newsletter",
        )

    def test_format_newsletter_for_email(self):
        formatted = format_newsletter_for_email(self.newsletter)
        self.assertIn("Subject: Test Title", formatted)
        self.assertIn("Date: Friday, 22 August 2025 10:00", formatted)
        self.assertIn("URL: https://example.com/newsletter", formatted)
        self.assertIn("This is the test content.", formatted)

    def test_format_multiple_newsletters(self):
        n2 = Newsletter(
            title="Second",
            content="Second content.",
            publication_date=datetime(2025, 8, 23, 11, 0),
            url="https://example.com/second",
        )
        formatted = format_multiple_newsletters([self.newsletter, n2])
        self.assertIn("Subject: Test Title", formatted)
        self.assertIn("Subject: Second", formatted)
        self.assertIn("---", formatted)


if __name__ == "__main__":
    unittest.main()
