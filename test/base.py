# /test/base.py

import unittest
from app.app import create_app, db

class BaseTest(unittest.TestCase):
    """Set up and tear down methods for test cases
    """
    def setUp(self):
        """Initialize test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'name': 'guy',
            'email': 'guy@yes.com',
            'password': 'test_password'
        }
        self.bucketlist = {'name':'list1', 'date':'01012018', 'description':'Some description'}
        self.bucketlist_item1 = {'name':'bucketlist_item1', 'description':'Do stuff'}
        self.bucketlist_item2 = {'name':'bucketlist_item2', 'description':'Do a little more stuff'}

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, name="guy1", email="guy1@yes.com", password="aaa"):
        """Register a new user for the bucketlist tests
        """
        user_data = {
            'name': name,
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="guy1@yes.com", password="aaa"):
        """Log in with the registered account
        """
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def create_bucketlist(self, access_token):
        """Create a new bucketlist to test activities
        """
        return self.client().post('/bucketlists/',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist)

    def tearDown(self):
        """Tear down initialized variables
        """
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
