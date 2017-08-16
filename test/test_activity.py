# /test_activity.py
"""Tests for bucketlist items
"""
import unittest
import json
from app import create_app, db

class ActivityTestCase(unittest.TestCase):
    """Test cases for bucketlist items
    """
    def setUp(self):
        """Initializing the app and defining test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name':'list1', 'date':'01012018', 'description':'Some description'}
        self.activity = {'name':'activity1', 'description':'Do stuff'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_activity_creation(self):
        """Test API can create an activity (POST)
        """
        rb = self.client().post('/bucketlists/', data=self.bucketlist)
        result = self.client().post('/bucketlists/1/items', data=self.activity)
        self.assertEqual(result.status_code, 201)
        self.assertIn('activity1', str(result.data))

    def test_api_return_all_activities(self):
        """Test that the API can return all activities (GET)
        """
        rb = self.client().post('/bucketlists/', data=self.bucketlist)
        result = self.client().post('/bucketlists/1/items', data=self.activity)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/bucketlists/1/items')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Do stuff', str(result.data))

    def test_activity_editing(self):
        """Test API can edit an activity (PUT)
        """
        rb = self.client().post('/bucketlists/', data=self.bucketlist)
        result = self.client().post('/bucketlists/1/items', data=self.activity)
        self.assertEqual(result.status_code, 201)
        result = self.client().put(
            '/bucketlists/1/items/1',
            data={'bucketlist_id':1, 'name':'activity2', 'description':'New thing'})
        self.assertEqual(result.status_code, 200)
        new_result = self.client().get('/bucketlists/1/items')
        self.assertIn('New thing', str(new_result.data))

    def test_activity_deleting(self):
        """Test API can delete an activity (DELETE)
        """
        rb = self.client().post('/bucketlists/', data=self.bucketlist)
        result = self.client().post('/bucketlists/1/items', data=self.activity)
        self.assertEqual(result.status_code, 201)
        delete_result = self.client().delete('/bucketlists/1/items/1')
        self.assertEqual(delete_result.status_code, 200)
        #Test for data, should return a 404
        new_result = self.client().get('/bucketlists/1/items/1')
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
