# /app/activity/__init__.py

from flask import Blueprint

bucketlist_item_blueprint = Blueprint('bucketlist_item', __name__)

from . import views
