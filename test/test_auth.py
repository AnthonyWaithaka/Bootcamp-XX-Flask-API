# /test/test_auth.py

import json
from base import *

class AuthTestCase(BaseTest):
    """Several test cases for authentication blueprint
    """
    def test_registration(self):
        """Test user registration is successful
        """
        result = self.register_user()
        result_json = json.loads(result.data.decode())
        self.assertEqual(result_json['message'], "User %s %s registered successfully. Please Log in."
        %('guy1', 'guy1@yes.com'))

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice
        """
        result = self.register_user()
        new_result = self.register_user()
        new_result_json = json.loads(new_result.data.decode())
        self.assertEqual(new_result_json['message'], "User account exists.")

    def test_user_login(self):
        """Test user with registered account can log in
        """
        result = self.register_user()
        login_result = self.login_user()
        login_result_json = json.loads(login_result.data.decode())
        self.assertEqual(login_result_json['message'], "Logged in successfully.")

    def test_user_logout(self):
        """Test user can log out
        """
        result = self.register_user()
        login_result = self.login_user()
        access_token = json.loads(login_result.data.decode())['access_token']

        logout_result = self.client().post('/auth/logout',
                                          headers=dict(Authorization="Bearer " + access_token))
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
        self.assertEqual(
            result_json['message'], "Invalid email or password. Try again.")

    def test_user_reset_password(self):
        """Test user can reset their password
        """
        result = self.register_user()
        reset_result = self.client().post('/auth/reset-password', data={
            'email':'guy1@yes.com',
            'old_password':'aaa',
            'new_password':'newstuff'
        })
        login_result = self.client().post('/auth/login', data={
            'email':'guy1@yes.com',
            'password':'newstuff'
        })
        self.assertEqual(login_result.status_code, 200)
