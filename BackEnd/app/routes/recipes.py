from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
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
        "ingredients", "instructions", "image_url", "created_by"
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

    new_recipe = Recipe(
        title = data["title"], 
        source_url = data["source_url"], 
        source_platform = data["source_platform"],
        ingredients = data["ingredients"],
        instructions = data["instructions"],
        image_url = data["image_url"],
        submitted_by = user_id,
        created_by = data["created_by"]
    )

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
    query = request.args.get('q', '')

    if not query:
         return jsonify({'recipes':[]}), 200

    # Use LIKE for partial matching
    # The % wildcards match any characters before and after the search term
    search_term = f'%{query}%'

    recipes = Recipe.query.filter(
         db.or_(
              Recipe.title.ilike(search_term), # Case-insensitive match
         )
    ).limit(20).all()

    return jsonify({'recipes':[recipe.to_dict() for recipe in recipes]}), 200


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

     mutable_recipe_fields = [
             "title", "source_url", "source_platform",
             "ingredients", "instructions", "image_url", "created_by"
         ]
     
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

          return jsonify({'message': 'Recipe deleted successfullt'}), 200
     except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
