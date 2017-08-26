# /app/bucketlist_item/views.py

"""Views methods for managing bucketlist item endpoints
"""

from flask import Blueprint

bucketlist_item_blueprint = Blueprint('bucketlist_item', __name__)

from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from app.models import Bucketlist, User, BucketlistItem, Blacklist
from app.app import user_id

def authentication_required(request_method):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            blacklisted = Blacklist.query.filter_by(used_token=access_token).first()
            if blacklisted:
                response = {'message':'Please log in to access bucketlists.'}
                return make_response(jsonify(response)), 401
            global user_id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=kwargs['list_id']).first()
                if bucketlist.user_id != user_id:
                    return make_response(jsonify({'message':'Unauthorized access to this bucketlist.'}))
                # user has been authenticated
                return request_method(*args, **kwargs)
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 400
        else:
            return make_response(jsonify({'message':'Unauthorized attempt.'})), 401
    return wrapper

class ActivitiesView(MethodView):
    """Request handling for bucketlist items
    """
    @authentication_required
    def get(self, list_id):
        """GET request handling for /bucketlists/<int:list_id>/items
        Return all the bucketlist's items
        """
        activities = BucketlistItem.query.filter_by(bucketlist_id=list_id)
        results = []

        for bucketlist_item in activities:
            obj = {
                'id':bucketlist_item.id,
                'bucketlist_id':bucketlist_item.bucketlist_id,
                'name':bucketlist_item.bucketlist_item_name,
                'description':bucketlist_item.bucketlist_item_description
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @authentication_required
    def post(self, list_id):
        """POST request handling for /bucketlists/<int:list_id>/items
        Create a new bucketlist item
        """
        name = str(request.data.get('name', ''))
        description = str(request.data.get('description', ''))
        if name:
            bucketlist_item = BucketlistItem(list_id, name, description)
            bucketlist_item.save()
            response = jsonify({
                'id':bucketlist_item.id,
                'bucketlist_id':bucketlist_item.bucketlist_id,
                'name':bucketlist_item.bucketlist_item_name,
                'description':bucketlist_item.bucketlist_item_description
            })
            response.status_code = 201
            return response

class ActivitiesManipulationView(MethodView):
    """Request handling for manipulating bucketlist items
    """
    @authentication_required
    def delete(self, list_id, item_id):
        """_DELETE request handling for /bucketlists/<int:list_id>/items/<int:item_id>
        Delete the bucketlist item
        """
        bucketlist_item = BucketlistItem.query.filter_by(id=item_id).first()
        if not bucketlist_item:
            abort(404)
        else:
            bucketlist_item.delete()
            return {
                "message":"bucketlist_item {} deleted successfully".format(bucketlist_item.id)}, 200

    @authentication_required
    def put(self, list_id, item_id):
        """PUT request handling for /bucketlists/<int:list_id>/items/<int:item_id>
        Update a bucketlist item's details
        """
        bucketlist_item = BucketlistItem.query.filter_by(id=item_id).first()
        if not bucketlist_item:
            abort(404)
        else:
            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))
            bucketlist_item.bucketlist_item_name = name
            bucketlist_item.bucketlist_item_description = description
            bucketlist_item.save()
            response = jsonify({
                'id': bucketlist_item.id,
                'bucketlist_id': bucketlist_item.bucketlist_id,
                'name': bucketlist_item.bucketlist_item_name,
                'description': bucketlist_item.bucketlist_item_description
            })
            response.status_code = 200
            return response

    @authentication_required
    def get(self, list_id, item_id):
        """GET request handling for /bucketlists/<int:list_id>/items/<int:item_id>
        Return the bucketlist item's data
        """
        bucketlist_item = BucketlistItem.query.filter_by(id=item_id).first()
        if not bucketlist_item:
            abort(404)
        else:
            response = jsonify({
                'id': bucketlist_item.id,
                'bucketlist_id': bucketlist_item.bucketlist_id,
                'name': bucketlist_item.bucketlist_item_name,
                'description': bucketlist_item.bucketlist_item_description
            })
            response.status_code = 200
            return response

activities_view = ActivitiesView.as_view('activities_view')
activitiesmanip_view = ActivitiesManipulationView.as_view('activitiesmanip_view')

# rules for the bucketlist routes
bucketlist_item_blueprint.add_url_rule(
    '/bucketlists/<int:list_id>/items',
    view_func=activities_view,
    methods=['GET', 'POST'])

bucketlist_item_blueprint.add_url_rule(
    '/bucketlists/<int:list_id>/items/<int:item_id>',
    view_func=activitiesmanip_view,
    methods=['DELETE', 'PUT', 'GET'])
