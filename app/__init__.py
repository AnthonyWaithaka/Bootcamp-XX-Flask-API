# /app/__init__.py
"""App module functions and imports
"""

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

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

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        """Create a new bucketlist entry
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    date = str(request.data.get('date', ''))
                    description = str(request.data.get('description', ''))
                    if name:
                        bucketlist = Bucketlist(user_id, name, date, description)
                        bucketlist.save()
                        response = jsonify({
                            'user':bucketlist.user_id,
                            'id':bucketlist.id,
                            'name':bucketlist.bucketlist_name,
                            'date':bucketlist.deadline_date,
                            'description':bucketlist.bucketlist_description
                        })
                        response.status_code = 201
                        return response
                else:
                    bucketlists = Bucketlist.query.filter_by(user_id=user_id)
                    results = []

                    for bucketlist in bucketlists:
                        obj = {
                            'user':bucketlist.user_id,
                            'id':bucketlist.id,
                            'name':bucketlist.bucketlist_name,
                            'date':bucketlist.deadline_date,
                            'description':bucketlist.bucketlist_description
                        }
                        results.append(obj)
                    response = jsonify(results)
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_return(id, **kwargs):
        """Return and manipulate a bucketlist by id
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
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
                        'description': bucketlist.bucketlist_description,
                        'user_id': bucketlist.user_id
                    })
                    response.status_code = 200
                    return response
                else:
                    #GET
                    response = jsonify({
                        'id': bucketlist.id,
                        'user_id': bucketlist.user_id,
                        'name': bucketlist.bucketlist_name,
                        'date': bucketlist.deadline_date,
                        'description': bucketlist.bucketlist_description
                    })
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {'message':message}
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:bucketlist_id>/items', methods=['POST', 'GET'])
    def activities(bucketlist_id, **kwargs):
        """Create a new activity
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
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
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:bucketlist_id>/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def activity_manipulate(bucketlist_id, id, **kwargs):
        """Return an activity by id for PUT and DELETE operations
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
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
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
