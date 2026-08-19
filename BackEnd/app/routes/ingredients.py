from flask import Blueprint, jsonify, request
from flask_login import login_required

from ..models import Ingredient, RecipeIngredient, Recipe

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