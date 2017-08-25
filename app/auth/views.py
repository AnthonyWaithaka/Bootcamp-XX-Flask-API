# /app/auth/views.py

from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify, session
from app.models import User, Blacklist


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
                email = post_data['email']
                password = post_data['password']
                user = User(name=username, email=email, password=password)
                user.save()

                response = {
                    'message': 'User registered successfully. Please Log in.'
                }
                return make_response(jsonify(response)), 201
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

class LoginView(MethodView):
    """Handle user login and access token generation
    """
    def post(self):
        """POST request handling to generate user access token
        """
        try:
            user = User.query.filter_by(email=request.data['email']).first()
            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message':'Logged in successfully.',
                        'access_token':access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message':'Invalid email or password. Try again.'
                }
                return make_response(jsonify(response)), 401
            
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

class LogoutView(MethodView):
    """Handle user logout and revoke access token
    """
    def post(self):
        """GET request handling for current user logout
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
                    return make_response(jsonify(response)), 200
        except Exception as e:
            response = {'message':str(e)}
            return make_response(jsonify(response)), 500

class ResetPassword(MethodView):
    """Handle user request password
    """
    def post(self):
        email = request.data['email']
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = User.query.filter_by(email=email).first()
        if user and user.password_is_valid(old_password):
            result = user.reset_password(email, new_password)
            if result:
                response = {'message':'Reset password successfully'}
                return make_response(jsonify(response)), 200
            else:
                response = {'message':'Password reset failed'}
                return make_response(jsonify(response)), 404

registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_view = ResetPassword.as_view('reset_view')

# rule for registration route
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=reset_view,
    methods=['POST']
)