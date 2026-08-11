from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, logout_user
from datetime import datetime, timezone, timedelta

from ..models import Recipe, User, SavedRecipes
from ..extensions import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
@login_required
def get_user():
    return jsonify({
        'hello':f'hello user number {current_user.user_id}'
    })

@user_bp.route('/user/recipes', methods=['GET'])
@login_required
def get_user_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('page', 1, type=int)

    # Join Recipe and SavedRecipes, filtering by the current logged-in user
    pagination = (
        Recipe.query.join(SavedRecipes, Recipe.recipe_id == SavedRecipes.recipe_id)
        .filter(SavedRecipes.user_id == current_user.user_id)
        .order_by(SavedRecipes.saved_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    recipes = [recipe.to_dict() for recipe in pagination.items]

    return jsonify({
        'saved recipes' : recipes,
        'total': pagination.total,
        'pages': pagination.pages,
        'current page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@user_bp.route('/user/recipes/<recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    saved_recipe = SavedRecipes(user_id=current_user.user_id, recipe_id=recipe_id)
    db.session.add(saved_recipe)
    db.session.commit()

    return jsonify({
        'message': 'success',
        'recipe_saved': f'{recipe.title} successfully saved to users recipes'
    }), 201

@user_bp.route('/user/recipes/<recipe_id>', methods=['DELETE'])
@login_required
def delete_recipe(recipe_id):
    saved_recipe = SavedRecipes.query.filter_by(user_id=current_user.user_id, recipe_id=recipe_id).first()

    if not saved_recipe:
        return jsonify({'error': 'Recipe not previously saved, cannot delete.'}), 404
    
    try:
        db.session.delete(saved_recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/user', methods=['DELETE'])
@login_required
def delete_user_profile():
    user_id = current_user.user_id

    try:
        # grab and delete attached saved recipes and submitted recipes
        # .delete() bulk deletion
        SavedRecipes.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        Recipe.query.filter_by(submitted_by=user_id).delete(synchronize_session=False)
        
        # delete user
        db.session.delete(current_user)
        db.session.commit()

        # Clear session / logout user
        logout_user()

        return jsonify({
            'message': 'Successfully deleted user and attached recipes!'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500