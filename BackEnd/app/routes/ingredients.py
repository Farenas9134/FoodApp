from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from flask_login import login_required, current_user

from ..models import Ingredient, RecipeIngredient, Recipe
from ..extensions import db

ingredient_bp = Blueprint('ingredients', __name__)

@ingredient_bp.route("/ingredients", methods=["POST"])
@login_required
def create_ingredient():
    # Grab data from request/url
    data = request.get_json()
    # Edge Case check - No inpute
    if not data: return jsonify({"error":"Missing JSON body"}), 400

    # Establish non-negotioable fields needed to create ingredient
    required_fields = set(Ingredient.__table__.columns.keys()) - {'id', 'is_verified', 'is_deleted', 'created_by'}
    missing = []
    # If any required field missing, return error message with missing fields included
    for field in required_fields:
        if field not in data:
            missing.append(field)
    if missing: return jsonify({"error": "Missing required fields", "missing":missing}), 400

    # Check if ingredient already exists
    # Name works for now, but need to differentiate btw Generic/Name Brand/Homemade/etc.
    stmt = select(Ingredient).filter_by(name=data["name"])
    existing_recipe = db.session.scalars(stmt).first()

    if existing_recipe: return jsonify({"error": "Ingredient already exists in our database!"}), 400

    user_id = current_user.user_id
    new_ingredient = Ingredient(created_by=user_id)

    # Fill in necessary data for Ingredient creation
    for field,value in data.items():
        # Check to see if field is proper
        if field in required_fields:
            setattr(new_ingredient, field, value)

    # Add and Commit ingredient to database
    db.session.add(new_ingredient)
    db.session.commit()

    # Return success message
    return jsonify({
        "message":"Ingredient created successfully",
        "ingredient": new_ingredient.to_dict()
    }), 201

@ingredient_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    per_page = min(per_page, 100)

    # Determine if user is logged in
    user_id = current_user.user_id if current_user.is_authenticated else None

    # Build select statement using built-in function
    stmt = Ingredient.get_visible_for_user(user_id)

    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)

    return jsonify({
        'ingredients': [ingredient.to_dict() for ingredient in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@ingredient_bp.route('/ingredients/<ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    user_id = current_user.user_id if current_user.is_authenticated else None

    # Restrict lookup to visible ingredients only (staples, customs, & non soft-deleted ones)
    stmt = Ingredient.get_visible_for_user(user_id).where(Ingredient.id == ingredient_id)
    ingredient = db.session.scalars(stmt).first()

    if not ingredient:
        return jsonify({"error":"Ingredient not found!"}), 404
    
    return jsonify({'ingredient': ingredient.to_dict()}), 200

@ingredient_bp.route('/ingredients/<ingredient_id>', methods=['PUT'])
@login_required
def edit_ingredient(ingredient_id):
    user_id = current_user.user_id
    data = request.get_json()
    if not data:
        return jsonify({'error':'No data provided'}), 400
    
    ingredient = Ingredient.query.get_or_404(ingredient_id, "error: Ingredient ID does not exist!")

    # Check if ingredient is a staple/essential ingredient
    if ingredient.is_verified:
        return jsonify({"error": "Only admin can edit this ingredient"}), 400

    # Check if ingredient submitted by user
    if user_id != ingredient.created_by:
        return jsonify({'error': 'Only user who submitted this ingredient can change it.'}), 400

    mutable_i_field = set(Ingredient.__table__.columns.keys()) - {'id', 'is_verified', 'created_by'}

    try:
        for field, value in data.items():
            if field in mutable_i_field:
                if field == 'name':
                    stmt = select(Ingredient).where(
                        getattr(Ingredient, field) == value,
                        Ingredient.id != ingredient_id
                    )
                    existing = db.session.scalars(stmt).first()
                    if existing:
                        return jsonify({'error': f"{field.replace('_', '').title()} already taken"}), 400
                setattr(ingredient, field, value)

        db.session.commit()
        return jsonify({'message': "Sucessfully changed this ingredient", 'ingredient':ingredient.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ingredient_bp.route('/ingredients/search', methods=['GET'])
def search_ingredients():
    # Grab pagination details (specific page you want, how many records per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)

    # Grab search query
    query_str = request.args.get('q', '').strip()

    # Check if user is logged in
    user_id = current_user.user_id if current_user.is_authenticated else None

    # Grab default Select Statement
    stmt = Ingredient.get_visible_for_user(user_id)

    # Add query search into statement
    if query_str:
        stmt = stmt.where(Ingredient.name.ilike(f"%{query_str}%"))

    # Paginate search results with prev. defined constraints
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)

    return jsonify({
            'ingredients': [ingredient.to_dict() for ingredient in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }), 200

@ingredient_bp.route('/ingredients/<ingredient_id>', methods=["DELETE"])
@login_required
def delete_ingredient(ingredient_id):
    # Grab ingredient record
    ingredient = Ingredient.query.get_or_404(ingredient_id, "error: Ingredient does not exist!")

    # If user did not create Ingredient throw error
    if current_user.user_id != ingredient.created_by: 
        return jsonify({"message":"User did not create this ingredient!"}), 403
    # If ingredient is a staple cannot delete
    if ingredient.is_verified: 
        return jsonify({"message":"Ingredient can only be deleted by an admin user!"}), 403

    # Check if ingredient is used in ANY recipe or pantry
    is_used_in_recipes = db.session.query(
        db.session.query(RecipeIngredient).filter_by(ingredient_id=ingredient.id).exists()
        ).scalar()

    if is_used_in_recipes:
        # Soft delete so past recipes won't break and reference Nulls
        ingredient.is_deleted = True
    else:
        # Delete safely
        db.session.delete(ingredient)

    db.session.commit()
    return jsonify({"message": "Ingredient deleted successfully!"}), 200