from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from ..models import Recipe
from ..extensions import db

recipes_db = Blueprint('recipes', __name__)

@recipes_db.route('/recipes-submit', methods=["POST"])
# @login_required
def recipe_submit():
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
        return jsonify({"error": "Missing required fields", "missing": missing}), 400

    # Apparently modern 2.0 way to check for duplicate data
    stmt = select(Recipe).filter_by(title=data["title"], source_url=data["source_url"])
    existing_recipe = db.session.scalars(stmt).first()

    if existing_recipe:
            return jsonify({"error": "Recipe already exists in our database!"}), 400

    # For testing purposes, aka when @login_required commented out
    user_id = current_user.id if current_user.is_authenticated else 1

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
def recipes():
    # grab 10 recipes from db
    stmt = select(Recipe).limit(10)
    recipe_list = db.session.scalars(stmt).all()

    output = []

    # limited info for now, more details from specific lookup? (clicking on a recipe)
    for recipe in recipe_list:
         output.append({
              "id":recipe.recipe_id,
              "title":recipe.title,
              "image_url":recipe.image_url
              # include tags like: vegan, vegetarian, halal, etc.
         })

    return jsonify(output), 200

@recipes_db.route('/recipes/<id>', methods=["GET"])
def recipes_get_id(id):
    recipe = db.session.get(Recipe, id)
    if not recipe:
         return jsonify({"error":"Recipe not found."}), 404

    return jsonify(recipe.to_dict()), 200
