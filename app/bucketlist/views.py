# /app/bucketlist/views.py

"""Views methods for managing bucketlist endpoints
"""

from flask import Blueprint

bucketlist_blueprint = Blueprint('bucketlist', __name__)

from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from app.models import Bucketlist, User, Blacklist
from app.app import user_id
from app.crossdomain import crossdomain

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
        if request.args.get('limit'):
            limit_param = int(request.args.get('limit'))
        else:
            limit_param = 10
        
        if request.args.get('page'):
            page_param = int(request.args.get('page'))
        else:
            page_param = 0

        if request.args.get('q'):
            search_param = request.args.get('q')
            for bucketlist in bucketlists:
                if search_param.lower() in bucketlist.bucketlist_name.lower():
                    obj = {
                        'user':bucketlist.user_id,
                        'id':bucketlist.id,
                        'name':bucketlist.bucketlist_name,
                        'date':bucketlist.deadline_date,
                        'description':bucketlist.bucketlist_description
                    }
                    results.append(obj)
        else:
            #Otherwise return all
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
            return make_response({'message':'No bucketlists found.'}), 404

        results = results[::-1]
        records_length = len(results)
        split_results = results[(page_param*limit_param):((page_param*limit_param)+limit_param)]
        total_result = {'bucketlists': split_results, 'records_length': records_length}

        if split_results == []:
            return make_response({'message':'Page does not exist.'}), 404

        response = jsonify(total_result)
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Credentials'] = True
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
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
            response.headers['Access-Control-Allow-Origin'] = "*"
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.status_code = 201
            return response
    
    def options(self):
        """OPTIONS request handling for Cross Origin Resource Sharing default
        """
        response = {
            'message': 'CORS Authorization'
        }
        return crossdomain(response, 'options'), 200

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
            response = jsonify({
                "message":"bucketlist {} deleted successfully".format(bucketlist.id)})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = "*"
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'DELETE'
            return response
            # return {
            #     "message":"bucketlist {} deleted successfully".format(bucketlist.id)}, 200

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
            response.headers['Access-Control-Allow-Origin'] = "*"
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'PUT'
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
            response.headers['Access-Control-Allow-Origin'] = "*"
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
            return response
    
    def options(self, list_id):
        """OPTIONS request handling for Cross Origin Resource Sharing default
        """
        response = {
            'message': 'CORS Authorization'
        }
        return crossdomain(response, 'options'), 200

bucketlists_view = BucketListsView.as_view('bucketlists_view')
bucketlistsmanip_view = BucketListsManipulationView.as_view('bucketlistsmanip_view')

# rules for the bucketlist routes
bucketlist_blueprint.add_url_rule(
    '/bucketlists/',
    view_func=bucketlists_view,
    methods=['GET', 'POST', 'OPTIONS'])

bucketlist_blueprint.add_url_rule(
    '/bucketlists/<int:list_id>',
    view_func=bucketlistsmanip_view,
    methods=['DELETE', 'PUT', 'GET', 'OPTIONS'])
