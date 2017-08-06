# /app/models.py
"""Application models for database population
"""
from app import db

class User(db.Model):
    """User table class
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, email, password):
        """Initialize new user account
        """
        self.username = name
        self.email = email
        self.password = password

    def save(self):
        """Store new store new user account into database
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Return all user accounts
        """
        return User.query.all()

    def delete(self):
        """Delete a user account from the database
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Object instance of the class when it is queried
        """
        return "<User: {}>".format(self.name)

class Bucketlist(db.Model):
    """Bucketlist table class
    """
    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    bucketlist_name = db.Column(db.String(255))
    deadline_date = db.Column(db.DateTime)
    bucketlist_description = db.Column(db.String(255))

    def __init__(self, name, date, description):
        """Initialize bucketlist with name, deadline date and description
        """
        self.bucketlist_name = name
        self.deadline_date = date
        self.bucketlist_description = description

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

class Activity(db.Model):
    """Activity table class
    """
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    bucketlist_id = db.Column(db.Integer)
    activity_name = db.Column(db.String(255))
    activity_description = db.Column(db.String(255))

    def __init__(self, bucketlist_id, name, description):
        """Initialize activity with bucketlist_id, name and description
        """
        self.bucketlist_id = bucketlist_id
        self.activity_name = name
        self.activity_description = description

    def save(self):
        """Store new activity into database
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Return all activity entries in database
        """
        return Activity.query.all()

    def delete(self):
        """Delete an activity from the database
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Object instance of the class when it is queried
        """
        return "<Activity: {}>".format(self.name)
