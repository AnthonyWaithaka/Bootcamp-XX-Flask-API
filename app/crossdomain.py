# app/crossdomain.py
"""
Allow Cross Origin Resource Sharing for secure browsers
"""

from flask import make_response, jsonify

def crossdomain(request_response, request_method='get'):
    response = make_response(jsonify(request_response))
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Credentials'] = True
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    if request_method == 'get':    
        response.headers['Access-Control-Allow-Methods'] = 'GET'
    elif request_method == 'post':
        response.headers['Access-Control-Allow-Methods'] = 'POST'
    elif request_method == 'put':
        response.headers['Access-Control-Allow-Methods'] = 'PUT'
    elif request_method == 'delete':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE'
    elif request_method == 'options':
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST, PUT, DELETE'

    return response