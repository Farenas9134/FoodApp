'''
Where we define tables with corresponding fields
'''

from . import db
from flask_login import UserMixin
from datetime import datetime, timezone
import sqlalchemy as sa

from sqlalchemy import UniqueConstraint
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash

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

    # Admin Flag
    is_admin = db.Column(db.Boolean, default=False, nullable = False)
    
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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Core macros
    calories = db.Column(db.Float, nullable=False, default=0.0)
    protein_g = db.Column(db.Float, default=0.0)
    carbs_g = db.Column(db.Float, default=0.0)
    fat_g = db.Column(db.Float, default=0.0)

    # Permission & Data Integrity Control
    is_verified = db.Column(db.Boolean, default=False, nullable = False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)

    # Soft deletion of ingredients but still want it to be referenced by recipes
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, server_default=sa.text('0'))

    # Detailed micronutrients
    # Figure out later, focus on macros
    # micronutrients = db.Column(db.JSON, default=dict)

    def to_dict(self, mode=1):
        """Default mode is 1 which returns minimized non-macro nutrient info, 2 returns full data"""
        data = {}
        for column in self.__table__.columns:
            if mode == 1 and column.name == 'name':
                value = getattr(self, column.name)
                data[column.name] = value
            elif mode == 2:
                value = getattr(self, column.name)
                data[column.name] = value
        return data

    @classmethod
    def get_visible_for_user(cls, user_id):
        """Returns a SQLAlchemy Select statement for visible ingredients"""
        stmt = sa.select(cls).where(cls.is_deleted == False)

        if user_id is not None:
            stmt = stmt.where(
                sa.or_(
                    cls.is_verified == True,
                    cls.created_by == user_id
                )
            )
        else:
            stmt = stmt.where(cls.is_verified == True)

        return stmt.order_by(cls.name)

class RecipeIngredient(db.Model):
    __tablename__ = "RecipeIngredient"

    # Standalone pk so we can have multiple instances of one ingredient
    recipe_ingredient_id = db.Column(db.Integer, primary_key=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'), nullable=False)

    amount = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(50), nullable=False, default='')
    notes = db.Column(db.String(200), default='')

    # Direct relationship to Ingredient Model
    ingredient: so.Mapped['Ingredient'] = so.relationship()

    def to_dict(self):
        # Grab ingredient info from linked Ingredient model
        data = self.ingredient.to_dict() if self.ingredient else {}

        # Add recipe specific details
        data['recipe_ingredient_id'] = self.recipe_ingredient_id
        data['amount'] = self.amount
        data['unit'] = self.unit
        data['notes'] = self.notes

        return data
class UserPantry(db.Model):
    __tablename__ = "UserPantry"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
class Recipe(db.Model):
    # sets name of db table in SQLite
    __tablename__ = "recipes"

    # ATTRS TO ADD FOR RECIPE EXTRACTION #
    nutrients = db.Column(db.JSON, default=list) # -> nutrients of the entire recipe
    description = db.Column(db.String(1000), default='') # -> short description of a recipe, sometimes they suck lol
    total_time = db.Column(db.Integer, default=0) # -> including prep and cooking
    # Don't know which of the previous 3 are more useful so putting all of them
    category = db.Column(db.String(100), default='') # -> tells whether a recipe is a main course, appetizer, dessert, etc.
    rating = db.Column(db.Float, default=0.0) # -> rating of recipe out of 5 stars
    servings = db.Column(db.String(100), default='') # -> how many servings the recipe makes

    # FOR SOME OF THESE IM HONESTLY NOT SURE IF nullable=True OR nullable=False MAKES THE MOST SENSE
    
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(1000), nullable=False)
    source_platform = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    image_url = db.Column(db.String(1000), nullable=False, default=list)
    # Update tags after setting new attrs
    tags = db.Column(db.JSON, default={})
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # if we create an account for each 'influencer' we can have a table for them
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    recipe_ingredients: so.WriteOnlyMapped['RecipeIngredient'] = so.relationship(
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    # Composite Unique Constraint: 
    # - user_id + title combination MUST be unique AND
    # - url MUST be unique
    __table_args__ = (
            # Checks: Is this source_url already in the database?
            UniqueConstraint('source_url', name='uq_recipes_source_url'),
            
            # Checks: Has this user already used this title?
            UniqueConstraint('submitted_by', 'title', name='uq_user_recipe_title'),
        )
        
    def to_dict(self, mode=1):
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # check if item is a datetime object (shoots errors when passed)
            if isinstance(value, datetime):
                # turns datetime into formatted string
                value = value.isoformat()
            # Simple mode for minimal recipe display instead of huge blocky text
            if mode == 2 and column.name == 'instructions':
                continue
            data[column.name] = value
        return data

    def get_ingredients_print(self):
        # Generate select query from writeonlymapped relationship
        stmt = self.recipe_ingredients.select()

        # execute and return all rows as a python list
        recipe_ingredients = db.session.scalars(stmt).all()

        return [ri.to_dict() for ri in recipe_ingredients]

    def get_ingredients(self):
                # Generate select query from writeonlymapped relationship
        stmt = self.recipe_ingredients.select()

        # execute and return all rows as a python list
        recipe_ingredients = db.session.scalars(stmt).all()

        return recipe_ingredients

class SavedRecipes(db.Model):
    __tablename__ = 'SavedRecipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), nullable=False)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))