# /app/models.py
"""Application models for database population
"""
from app import db

class Bucketlist(db.Model):
    """Bucketlist table class
    """
    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    def __init__(self, name):
        """Initialize bucketlist with name
        """
        self.name = name

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
