# /app/activity/views.py

"""Views methods for managing bucketlist item endpoints
"""

from . import activity_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from app.models import Bucketlist, User, Activity

class ActivitiesView(MethodView):
    """Request handling for bucketlist items
    """
    def get(self, list_id):
        """GET request handling for /bucketlists/<int:list_id>/items
        Return all the bucketlist's items
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
                activities = Activity.query.filter_by(bucketlist_id=list_id)
                results = []

                for activity in activities:
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

    def post(self, list_id):
        """POST request handling for /bucketlists/<int:list_id>/items
        Create a new bucketlist item
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
                name = str(request.data.get('name', ''))
                description = str(request.data.get('description', ''))
                if name:
                    activity = Activity(list_id, name, description)
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
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class ActivitiesManipulationView(MethodView):
    """Request handling for manipulating bucketlist items
    """
    def delete(self, list_id, item_id):
        """DELETE request handling for /bucketlists/<int:list_id>/items/<int:item_id>
        Delete the bucketlist item
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
                activity = Activity.query.filter_by(id=item_id).first()
                if not activity:
                    abort(404)
                else:
                    activity.delete()
                    return {
                        "message":"activity {} deleted successfully".format(activity.id)}, 200
            else:
                message = user_id
                response = {'message':message}
                return make_response(jsonify(response)), 401

    def put(self, list_id, item_id):
        """PUT request handling for /bucketlists/<int:list_id>/items/<int:item_id>
        Update a bucketlist item's details
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
                activity = Activity.query.filter_by(id=item_id).first()
                if not activity:
                    abort(404)
                else:
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
                message = user_id
                response = {'message':message}
                return make_response(jsonify(response)), 401

    def get(self, list_id, item_id):
        """GET request handling for /bucketlists/<int:list_id>/items/<int:item_id>
        Return the bucketlist item's data
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user has been authenticated
                activity = Activity.query.filter_by(id=item_id).first()
                if not activity:
                    abort(404)
                else:
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
                response = {'message':message}
                return make_response(jsonify(response)), 401

activities_view = ActivitiesView.as_view('activities_view')
activitiesmanip_view = ActivitiesManipulationView.as_view('activitiesmanip_view')

# rules for the bucketlist routes
activity_blueprint.add_url_rule(
    '/bucketlists/<int:list_id>/items',
    view_func=activities_view,
    methods=['GET', 'POST'])

activity_blueprint.add_url_rule(
    '/bucketlists/<int:list_id>/items/<int:item_id>',
    view_func=activitiesmanip_view,
    methods=['DELETE', 'PUT', 'GET'])
