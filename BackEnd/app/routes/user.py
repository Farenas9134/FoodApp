from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, logout_user
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa

from ..models import Recipe, User, SavedRecipes, Relationships
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
    per_page = request.args.get('page', 10, type=int)

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

@user_bp.route('/user/follow/<user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    user = db.session.scalar(sa.select(User).where(User.user_id == user_id))
    if user is None:
        return jsonify({'error': f'User id {user_id} not found.'}), 401

    if user == current_user:
        return jsonify({'error': 'You cannot follow yourself!'}), 401

    current_user.follow(user)
    db.session.commit()

    return jsonify({'message': f'You have successfully followed {user.name}'}), 201

@user_bp.route('/user/unfollow/<user_id>', methods=['DELETE'])
@login_required
def unfollow_user(user_id):
    user = db.session.scalar(sa.select(User).where(User.user_id == user_id))
    if user is None:
        return jsonify({'error': f'User id {user_id} not found.'}), 401

    if user == current_user:
        return jsonify({'error': 'You cannot unfollow yourself!'}), 401

    current_user.unfollow(user)
    db.session.commit()

    return jsonify({'message': f'You have successfully unfollowed {user.name}'}), 201

@user_bp.route('/user/followers', methods=['GET'])
@login_required
def get_user_followers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Generates SQL select construct from the instance relationship
    stmt = current_user.followers.select().order_by(Relationships.followed_at.desc())

    pagination = db.paginate(
        stmt, page=page, per_page=per_page, error_out=False
    )  

    followers_data = []
    for user in pagination.items:
        followers_data.append({
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email
        })
    
    return jsonify({
        'followers' : followers_data,
        'total': pagination.total,
        'pages': pagination.pages,
        'current page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@user_bp.route('/user/followings', methods=['GET'])
@login_required
def get_user_followings():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Generates SQL select construct from the instance relationship
    stmt = current_user.following.select().order_by(Relationships.followed_at.desc())

    pagination = db.paginate(
        stmt, page=page, per_page=per_page, error_out=False
    )  

    following_data = []
    for user in pagination.items:
        following_data.append({
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email
        })
    
    return jsonify({
        'following' : following_data,
        'total': pagination.total,
        'pages': pagination.pages,
        'current page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

# TESTING ROUTE ONLY
@user_bp.route('/all-users', methods=['GET'])
# @login_required
def get_all_users():
    all_users = db.session.scalars(sa.select(User)).all()

    user_list = []
    for user in all_users:
        user_list.append({
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'followers_count': user.followers_count(),
            'following_count': user.following_count()
        })

    return jsonify({
            'count': len(user_list),
            'users': user_list
        }), 200