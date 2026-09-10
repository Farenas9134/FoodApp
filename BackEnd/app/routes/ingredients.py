from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from flask_login import login_required, current_user

from ..models import Ingredient, RecipeIngredient, Recipe
from ..extensions import db

ingredient_bp = Blueprint('ingredients', __name__)

@ingredient_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    per_page = min(per_page, 100)

    pagination = Ingredient.query.order_by(Ingredient.name).paginate(
        page = page,
        per_page=per_page,
        error_out=False
    )

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
    ingredient = Ingredient.query.get_or_404(ingredient_id)

    return jsonify({'ingredient': ingredient.to_dict()}), 200

@ingredient_bp.route('/ingredients/<ingredient_id>', methods=['PUT'])
@login_required
def edit_ingredient(ingredient_id):
    user_id = current_user.user_id
    data = request.get_json()
    if not data:
        return jsonify({'error':'No data provided'}), 400
    
    ingredient = Ingredient.query.get_or_404(ingredient_id)

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
                if field in ('name'):
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
@login_required
def search_ingredients():
    query_str = request.args.get('q', '').strip()

    # Restrict search results to public staples or user's own created ingredients
    stmt = select(Ingredient).where(
        Ingredient.name.ilike(f"%{query_str}%"),
        or_(
            Ingredient.is_verified == True,
            Ingredient.created_by == current_user.user_id
        )
    )
    results = db.session.scalars(stmt).all()
    return jsonify([i.to_dict() for i in results]), 200