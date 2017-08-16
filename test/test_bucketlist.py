# /test_bucketlist.py
"""Tests for user bucketlists
"""
import unittest
import json
from app import create_app, db

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
            db.create_all()

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST)
        """
        result = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201, msg="Page not returned")
        self.assertIn('list1', str(result.data), msg="Bucketlist not created")

    def test_api_return_all_bucketlists(self):
        """Test that the API can return all bucketlists (GET)
        """
        result = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/bucketlists/')
        self.assertEqual(result.status_code, 200, msg="Page not returned")
        self.assertIn('Some description', str(result.data), msg="Bucketlist not returned")

    def test_api_return_bucketlist_by_id(self):
        """Test that the API can return a bucketlist by its id (GET)
        """
        result = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result_in_json = json.loads(
            result.data.decode('utf-8').replace("'", "\""))
        new_result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(new_result.status_code, 200, msg="Page not returned")
        self.assertIn('Some description', str(result.data), msg="Bucketlist not returned")

    def test_bucketlist_editing(self):
        """Test API can edit a bucketlist (PUT)
        """
        result = self.client().post(
            '/bucketlists/',
            data={'name':'list2', 'date':'01012018',
                  'description':'Some other description'})
        self.assertEqual(result.status_code, 201)
        result = self.client().put(
            '/bucketlists/1',
            data={
                "name":"list3", "date":"01012018",
                "description":"Some other description"})
        self.assertEqual(result.status_code, 200, msg="Page not returned")
        new_result = self.client().get('/bucketlists/1')
        self.assertIn('other', str(new_result.data), msg="Bucketlist not updated")

    def test_bucketlist_deleting(self):
        """Test API can delete a bucketlist (DELETE)
        """
        result = self.client().post(
            '/bucketlists/',
            data = {'name':'list1', 'date':'01012018',
                    'description':'Some new description'})
        self.assertEqual(result.status_code, 201)
        delete_result = self.client().delete('/bucketlists/1')
        self.assertEqual(delete_result.status_code, 200)
        #Test for data, should return a 404
        new_result = self.client().get('/bucketlists/1')
        self.assertEqual(new_result.status_code, 404, msg="Bucketlist not deleted")

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
