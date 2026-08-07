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
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(1000))
    source_platform = db.Column(db.String(100))
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(1000))
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

