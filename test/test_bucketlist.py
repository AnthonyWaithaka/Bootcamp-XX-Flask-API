# /test_bucketlist.py
"""Tests for user bucketlists
"""
import unittest
import json
from app.app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """Test cases for bucketlists
    """
    def setUp(self):
        """Initializing the app and defining test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name':'list1', 'date':'01012018', 'description':'Some description'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
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

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client().post('/bucketlists/',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        self.assertIn('list1', str(result.data))

    def test_api_return_all_bucketlists(self):
        """Test that the API can return all bucketlists (GET)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client().post('/bucketlists/',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/bucketlists/',
                                   headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Some description', str(result.data))

    def test_api_return_bucketlist_by_id(self):
        """Test that the API can return a bucketlist by its id (GET)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client().post('/bucketlists/',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result_in_json = json.loads(
            result.data.decode('utf-8').replace("'", "\""))
        new_result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(new_result.status_code, 200)
        self.assertIn('Some description', str(result.data))

    def test_bucketlist_editing(self):
        """Test API can edit a bucketlist (PUT)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client().post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'list2', 'date':'01012018',
                  'description':'Some other description'})
        self.assertEqual(result.status_code, 201)
        result_json = json.loads(result.data.decode())
        result = self.client().put(
            '/bucketlists/{}'.format(result_json['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name":"list3", "date":"01012018",
                "description":"Some other description"})
        self.assertEqual(result.status_code, 200)
        new_result = self.client().get(
            '/bucketlists/{}'.format(result_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('other', str(new_result.data))

    def test_bucketlist_deleting(self):
        """Test API can delete a bucketlist (DELETE)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client().post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'list1', 'date':'01012018',
                  'description':'Some new description'})
        self.assertEqual(result.status_code, 201)
        result_json = json.loads(result.data.decode())
        delete_result = self.client().delete(
            '/bucketlists/{}'.format(result_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(delete_result.status_code, 200)
        #Test for data, should return a 404
        new_result = self.client().get(
            '/bucketlists/1',
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
