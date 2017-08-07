# /app/__init__.py
"""App module functions and imports
"""

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

#local imports
from instance.config import app_config

#initializing sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    """Create new Flask object and
    connect to database
    """
    from app.models import User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/auth/register', methods=['POST', 'GET'])
    def register():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            email = str(request.data.get('email', ''))
            password = str(request.data.get('password', ''))
            if name:
                user = User(name, email, password)
                user.save()
                response = jsonify({
                    'id':user.id,
                    'name':user.username,
                    'email':user.email,
                    'password':user.password
                })
                response.status_code = 201
                return response
        else:
            users = User.get_all()
            results = []

            for user in users:
                obj = {
                    'id':user.id,
                    'name':user.username,
                    'email':user.email,
                    'password':user.password
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    return app
