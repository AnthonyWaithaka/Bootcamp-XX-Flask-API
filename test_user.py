# /test_user.py
"""Tests for user accounts
"""
import unittest
from app import create_app, db

class UserTestCase(unittest.TestCase):
    """Test cases for users
    """
    def setUp(self):
        """Initializing the app and defining test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'name':'user1', 'email':'guy@yes.com', 'password':'aaa'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test API can create a user account (POST)
        """
        result = self.client().post('/auth/register', data=self.user)
        self.assertEqual(result.status_code, 201, msg="Page not returned")
        self.assertIn('user1', str(result.data), msg="User not created")

    def tearDown(self):
        """Tear down initialized variables
        """
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# make the tests executable
if __name__ == "__main__":
    unittest.main()
