# /test_bucketlist_item.py
"""Tests for bucketlist items
"""
import unittest
import json
from app.app import create_app, db

class BucketlistItemTestCase(unittest.TestCase):
    """Test cases for bucketlist items
    """
    def setUp(self):
        """Initializing the app and defining test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name':'list1', 'date':'01011999', 'description':'Some description'}
        self.bucketlist_item1 = {'name':'bucketlist_item1', 'description':'Do stuff'}
        self.bucketlist_item2 = {'name':'bucketlist_item2', 'description':'Do a little more stuff'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, name="guy2", email="guy2@yes.com", password="bbb"):
        """Register a new user for the bucketlist_item tests
        """
        user_data = {
            'name': name,
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="guy2@yes.com", password="bbb"):
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
        result = self.client().post('/bucketlists/',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        self.assertIn('list1', str(result.data))


    def test_bucketlist_item_creation(self):
        """Test API can create an bucketlist_item (POST)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result = self.client().post('/bucketlists/1/items',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist_item1)
        self.assertEqual(result.status_code, 201)
        self.assertIn('bucketlist_item1', str(result.data))

    def test_api_return_all_activities(self):
        """Test that the API can return all activities (GET)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result1 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        result2 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item2)
        self.assertEqual(result1.status_code, 201)
        self.assertEqual(result2.status_code, 201)
        result = self.client().get('/bucketlists/1/items',
                                   headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Do stuff', str(result1.data))
        self.assertIn('Do a little more stuff', str(result2.data))

    def test_bucketlist_item_editing(self):
        """Test API can edit an bucketlist_item (PUT)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result1 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        result2 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item2)
        self.assertEqual(result1.status_code, 201)
        self.assertEqual(result2.status_code, 201)
        result = self.client().put(
            '/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={'bucketlist_id':1, 'name':'bucketlist_itemnew', 'description':'New thing'})
        self.assertEqual(result.status_code, 200)
        new_result = self.client().get(
            '/bucketlists/1/items',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('New thing', str(new_result.data))

    def test_bucketlist_item_deleting(self):
        """Test API can delete an bucketlist_item (DELETE)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result1 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        result2 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        self.assertEqual(result1.status_code, 201)
        self.assertEqual(result2.status_code, 201)
        delete_result = self.client().delete(
            '/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(delete_result.status_code, 200)
        #Test for data, should return a 404
        new_result = self.client().get(
            '/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(new_result.status_code, 404)

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
