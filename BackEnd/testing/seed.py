"""
    Script for testing purposes only

    Adds n recipes into db.
    Recipes from a dataset I found on google.
    Script is hyper-tuned to only work with only this dataset

    Run in BackEnd directory:
        python -m testing.seed
"""

import json

from app import create_app
from app.extensions import db
from app.models import User, Recipe
from sqlalchemy import text

app = create_app()

recipe_json = 'testing/recipes-main/recipes.json'

RECIPES_TO_ADD = 20

if __name__ == "__main__":
    # lets python know we want the code to run and communicate with the app and its db
    with app.app_context():
        with open(recipe_json, 'r') as f:
            recipes_data = json.load(f)

        db.drop_all()
        db.create_all()
        print("Database schema reset successfully.")

        # grabs all the attrs from recipe minus the ones mentioned
        recipe_fields = set(Recipe.__table__.columns.keys()) - {'recipe_id', 'created_at', 'last_updated'}

        for i in range(RECIPES_TO_ADD):
            for field, value in recipes_data[i].items():
                # print(field,": ", value, '\n')
                if field == 'Name':
                    title = value
                elif field == 'url':
                    source_url = value
                elif field == 'Author':
                    created_by = value
                elif field == 'Ingredients':
                    ingredients = value
                elif field == 'Method':
                    instructions = value
            image_url = f'{title}.jpg'
            source_platform = 'Dataset'
            tags = "seeded"
            submitted_by = 999

            if Recipe.query.filter_by(title=title).first():
                print(f"Skipping existing recipe: {title}")
                continue

            new_recipe = Recipe(title=title, source_url=source_url, created_by=created_by, ingredients=ingredients, 
                                instructions=instructions, image_url=image_url, source_platform=source_platform, tags=tags, submitted_by=submitted_by)
            db.session.add(new_recipe)

        db.session.commit()
        print(f"Successfully ran seed script!")
