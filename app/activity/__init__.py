# /app/activity/__init__.py

from flask import Blueprint

activity_blueprint = Blueprint('activity', __name__)

from . import views
