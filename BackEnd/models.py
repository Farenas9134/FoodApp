'''
Where we define tables with corresponding fields
'''

from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)