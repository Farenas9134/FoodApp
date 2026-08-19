from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from ..models import Recipe
from ..extensions import db

recipes_db = Blueprint('recipes', __name__)

@recipes_db.route('/recipes-submit', methods=["POST"])
# @login_required
def submit_recipe():
    data = request.get_json()
    if not data: 
        return jsonify({"error": "Missing JSON body"}), 400

    required_fields = [
        "title", "source_url", "source_platform",
        "recipe_ingredients", "instructions", "image_url", "created_by"
    ]

    missing = []
    for field in required_fields:
        if field not in data:
            missing.append(field)

    if missing:
        return jsonify({"error": "Missing required fields", "missing": missing}), 401

    # Apparently modern 2.0 way to check for duplicate data
    stmt = select(Recipe).filter_by(title=data["title"], source_url=data["source_url"])
    existing_recipe = db.session.scalars(stmt).first()

    if existing_recipe:
            return jsonify({"error": "Recipe already exists in our database!"}), 400

    # For testing purposes, aka when @login_required commented out
    user_id = current_user.id if current_user.is_authenticated else 67

    # Grab all attrs in Recipe relation, removing auto generated field submission
    valid_fields = set(Recipe.__table__.columns.keys()) - {'recipe_id', 'created_at', 'last_updated'}

    new_recipe = Recipe(submitted_by=user_id)

    for field,value in data.items():
         if field in valid_fields:
              setattr(new_recipe, field, value)

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({
        "message":"Recipe created successfully",
        "recipe": new_recipe.to_dict()
    }), 201

@recipes_db.route('/recipes', methods=["GET"])
def get_recipes():
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # limit per_page to prevent excessive data retrieval
    per_page = min(per_page, 100)

    pagination = Recipe.query.order_by(Recipe.created_at.desc()).paginate(
        page = page,
        per_page = per_page,
        error_out=False
        )

    return jsonify({
         'recipe': [recipe.to_dict() for recipe in pagination.items],
         'total': pagination.total,
         'pages': pagination.pages,
         'current_page': page,
         'has_next': pagination.has_next,
         'has_prev': pagination.has_prev
    }), 200

@recipes_db.route('/recipes/<recipe_id>', methods=["GET"])
def get_recipe_by_id(recipe_id):
    # get_or_404 automatically returns 404 error if recipe not found
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict()), 200

@recipes_db.route('/recipes/search', methods=['GET'])
def search_recipes():
    '''
        Lowkey inefficent but should work rn as db is small.
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = request.args.to_dict(flat=False)

    if not query:
         return jsonify({'recipes':[]}), 200

    # Only search by: title, source platform, ingredients, 
    #                 tags, submitted by?, created by
    valid_fields = set(Recipe.__table__.columns.keys()) - {'recipe_id', 'created_at', 'last_updated', 'instructions', 'image_url', 'created_at', 'last_updated'}

    conditions = []

    for field, value in query.items():
         if field in valid_fields:
              # returns the entire column for that field
              # Recipe.title -> entire column of titles
              column = getattr(Recipe, field)
              for val in value:
                   if val.strip():
                        # With that column, search for items
                        conditions.append(column.ilike(f'%{val.strip()}%'))
                # and_ -> merges all passed args into a single SQL WHERE clause joined by AND
                # * -> unpacks items in list into seperate arguments
    
    pagination = Recipe.query.filter(db.and_(*conditions)).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
             'recipes': [recipe.to_dict() for recipe in pagination.items],
             'total': pagination.total,
             'pages': pagination.pages,
             'current_page': page,
             'has_next': pagination.has_next,
             'has_prec': pagination.has_prev
    
        }), 200


@recipes_db.route('/recipes/<int:recipe_id>', methods=['PUT'])
# @login_required
def update_recipe(recipe_id):
     user_id = current_user.id if current_user.is_authenticated else 67
     data = request.get_json()

     if not data:
          return jsonify({'error':'No data provided'}), 400

     recipe = Recipe.query.get_or_404(recipe_id)
     if recipe.submitted_by != user_id:
          return jsonify({'error': 'User did not create recipe.'}), 403

     mutable_recipe_fields = set(Recipe.__table__.columns.keys()) - {'recipe_id', 'created_at', 'last_updated'}
     
     try:
        for field, value in data.items():
            if field in mutable_recipe_fields:
                # Check for duplicates on prev. unique fields in Recipe class
                if field in ('title', 'source_url'):
                        stmt = select(Recipe).where(
                             getattr(Recipe, field) == value,
                             Recipe.recipe_id != recipe_id
                        )
                        existing = db.session.scalars(stmt).first()
                        if existing:
                            return jsonify({'error':f'{field.replace("_"," ").title()} already taken'}), 400
                # Set field attribute to recipe
                setattr(recipe, field, value)
        setattr(recipe, 'last_updated', datetime.now(timezone.utc))

        db.session.commit()
        return jsonify({'Success': 'Successfully changed the recipe!', 'recipe': recipe.to_dict()}), 200
     
     except Exception as e:
          db.session.rollback()
          return jsonify({'error':str(e)}), 500

@recipes_db.route('/recipes/<int:recipe_id>', methods=['DELETE'])
# @login_required
def delete_recipe(recipe_id):
     recipe = Recipe.query.get_or_404(recipe_id)
     user_id = current_user.id if current_user.is_authenticated else 67

     if user_id != recipe.submitted_by:
          return jsonify({'error': 'User did not submit this recipe. Cannot delete it.'}), 401

     try:
          db.session.delete(recipe)
          db.session.commit()

          return jsonify({'message': 'Recipe deleted successfully'}), 200
     except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recipes_db.route('/recipes/recent', methods=["GET"])
def get_recent_recipes():
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Recipes posted from the last 7 days
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)

    pagination = Recipe.query.filter(
         Recipe.created_at >= cutoff_date,
    ).order_by(Recipe.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
         'recipes': [recipe.to_dict() for recipe in pagination.items],
         'total': pagination.total,
         'pages': pagination.pages,
         'current_page': page,
         'has_next': pagination.has_next,
         'has_prec': pagination.has_prev

    }), 200