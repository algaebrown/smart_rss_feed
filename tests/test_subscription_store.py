import unittest
from datetime import datetime
from user import User
from newsletter import Newsletter
from subscription import Subscription
from subscription_store import SubscriptionStore


class TestSubscriptionStore(unittest.TestCase):
    def setUp(self):
        self.store = SubscriptionStore()
        self.user = User(
            email="user@example.com", password_hash="hash", profile_info="Profile"
        )
        self.newsletter = Newsletter(
            title="Weekly Update",
            content="Content",
            publication_date=datetime(2025, 8, 22),
        )
        self.subscription = Subscription(
            user=self.user,
            newsletter=self.newsletter,
            subscribed_at=datetime(2025, 8, 22),
        )

    def test_create_and_read(self):
        self.store.create(self.subscription)
        s = self.store.read("user@example.com", "Weekly Update")
        self.assertIsNotNone(s)
        self.assertEqual(s.user.email, "user@example.com")
        self.assertEqual(s.newsletter.title, "Weekly Update")

    def test_update(self):
        self.store.create(self.subscription)
        updated = Subscription(
            user=self.user,
            newsletter=self.newsletter,
            subscribed_at=datetime(2025, 8, 23),
        )
        result = self.store.update("user@example.com", "Weekly Update", updated)
        self.assertTrue(result)
        s = self.store.read("user@example.com", "Weekly Update")
        self.assertEqual(s.subscribed_at, datetime(2025, 8, 23))

    def test_delete(self):
        self.store.create(self.subscription)
        result = self.store.delete("user@example.com", "Weekly Update")
        self.assertTrue(result)
        s = self.store.read("user@example.com", "Weekly Update")
        self.assertIsNone(s)

    def test_list_all(self):
        self.store.create(self.subscription)
        subs = self.store.list_all()
        self.assertEqual(len(subs), 1)
        self.assertEqual(subs[0].user.email, "user@example.com")
        self.assertEqual(subs[0].newsletter.title, "Weekly Update")


if __name__ == "__main__":
    unittest.main()
