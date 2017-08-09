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
    from app.models import User, Bucketlist, Activity
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/auth/register', methods=['POST', 'GET'])
    def register():
        """Register a new user account
        """
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

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        """Create a new bucketlist entry
        """
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            date = str(request.data.get('date', ''))
            description = str(request.data.get('description', ''))
            if name:
                bucketlist = Bucketlist(name, date, description)
                bucketlist.save()
                response = jsonify({
                    'id':bucketlist.id,
                    'name':bucketlist.bucketlist_name,
                    'date':bucketlist.deadline_date,
                    'description':bucketlist.bucketlist_description
                })
                response.status_code = 201
                return response
        else:
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id':bucketlist.id,
                    'name':bucketlist.bucketlist_name,
                    'date':bucketlist.deadline_date,
                    'description':bucketlist.bucketlist_description
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_return(id, **kwargs):
        """Return a bucketlist by id
        """
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                "message":"bucketlist {} deleted successfully".format(bucketlist.id)}, 200
        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            date = str(request.data.get('date', ''))
            description = str(request.data.get('description', ''))
            bucketlist.bucketlist_name = name
            bucketlist.deadline_date = date
            bucketlist.bucketlist_description = description
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.bucketlist_name,
                'date': bucketlist.deadline_date,
                'description': bucketlist.bucketlist_description
            })
            response.status_code = 200
            return response
        else:
            #GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.bucketlist_name,
                'date': bucketlist.deadline_date,
                'description': bucketlist.bucketlist_description
            })
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:bucketlist_id>/items', methods=['POST', 'GET'])
    def activities(bucketlist_id, **kwargs):
        """Create a new activity
        """
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))
            if name:
                activity = Activity(bucketlist_id, name, description)
                activity.save()
                response = jsonify({
                    'id':activity.id,
                    'bucketlist_id':activity.bucketlist_id,
                    'name':activity.activity_name,
                    'description':activity.activity_description
                })
                response.status_code = 201
                return response
        else:
            #Return all activities
            activities = Activity.get_all()
            results = []

            for activity in activities:
                if activity.bucketlist_id == bucketlist_id:
                    obj = {
                        'id':activity.id,
                        'bucketlist_id':activity.bucketlist_id,
                        'name':activity.activity_name,
                        'description':activity.activity_description
                    }
                    results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:bucketlist_id>/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def activity_manipulate(bucketlist_id, id, **kwargs):
        """Return an activity by id for PUT and DELETE operations
        """
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            abort(404)

        if request.method == 'DELETE':
            activity.delete()
            return {
                "message":"activity {} deleted successfully".format(activity.id)}, 200
        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))
            activity.activity_name = name
            activity.activity_description = description
            activity.save()
            response = jsonify({
                'id': activity.id,
                'bucketlist_id': activity.bucketlist_id,
                'name': activity.activity_name,
                'description': activity.activity_description
            })
            response.status_code = 200
            return response
        else:
            #GET
            response = jsonify({
                'id': activity.id,
                'bucketlist_id': activity.bucketlist_id,
                'name': activity.activity_name,
                'description': activity.activity_description
            })
            response.status_code = 200
            return response

    return app
