# /test_bucketlist.py
"""Tests for user bucketlists
"""
import json
from base import *

class BucketlistTestCase(BaseTest):
    """Test cases for bucketlists
    """
    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client().post('/bucketlists/',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist)
        self.assertIn('list1', str(result.data))

    def test_api_return_all_bucketlists(self):
        """Test that the API can return all bucketlists (GET)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.create_bucketlist(access_token)
        result = self.client().get('/bucketlists/',
                                   headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Some description', str(result.data))

    def test_api_return_bucketlist_by_id(self):
        """Test that the API can return a bucketlist by its id (GET)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.create_bucketlist(access_token)
        result_in_json = json.loads(
            result.data.decode('utf-8').replace("'", "\""))
        new_result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Some description', str(result.data))

    def test_bucketlist_editing(self):
        """Test API can edit a bucketlist (PUT)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.create_bucketlist(access_token)
        result_json = json.loads(result.data.decode())
        result = self.client().put(
            '/bucketlists/{}'.format(result_json['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name":"list3", "date":"01012018",
                "description":"Some other description"})
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
        result = self.create_bucketlist(access_token)
        result_json = json.loads(result.data.decode())
        delete_result = self.client().delete(
            '/bucketlists/{}'.format(result_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        #Test for data, should return a 404
        new_result = self.client().get(
            '/bucketlists/{}'.format(result_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(new_result.status_code, 404)

    def test_bucketlist_search(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.create_bucketlist(access_token)
        search_result = self.client().get('/bucketlists/?q=l',
                                           headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('list1', str(search_result.data))

# make the tests executable
if __name__ == "__main__":
    unittest.main()
