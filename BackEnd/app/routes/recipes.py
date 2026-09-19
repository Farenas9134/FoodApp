from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from ..models import Recipe, Ingredient, RecipeIngredient
from ..extensions import db
from ingredient_parser import parse_ingredient

recipes_db = Blueprint('recipes', __name__)

def safe_parse_amounts(raw_quantity):
    'Converts quantity to float. Returns amount, extra_notes'
    if not raw_quantity:
        return 1.0, ''
    try:
        return float(raw_quantity), ""
    except (ValueError, TypeError):
        # Parse_ingredient() likely returned non-numeric string as the amount
        return 1.0, str(raw_quantity)

@recipes_db.route('/recipes-submit', methods=["POST"])
@login_required
def submit_recipe():
     data = request.get_json()

     if not isinstance(data, dict): 
          return jsonify({"error": "Request body must be valid JSON"}), 400

     required_fields = set(Recipe.__table__.columns.keys()) - {
          'recipe_id',
          'created_at',
          'last_updated',
          'submitted_by'
     } | {'recipe_ingredients'}

     missing = []
     for field in required_fields:
          if field not in data:
               missing.append(field)

     if missing:
          return jsonify({"error": "Missing required fields", "Missing": missing}), 400

     user_id = current_user.user_id if current_user.is_authenticated else 1

     # Attempt to add recipe to DB
     try:
          # Insantiate recipe instance
          new_recipe = Recipe(submitted_by=user_id)
          ingredients_parsed = []

          for field,value in data.items():
               # Only work with valid fields
               if field not in required_fields: continue
               # Check each ingredient to see if Ingredient record needs to be made
               if field == 'recipe_ingredients':
                    # For each ingredient in the list of ingredients
                    for item in value:
                         ingredient_info = parse_ingredient(item)
                         ingredients_parsed.append(ingredient_info)

               # Not a field that requires special handling, just add to Recipe (title, source_url, etc.)
               else:
                    setattr(new_recipe, field, value)

          # If no ingredients parsed, recipe cannot be created
          if len(ingredients_parsed) == 0:
               raise ValueError("Recipe must have at least one ingredient.")

          db.session.add(new_recipe)
          db.session.flush()

          # Local ingredient cache to prevent Ingredient duplicates due to temp. flushes
          local_ingredient_cache = {}

          # If successful, then run through each ingredient
          for ing in ingredients_parsed:
               # Ingredient parser did not assign a name
               if not ing.name: continue
               # Grab ing info based on parse_ingredient output format
               ing_name = ing.name[0].text.lower()
               ing_raw_qty = ing.amount[0].quantity if len(ing.amount) == 1 else 0
               ing_amount, ing_notes = safe_parse_amounts(ing_raw_qty)
               ing_unit = str(ing.amount[0].unit) if len(ing.amount) == 1 else ''
               ing_base_comment = ing.comment.text if ing.comment else ''
               # Merge comments and any notes if any
               ing_comment = f"{ing_notes} {ing_base_comment}".strip()

               # Check local cache first
               new_ing = local_ingredient_cache.get(ing_name)

               # Then check if existing ingredient record exists first
               if not new_ing:
                    new_ing = Ingredient.query.filter_by(name=ing_name).first()

               # If completely new ingredient, create new record
               # other details are left to default for now
               if not new_ing:
                    new_ing = Ingredient(name=ing_name, created_by=user_id)
                    db.session.add(new_ing)
                    # Adds instance in limbo state, not a full commit. Flush needed to assign an id
                    db.session.flush()

               local_ingredient_cache[ing_name] = new_ing

               # Add RecipeIngredient record to link ing to recipe
               recipe_ingredient = RecipeIngredient(
                    recipe_id = new_recipe.recipe_id,
                    ingredient_id = new_ing.id,
                    amount = ing_amount,
                    unit = ing_unit,
                    notes = ing_comment
               )
               db.session.add(recipe_ingredient)

          # If all runs smooth, full commit it all
          db.session.commit()

     except Exception as e:
          db.session.rollback()
          return jsonify({
               "error":"Failed to create recipe. Duplicate entry or invalid data.",
               "details":str(e)
          }), 400

     # Everything went well, return success message
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
         'recipes': [recipe.to_dict(2) for recipe in pagination.items],
         'total': pagination.total,
         'pages': pagination.pages,
         'current_page': page,
         'has_next': pagination.has_next,
         'has_prev': pagination.has_prev
    }), 200

@recipes_db.route('/recipes/<recipe_id>', methods=["GET"])
def get_recipe_by_id(recipe_id):
    # get_or_404 automatically returns 404 error if recipe not found
    recipe = Recipe.query.get_or_404(recipe_id, "error: Recipe does not exist!")
              
    return jsonify({
         'recipe': recipe.to_dict(),
         'ingredients': recipe.get_ingredients()
    }), 200

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
             'recipes': [recipe.to_dict(2) for recipe in pagination.items],
             'total': pagination.total,
             'pages': pagination.pages,
             'current_page': page,
             'has_next': pagination.has_next,
             'has_prec': pagination.has_prev
    
        }), 200


@recipes_db.route('/recipes/<int:recipe_id>', methods=['PUT'])
@login_required
def update_recipe(recipe_id):
     user_id = current_user.id if current_user.is_authenticated else 1
     data = request.get_json()

     if not data:
          return jsonify({'error':'No data provided'}), 400

     recipe = Recipe.query.get_or_404(recipe_id, "error: recipe does not exist!")
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
     recipe = Recipe.query.get_or_404(recipe_id, "error: recipe does not exist!")
     user_id = current_user.user_id if current_user.is_authenticated else 67

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
         'recipes': [recipe.to_dict(2) for recipe in pagination.items],
         'total': pagination.total,
         'pages': pagination.pages,
         'current_page': page,
         'has_next': pagination.has_next,
         'has_prec': pagination.has_prev

    }), 200