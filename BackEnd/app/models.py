'''
Where we define tables with corresponding fields
'''

from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Overrides default get_id() function, otherwise we get NotImplementedError()
    def get_id(self):
        return (self.user_id)
