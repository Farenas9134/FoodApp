from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import select, delete, func

from ..models import Ingredient, Recipe, UserPantry, RecipeIngredient
from ..extensions import db

user_pantry_bp = Blueprint('user-pantry', __name__)

@user_pantry_bp.route("/pantry", methods=['GET'])
@login_required
def get_user_pantry():
    """Grabs a user's stored pantry ingredients"""
    user_id = current_user.user_id
    try:
        # Build stmt to load in pantry ingredients
        stmt = select(UserPantry).where(
            UserPantry.user_id == user_id
        ).options(
            # performs LEFT OUTER JOIN with ingredient table
            joinedload(UserPantry.ingredient)
        )

        # Execute optimized query with joinedload
        pantry_items = db.session.scalars(stmt).all()

        return jsonify({
            'pantry': [item.to_dict() for item in pantry_items]
        }), 201
    except Exception as e:
        return jsonify({'error':str(e)}), 500

@user_pantry_bp.route('/pantry', methods=['POST'])
@login_required
def add_to_user_pantry():
    """Adds a set of ingredient ids into the User's pantry"""
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error':'Request body must be valid JSON'}), 400

    # grab ing id's from data
    ing_list = data.get('ingredients')
    if not ing_list:
        return jsonify({'message':'No ingredients provided'}), 200

    try:
        # Fetch all requested ingredients that exist and are visible to user
        stmt = Ingredient.get_visible_for_user(current_user.user_id).where(Ingredient.id.in_(ing_list))
        valid_ingredients = db.session.scalars(stmt).all()

        # Extract just valid IDs into a python set
        valid_ing_ids = {ing.id for ing in valid_ingredients}

        if not valid_ing_ids:
            return jsonify({'error':'None of the provided ingredients are valid'}), 400

        # Grab all exisiting ingredients in pantry
        stmt = select(UserPantry.ingredient_id).where(
            UserPantry.user_id == current_user.user_id,
            UserPantry.ingredient_id.in_(valid_ing_ids)
        )
        exisiting_pantry_ids = set(db.session.scalars(stmt).all())

        # Extract only ids to add into pantry
        ids_to_add = valid_ing_ids - exisiting_pantry_ids

        if not ids_to_add:
            return jsonify({'message': 'All ingredients are already in your pantry'}), 200

        new_pantry_items = [
            UserPantry(user_id=current_user.user_id, ingredient_id=ing_id)
            for ing_id in ids_to_add
        ]

        # Add them all to DB
        db.session.add_all(new_pantry_items)
        db.session.commit()

        return jsonify({
            'message': f'Successfully added {len(ids_to_add)} ingredients into User Pantry'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error':'Could not update User Pantry',
            'details':str(e)
        }), 400

def close_this():
    """Standard initial approach, runs X queries. New one does 2 queries to DB"""
    # @user_pantry_bp.route('/pantry', methods=['POST'])
    # @login_required
    # def add_to_user_pantry():
    #     """Adds a set of ingredient ids into the User's pantry"""
    #     data = request.get_json()
    #     if not isinstance(data, dict):
    #         return jsonify({'error':'Request body must be valid JSON'}), 400

    #     # grab ing id's from data
    #     ing_list = data.get('ingredients')
    #     if not ing_list:
    #         return jsonify({'message':'No ingredients provided'}), 200

    #     try:
    #         for ing_id in ing_list:
    #             # Check to see if ing exists
    #             stmt = Ingredient.get_visible_for_user(current_user.user_id).where(Ingredient.id==ing_id)
    #             ingredient = db.session.scalars(stmt).first()

    #             # If ingredient DNE skip
    #             if not ingredient: continue

    #             # Check if ing not already in pantry
    #             stmt = select(UserPantry).where(
    #                 UserPantry.user_id == current_user.user_id,
    #                 UserPantry.ingredient_id == ing_id
    #             )
    #             pantry_ingredient = db.session.scalars(stmt).first()
    #             if pantry_ingredient: continue

    #             # Ingredient exists and is not in pantry, create record and commit
    #             pantry_ingredient = UserPantry(user_id = current_user.user_id, ingredient_id=ing_id)
    #             db.session.add(pantry_ingredient)
    #             db.session.flush()
    #         # Once all ingredient ids gone through, commit
    #         db.session.commit()

    #         return jsonify({
    #             'message':'Successfully added ingredients into User Pantry'
    #         }), 201
        
    #     except Exception as e:
    #         db.session.rollback()
    #         return jsonify({
    #             'error':'Could not update User Pantry',
    #             'details':str(e)
    #         }), 400

@user_pantry_bp.route('/pantry', methods=['DELETE'])
@login_required
def remove_from_user_pantry():
    """Removes a set of ingredient ids from User's pantry"""
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error':'Request body must be valid JSON'}), 400

    # grab ing id's from data
    ing_list = data.get('ingredients')
    if not ing_list:
        return jsonify({'message':'No ingredients provided'}), 200

    try:
        # Grab all existing ingredients in pantry
        stmt = select(UserPantry.ingredient_id).where(
            UserPantry.user_id == current_user.user_id
        )
        current_pantry_ids = set(db.session.scalars(stmt).all())

        # Extract only ids to remove from pantry
        # Intersection of both sets to avoid doing validation of given ids
        ids_to_remove = current_pantry_ids & set(ing_list)

        if not ids_to_remove:
            return jsonify({'message':'Given ingredients do not exist in your pantry'}), 200

        # Remove ingredients
        stmt = delete(UserPantry).where(
            UserPantry.user_id == current_user.user_id,
            UserPantry.ingredient_id.in_(ids_to_remove))
        db.session.execute(stmt)
        db.session.commit()

        return jsonify({
            'message':'Successfully removed given ingredients from pantry!'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error':'Could not update User Pantry',
            'details':str(e)
        }), 400

@user_pantry_bp.route('/pantry-match', methods=['GET'])
@login_required
def get_pantry_matched_recipes():
    """Finds and ranks recipes based on a user's pantry contents"""
    # Check query args first, then check any JSON body if given, then default to 0.8 if all else fails
    json_data = request.get_json(silent=True) or {}
    raw_percentage = request.args.get('min_match_percentage') or json_data.get('min_match_percentage', 0.8)

    # If wrong input, just default to 0.8
    try:
        min_match_percentage = float(raw_percentage)
    except (ValueError, TypeError):
        min_match_percentage = 0.8

    user_id = current_user.user_id

    # Statement/Query to grab all ids in user's pantry
    pantry_subquery = (
        select(UserPantry.ingredient_id).where(
            UserPantry.user_id == user_id
        ).scalar_subquery()
    )

    # BIGGGGG ONE SINGLE QUERY/Statement
    stmt = (
        # Select Recipes, label their total required ingredients, and total matched ingredients
        select(
            Recipe,
            # Create column for each recipe where we store count of ingredient ids they have
            func.count(RecipeIngredient.ingredient_id).label('total_required'),
            # Create column for each recipe, where we store count of matching ingredient_ids in user pantry ids
            func.count(
                # If not matching recipeIngredient, make Null and don't increment count
                func.nullif(RecipeIngredient.ingredient_id.in_(pantry_subquery), False)
            ).label("total_matched")
        )
        # Join Recipe table to RecipeIngredient table by recipe_ids
        .join(RecipeIngredient, Recipe.recipe_id == RecipeIngredient.recipe_id)
        # Group joined rows by recipe_id
        .group_by(Recipe.recipe_id)

        # func.count()s below run inside each bucket

        # Filter out recipe buckets that don't meet minimum match percentage
        .having(
            # ingredient_id.in_(pantry_subquery) -> T/F. Is this given recipeIngredient in the User pantry?
            # func.nullif(..., False) -> If ingredient not in pantry, then turn Fale into NULL
            # func.count() ignores NULL values, incrementing only for True counts
            (func.count(func.nullif(RecipeIngredient.ingredient_id.in_(pantry_subquery), False)) 
             * 1.0 /
             func.count(RecipeIngredient.ingredient_id))
             # Only keep Recipes who meet the match ratio requirements
             >= min_match_percentage
        )

        # Order buckets by highest match percentage first, then by total ingredients required
        .order_by(
            # Match ratio
            (func.count(func.nullif(RecipeIngredient.ingredient_id.in_(pantry_subquery), False)) * 1.0 /
             func.count(RecipeIngredient.ingredient_id)).desc(),
             # RecipeIngredient count
             func.count(RecipeIngredient.ingredient_id).desc()
        )
    )

    results = db.session.execute(stmt).all()

    # Format results to add in match info
    formatted_results = []
    for recipe, total_req, total_match in results:
        recipe_data = recipe.to_dict(mode=2)
        recipe_data['match_info'] = {
            'total_required':total_req,
            'total_matched':total_match,
            'missing_count':total_req-total_match,
            'match_percentage': round((total_match/total_req) * 100, 1)
        }
        formatted_results.append(recipe_data)

    return jsonify({
        'recipes_matched': formatted_results
    }), 200