from flask import Blueprint, request, jsonify
from ..models import Recipe
from .. import db

recipes_db = Blueprint('recipes', __name__, template_folder='templates')

@recipes_db.route('/recipes-submit', methods=["POST"])
def recipes():

    data = request.get_json()
    if not data: return jsonify({"error": "Missing JSON body"}), 400

    required_fields = [
        "title",
        "source_url",
        "source_platform",
        "ingredients",
        "instructions",
        "image_url",
        "submitted_by"
    ]

    missing = []
    for field in required_fields:
        if field not in data:
            missing.append(field)

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing
        }), 400

    recipe = Recipe.query.filter_by(title=data["title"], source_url=data["source_url"]).first()

    if recipe:
            return jsonify({
                "error": "Recipe already exists in our database!"
            }), 400

    new_recipe = Recipe(
        title = data["title"], 
        source_url = data["source_url"], 
        source_platform = data["source_platform"],
        ingredients = data["ingredients"],
        instructions = data["instructions"],
        image_url = data["image_url"],
        submitted_by = data["submitted_by"]
    )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({
        "message":"Recipe created successfully",
        "recipe":{
            "title": data["title"],
            "source_platform": data["source_platform"],
            "submitted_by": data["submitted_by"]
        }
    })
