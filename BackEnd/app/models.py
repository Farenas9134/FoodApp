'''
Where we define tables with corresponding fields
'''

from . import db
from flask_login import UserMixin
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so

class Relationships(db.Model):
    __tablename__ = 'Relationships'

    followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable = False, primary_key=True)
    followed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    # There's a bunch to the following system I am confused by
    # Source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Relevant for password reset
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime(timezone=True), nullable = True)

    # rows where I am the follower, get me the followed user
    # WiteOnlyMapped prevents loading every row into a Python list,
    # user.following needs to explicitly be ran to load in followers
    following: so.WriteOnlyMapped['User'] = so.relationship(
        # which association table to route to
        secondary=Relationships.__table__, 

        # PrimaryJoin = how do I match this user to a row in followers
        # SecondaryJoin = Given that row, how do I find the other user
        # Match rows where follower_id == me (Primary), then fetch users where user_id == followed_id (Secondary)
        primaryjoin=(Relationships.follower_id == user_id),
        secondaryjoin=(Relationships.followed_id == user_id),
        # links the two, modifying one updates the other
        back_populates='followers',
        passive_deletes=True)

    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=Relationships.__table__, 
        primaryjoin=(Relationships.followed_id == user_id),
        secondaryjoin=(Relationships.follower_id == user_id),
        back_populates=('following'),
        passive_deletes=True)
    
    # Overrides default get_id() function, otherwise we get NotImplementedError()
    def get_id(self):
        return (self.user_id)

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.user_id == user.user_id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Core macros
    calories = db.Column(db.Float, nullable=False, default=0.0)
    protein_g = db.Column(db.Float, default=0.0)
    carbs_g = db.Column(db.Float, default=0.0)
    fat_g = db.Column(db.Float, default=0.0)

    # Detailed micronutrients
    # Figure out later, focus on macros
    # micronutrients = db.Column(db.JSON, default=dict)

    def to_dict(self):
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            data[column.name] = value
        return data

class RecipeIngredient(db.Model):
    __tablename__ = "RecipeIngredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'), primary_key=True)

    amount = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(50), nullable=False, default='')
    notes = db.Column(db.String(200), default='')

    # Direct relationship to Ingredient Model
    ingredient: so.Mapped['Ingredient'] = so.relationship()


class UserPantry(db.Model):
    __tablename__ = "UserPantry"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
class Recipe(db.Model):
    # sets name of db table in SQLite
    __tablename__ = "recipes"
    
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(1000), nullable=False)
    source_platform = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    image_url = db.Column(db.String(1000), nullable=False, default=list)
    tags = db.Column(db.String(100))
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # if we create an account for each 'influencer' we can have a table for them
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    recipe_ingredients: so.WriteOnlyMapped['RecipeIngredient'] = so.relationship(
        cascade='all, delete-orphan',
        passive_deletes=True
    )

        
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

class SavedRecipes(db.Model):
    __tablename__ = 'SavedRecipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))