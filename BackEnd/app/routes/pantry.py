from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from ..models import Ingredient, Recipe, UserPantry
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