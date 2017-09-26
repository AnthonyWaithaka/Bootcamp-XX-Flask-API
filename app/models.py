# /app/models.py
"""Application models for database population
"""
from app.app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta

class User(db.Model):
    """User table class
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, name, email, password):
        """Initialize new user account
        """
        self.username = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """Check if password hash is in the records
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Store user account into database
        """
        db.session.add(self)
        db.session.commit()
    def generate_token(self, user_id):
        """Generate access token
        """
        try:
            #payload setup with expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            #create byte string token using the payload and SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256')
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def reset_password(user, new_password):
        """Reset a specific user's password
        """
        user = User.query.filter_by(email=user).first()
        if user:
            user.password = Bcrypt().generate_password_hash(new_password).decode()
            user.save()
            return True
        else:
            return False

    @staticmethod
    def decode_token(token):
        """Decode access token from Authorization header
        """
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Login again"
        except jwt.InvalidTokenError:
            return "Invalid token. Register or Login"

class Blacklist(db.Model):
    """Used tokens
    """
    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True)
    used_token = db.Column(db.String(255))

    def __init__(self, token):
        """Store token variable
        """
        self.used_token = token

    def save(self):
        db.session.add(self)
        db.session.commit()

class Bucketlist(db.Model):
    """Bucketlist table class
    """
    __tablename__ = "bucketlist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bucketlist_name = db.Column(db.String(255))
    deadline_date = db.Column(db.String(255))
    bucketlist_description = db.Column(db.String(255))
    activities = db.relationship('BucketlistItem', order_by='BucketlistItem.id', cascade="all, delete-orphan")

    def __init__(self, created_by, name, date, description):
        """Initialize bucketlist with name, deadline date and description
        """
        self.bucketlist_name = name
        self.deadline_date = date
        self.bucketlist_description = description
        self.user_id = created_by

    def save(self):
        """Store new bucketlist into database
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Return all bucketlist entries in database
        """
        return Bucketlist.query.all()

    def delete(self):
        """Delete a bucketlist from the database
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Object instance of the class when it is queried
        """
        return "<Bucketlist: {}>".format(self.name)

class BucketlistItem(db.Model):
    """BucketlistItem table class
    """
    __tablename__ = "bucketlist_item"

    id = db.Column(db.Integer, primary_key=True)
    bucketlist_item_name = db.Column(db.String(255))
    bucketlist_item_description = db.Column(db.String(255))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def __init__(self, created_by, name, description):
        """Initialize bucketlist_item with bucketlist_id, name and description
        """
        self.bucketlist_item_name = name
        self.bucketlist_item_description = description
        self.bucketlist_id = created_by

    def save(self):
        """Store new bucketlist_item into database
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Return all bucketlist_item entries in database
        """
        return BucketlistItem.query.all()

    def delete(self):
        """Delete an bucketlist_item from the database
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Object instance of the class when it is queried
        """
        return "<BucketlistItem: {}>".format(self.name)
