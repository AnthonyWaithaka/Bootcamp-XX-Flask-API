# /app/auth/views.py

import re
from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User, Blacklist
from app.crossdomain import crossdomain

class RegistrationView(MethodView):
    """Register a new user account
    """
    def post(self):
        """POST request handling for /auth/register
        """
        user = User.query.filter_by(username=request.data['name']).first()
        if not user:
            try:
                post_data = request.data
                username = post_data['name']
                email = post_data['email'].lower()
                password = post_data['password']
                # ^ to match at the beginning of the line,
                # class with a-z for lowercase alphabet, 0-9 for numerals, underscore and hyphen.
                # grouping () to match a period, followed by the same characters as before the period.
                # * match one or more repetitions of the above.
                # match the character @.
                # match characters a-z, 0-9 and hyphen
                # match a group of characters: period '.', followed by a-z, 0-9 and hyphen.
                # * match one or more repetitions of the above group.
                # match a group of characters: period '.', followed by a-z.
                # restrict match of the above group of characters from minimum two to maximum four.
                # $ match the above group at the end of the line (e.g .com). Any more characters are invalid.
                match = re.match(
                    '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    email)

                if match is None:
                    return make_response(jsonify({'message':'Invalid email address.'})), 400

                user = User(name=username, email=email, password=password)
                user.save()

                response = {
                    'message': 'User %s %s registered successfully. Please Log in.' %(username, email)
                }
                return crossdomain(response, 'post'), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User account exists.'
            }
            return make_response(jsonify(response)), 202

    def options(self):
        """OPTIONS request handling for Cross Origin Resource Sharing default
        """
        response = {
            'message': 'CORS Authorization'
        }
        return crossdomain(response, 'options'), 200

class LoginView(MethodView):
    """Handle user login and access token generation
    """
    def post(self):
        """POST request handling to generate user access token
        """
        try:
            user = User.query.filter_by(email=request.data['email'].lower()).first()
            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message':'Logged in successfully.',
                        'access_token':access_token.decode()
                    }
                    return crossdomain(response, 'post'), 200
            else:
                response = {
                    'message':'Invalid email or password. Try again.'
                }
                return crossdomain(response), 401            
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def options(self):
        """OPTIONS request handling for Cross Origin Resource Sharing default
        """
        response = {
            'message': 'CORS Authorization'
        }
        return crossdomain(response, 'options'), 200

class LogoutView(MethodView):
    """Handle user logout and revoke access token
    """
    def post(self):
        """POST request handling for current user logout
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        try:
            if access_token:
                blacklisted = Blacklist.query.filter_by(used_token=access_token).first()
                if not blacklisted:
                    new_blacklist = Blacklist(access_token)
                    new_blacklist.save()
                    response = {
                        'message':'Logged out successfully.'
                    }
                    return crossdomain(response, 'post'), 200
                else:
                    response = {'message':'Token not valid. Please log in again.'}
                    return make_response(jsonify(response)), 401
        except Exception as e:
            response = {'message':str(e)}
            return make_response(jsonify(response)), 500
    
    def options(self):
        """OPTIONS request handling for Cross Origin Resource Sharing default
        """
        response = {
            'message': 'CORS Authorization'
        }
        return crossdomain(response, 'options'), 200

class ResetPassword(MethodView):
    """Handle user request password
    """
    def post(self):
        email = request.data['email'].lower()
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = User.query.filter_by(email=email).first()
        if user and user.password_is_valid(old_password):
            result = user.reset_password(email, new_password)
            if result:
                response = {'message':'Reset password successfully'}
                return crossdomain(response, 'post'), 200
            else:
                response = {'message':'Password reset failed'}
                return make_response(jsonify(response)), 501
    
    def options(self):
        """OPTIONS request handling for Cross Origin Resource Sharing default
        """
        response = {
            'message': 'CORS Authorization'
        }
        return crossdomain(response, 'options'), 200

registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_view = ResetPassword.as_view('reset_view')

# rule for registration route
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'OPTIONS'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST', 'OPTIONS'])

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST', 'OPTIONS']
)

auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=reset_view,
    methods=['POST', 'OPTIONS']
)