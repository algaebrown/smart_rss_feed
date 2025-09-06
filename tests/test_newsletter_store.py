import unittest
from datetime import datetime
from src.newsletter import Newsletter
from src.newsletter_store import NewsletterStore

class TestNewsletterStore(unittest.TestCase):
    def setUp(self):
        self.store = NewsletterStore()
        self.newsletter = Newsletter(
            title='Weekly Update',
            content='This is the newsletter content.',
            publication_date=datetime(2025, 8, 22)
        )

    def test_create_and_read(self):
        self.store.create(self.newsletter)
        n = self.store.read('Weekly Update')
        self.assertIsNotNone(n)
        self.assertEqual(n.title, 'Weekly Update')

    def test_update(self):
        self.store.create(self.newsletter)
        updated = Newsletter(
            title='Weekly Update',
            content='Updated content.',
            publication_date=datetime(2025, 8, 22)
        )
        result = self.store.update('Weekly Update', updated)
        self.assertTrue(result)
        n = self.store.read('Weekly Update')
        self.assertEqual(n.content, 'Updated content.')

    def test_delete(self):
        self.store.create(self.newsletter)
        result = self.store.delete('Weekly Update')
        self.assertTrue(result)
        n = self.store.read('Weekly Update')
        self.assertIsNone(n)

    def test_list_all(self):
        self.store.create(self.newsletter)
        newsletters = self.store.list_all()
        self.assertEqual(len(newsletters), 1)
        self.assertEqual(newsletters[0].title, 'Weekly Update')

if __name__ == '__main__':
    unittest.main()
