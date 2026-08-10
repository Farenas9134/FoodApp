'''
Where we define tables with corresponding fields
'''

from . import db
from flask_login import UserMixin
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Overrides default get_id() function, otherwise we get NotImplementedError()
    def get_id(self):
        return (self.user_id)

# What should this schema look like?
class Recipe(db.Model):
    # sets name of db table in SQLite
    __tablename__ = "recipes"
    
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(1000), nullable=False)
    source_platform = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False, default=list)
    instructions = db.Column(db.JSON, nullable=False)
    image_url = db.Column(db.String(1000), nullable=False, default=list)
    tags = db.Column(db.String(100))
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # if we create an account for each 'influencer' we can have a table for them
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

        
    def to_dict(self):
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # check if item is a datetime object (shoots errors when passed)
            if isinstance(value, datetime):
                # turns datetime into formatted string
                value = value.isoformat()
            data[column.name] = value
        return data

