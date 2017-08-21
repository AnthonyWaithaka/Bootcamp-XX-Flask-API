# /app/bucketlist/__init__.py

from flask import Blueprint

bucketlist_blueprint = Blueprint('bucketlist', __name__)

from . import views
