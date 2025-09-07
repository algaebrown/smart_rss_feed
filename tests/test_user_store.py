import unittest
from src.user import User
from src.user_store import UserStore


class TestUserStore(unittest.TestCase):
    def setUp(self):
        self.store = UserStore()
        self.user = User(
            email="test@example.com",
            password_hash="hashedpassword123",
            profile_info="Researcher in AI",
        )

    def test_create_and_read(self):
        self.store.create(self.user)
        u = self.store.read("test@example.com")
        self.assertIsNotNone(u)
        self.assertEqual(u.email, "test@example.com")

    def test_update(self):
        self.store.create(self.user)
        updated = User(
            email="test@example.com",
            password_hash="newhash456",
            profile_info="Updated profile",
        )
        result = self.store.update("test@example.com", updated)
        self.assertTrue(result)
        u = self.store.read("test@example.com")
        self.assertEqual(u.password_hash, "newhash456")
        self.assertEqual(u.profile_info, "Updated profile")

    def test_delete(self):
        self.store.create(self.user)
        result = self.store.delete("test@example.com")
        self.assertTrue(result)
        u = self.store.read("test@example.com")
        self.assertIsNone(u)

    def test_list_all(self):
        self.store.create(self.user)
        users = self.store.list_all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, "test@example.com")


if __name__ == "__main__":
    unittest.main()
