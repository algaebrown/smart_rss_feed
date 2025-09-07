import unittest
from datetime import datetime
from user import User
from newsletter import Newsletter
from subscription import Subscription


class TestSubscription(unittest.TestCase):
    def setUp(self):
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

    def test_subscription_fields(self):
        self.assertEqual(self.subscription.user.email, "user@example.com")
        self.assertEqual(self.subscription.newsletter.title, "Weekly Update")
        self.assertEqual(self.subscription.subscribed_at, datetime(2025, 8, 22))


if __name__ == "__main__":
    unittest.main()
