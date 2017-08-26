# /app/bucketlist/views.py

"""Views methods for managing bucketlist endpoints
"""

from flask import Blueprint

bucketlist_blueprint = Blueprint('bucketlist', __name__)

from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from app.models import Bucketlist, User, Blacklist
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
                # user has been authenticated
                return request_method(*args, **kwargs)
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 400
        else:
            return make_response(jsonify({'message':'Unauthorized attempt.'})), 401
    return wrapper

class BucketListsView(MethodView):
    """Request handling for the bucketlists
    that belong to the user currently logged in
    """
    @authentication_required
    def get(self):
        """GET request handling for /bucketlists/
        Return all the user's bucketlists
        """
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

        if results == []:
            return make_response({'message':'No bucketlists to view'}), 204

        response = jsonify(results)
        response.status_code = 200
        return response

    @authentication_required
    def post(self):
        """POST request handling for /bucketlists/
        Create a new bucketlist for the user
        """
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

class BucketListsManipulationView(MethodView):
    """Request handling for manipulating the bucketlists
    that belong to the user
    """
    @authentication_required
    def delete(self, list_id):
        bucketlist = Bucketlist.query.filter_by(id=list_id).first()
        if not bucketlist:
            abort(404)
        else:
            bucketlist.delete()
            return {
                "message":"bucketlist {} deleted successfully".format(bucketlist.id)}, 200

    @authentication_required
    def put(self, list_id):
        """PUT request handling for /bucketlists/<int:list_id>
        Update a bucketlist's details
        """
        bucketlist = Bucketlist.query.filter_by(id=list_id).first()
        if not bucketlist:
            abort(404)
        else:
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

    @authentication_required
    def get(self, list_id):
        """GET request handling for /bucketlists/<int:list_id>
        Return the user's bucketlist data
        """
        bucketlist = Bucketlist.query.filter_by(id=list_id).first()
        if not bucketlist:
            abort(404)
        else:
            response = jsonify({
                'id': bucketlist.id,
                'user_id': bucketlist.user_id,
                'name': bucketlist.bucketlist_name,
                'date': bucketlist.deadline_date,
                'description': bucketlist.bucketlist_description
            })
            response.status_code = 200
            return response

bucketlists_view = BucketListsView.as_view('bucketlists_view')
bucketlistsmanip_view = BucketListsManipulationView.as_view('bucketlistsmanip_view')

# rules for the bucketlist routes
bucketlist_blueprint.add_url_rule(
    '/bucketlists/',
    view_func=bucketlists_view,
    methods=['GET', 'POST'])

bucketlist_blueprint.add_url_rule(
    '/bucketlists/<int:list_id>',
    view_func=bucketlistsmanip_view,
    methods=['DELETE', 'PUT','GET'])
