# /app/app.py
"""App module functions and imports
"""

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

#local imports
from instance.config import app_config

#initializing sql-alchemy
db = SQLAlchemy()
user_id = None

def create_app(config_name):
    """Create new Flask object and
    connect to database
    """
    from app.models import User, Bucketlist, BucketlistItem
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .auth.views import auth_blueprint
    from .bucketlist.views import bucketlist_blueprint
    from .bucketlist_item.views import bucketlist_item_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(bucketlist_blueprint)
    app.register_blueprint(bucketlist_item_blueprint)
    return app
