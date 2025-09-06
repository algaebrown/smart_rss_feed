import unittest
from src.user import User

class TestUser(unittest.TestCase):
    def test_user_fields(self):
        u = User(
            email='test@example.com',
            password_hash='hashedpassword123',
            profile_info='Researcher in AI'
        )
        self.assertEqual(u.email, 'test@example.com')
        self.assertEqual(u.password_hash, 'hashedpassword123')
        self.assertEqual(u.profile_info, 'Researcher in AI')

    def test_profile_info_optional(self):
        u = User(
            email='test2@example.com',
            password_hash='hash456'
        )
        self.assertIsNone(u.profile_info)

if __name__ == '__main__':
    unittest.main()
