# /test/test_auth.py

import unittest
import json
from app.app import create_app, db

class AuthTestCase(unittest.TestCase):
    """Several test cases for authentication blueprint
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
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registration is successful
        """
        result = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        result_json = json.loads(result.data.decode())
        self.assertEqual(result_json['message'], "User %s %s registered successfully. Please Log in."
        %('guy', 'guy@yes.com'))

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice
        """
        result = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        new_result = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(new_result.status_code, 202)
        new_result_json = json.loads(new_result.data.decode())
        self.assertEqual(new_result_json['message'], "User account exists.")

    def test_user_login(self):
        """Test user with registered account can log in
        """
        result = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        login_result = self.client().post('/auth/login', data=self.user_data)
        login_result_json = json.loads(login_result.data.decode())
        self.assertEqual(login_result_json['message'], "Logged in successfully.")
        self.assertEqual(login_result.status_code, 200)

    def test_user_logout(self):
        """Test user can log out
        """
        result = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        login_result = self.client().post('/auth/login', data=self.user_data)
        self.assertEqual(login_result.status_code, 200)
        access_token = json.loads(login_result.data.decode())['access_token']

        logout_result = self.client().post('/auth/logout',
                                          headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(logout_result.status_code, 200)
        self.assertIn(json.loads(logout_result.data.decode())['message'], "Logged out successfully.")

    def test_non_registered_user_login(self):
        """Test user without account cannot log in
        """
        non_user = {
            'email': 'guy@no.com',
            'password': 'bbb'
        }
        result = self.client().post('/auth/login', data=non_user)
        result_json = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 401)
        self.assertEqual(
            result_json['message'], "Invalid email or password. Try again.")

    def test_user_reset_password(self):
        """Test user can reset their password
        """
        result = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        reset_result = self.client().post('/auth/reset-password', data={
            'email':'guy@yes.com',
            'old_password':'test_password',
            'new_password':'newstuff'
        })
        self.assertEqual(reset_result.status_code, 200)
        login_result = self.client().post('/auth/login', data={
            'email':'guy@yes.com',
            'password':'newstuff'
        })
        self.assertEqual(login_result.status_code, 200, msg="New password not accepted.")

    def tearDown(self):
        """Tear down initialized variables
        """
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
