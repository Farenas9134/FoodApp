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
from app.models import User, Recipe, RecipeIngredient, Ingredient
from sqlalchemy import text
import re
from ingredient_parser import parse_ingredient

app = create_app()

recipe_json = 'testing/recipes-main/recipes.json'

RECIPES_TO_ADD = 20

def safe_parse_amounts(raw_quantity):
    'Converts quantity to float. Returns amount, extra_notes'
    if not raw_quantity:
        return 0.0, ''
    try:
        return float(raw_quantity), ""
    except (ValueError, TypeError):
        # Parse_ingredient() likely returned non-numeric string as the amount
        return 0.0, str(raw_quantity)

if __name__ == "__main__":
    # lets python know we want the code to run and communicate with the app and its db
    with app.app_context():
        with open(recipe_json, 'r') as f:
            recipes_data = json.load(f)

        tables_to_reset = [
            RecipeIngredient.__table__,
            Recipe.__table__
        ]

        # Drop/Delete all data concerning tables we want to reseed
        db.metadata.drop_all(bind=db.engine, tables=tables_to_reset)
        db.metadata.create_all(bind=db.engine, tables=tables_to_reset)

        print("Recipe tables reset successfully.")

        # Extract recipe info for RECIPES_TO_ADD number of recipes
        for i in range(RECIPES_TO_ADD):
            ingredient_matches = []
            for field, value in recipes_data[i].items():
                if field == 'Name':
                    title = value
                elif field == 'url':
                    source_url = value
                elif field == 'Author':
                    created_by = value
                elif field == 'Method':
                    instructions = value

                # Get info out of ingredients portion to make ingredient instances, store for now into list
                elif field == 'Ingredients':
                    for item in value:
                        result = parse_ingredient(item)
                        ingredient_matches.append(result)
                        # print(item)
                        # print("Name:", result.name[0].text)
                        # print("Size:", result.size)
                        # if len(result.amount) ==1:
                        #     print("Quantity:", result.amount[0].quantity)
                        #     print("Unit:", result.amount[0].unit)
                        # if result.preparation:
                        #     print("Prep:", result.preparation.text)
                        # if result.comment:
                        #     print("Comment:", result.comment.text)
                        # if result.purpose:
                        #     print("Purpose:", result.purpose.text)
                        # print("\n")

            # Arbitrary info for seeded recipes
            image_url = f'{title}.jpg'
            source_platform = 'Dataset'
            tags = "seeded"
            submitted_by = 999

            if Recipe.query.filter_by(title=title).first():
                print(f"Skipping existing recipe: {title}")
                continue

            # create recipe instance for id
            new_recipe = Recipe(title=title, source_url=source_url, created_by=created_by, 
                                instructions=instructions, image_url=image_url, source_platform=source_platform, tags=tags, submitted_by=submitted_by)
            db.session.add(new_recipe)
            db.session.flush()

            # Add to seen ids to avoid doubles
            seen_ingredient_ids = set()

            # For each ingredient info, make ingredient instance or not
            for match in ingredient_matches:
                if not match.name:
                    continue
                name = match.name[0].text.lower()

                raw_qty = match.amount[0].quantity if len(match.amount) ==1 else 0
                amount, extra_note = safe_parse_amounts(raw_qty)
                
                unit = str(match.amount[0].unit) if len(match.amount) ==1 else ''

                # Extract comment and merge any extra notes
                base_comment = match.comment.text if match.comment else ''
                comment = f"{extra_note} {base_comment}".strip()

                # Fetch or create Ingredient
                ingredient = Ingredient.query.filter_by(name=name).first()
                if not ingredient:
                    ingredient = Ingredient(name=name)
                    db.session.add(ingredient)
                    db.session.flush()

                # Skip duplicates for this recipe
                if ingredient.id in seen_ingredient_ids:
                    print(f"Skipping duplicate ingredient '{name}' in recipe '{title}'")
                    continue

                seen_ingredient_ids.add(ingredient.id)

                # Add RecipeIngredient instance
                recipe_ingredient = RecipeIngredient(recipe_id=new_recipe.recipe_id, ingredient_id=ingredient.id, amount=amount, unit=unit, notes=comment)
                db.session.add(recipe_ingredient)

        db.session.commit()
        print(f"Successfully ran seed script!")

# Example dataset input:
# {"Name": "Christmas pie", 
# "url": "https://www.bbcgoodfood.com/recipes/2793/christmas-pie", 
# "Description": "Combine a few key Christmas flavours here to make a pie that both children and adults will adore", 
# "Author": "Mary Cadogan", 
# "Ingredients": ["2 tbsp olive oil", "knob butter", "1 onion, finely chopped", "500g sausagemeat or skinned sausages", "grated zest of 1 lemon", "100g fresh white breadcrumbs", "85g ready-to-eat dried apricots, chopped", "50g chestnut, canned or vacuum-packed, chopped", "2 tsp chopped fresh or 1tsp dried thyme", "100g cranberries, fresh or frozen", "500g boneless, skinless chicken breasts", "500g pack ready-made shortcrust pastry", "beaten egg, to glaze"], 
# "Method": ["Heat oven to 190C/fan 170C/gas 5. Heat 1 tbsp oil and the butter in a frying pan, then add the onion and fry for 5 mins until softened. Cool slightly. Tip the sausagemeat, lemon zest, breadcrumbs, apricots, chestnuts and thyme into a bowl. Add the onion and cranberries, and mix everything together with your hands, adding plenty of pepper and a little salt.", "Cut each chicken breast into three fillets lengthwise and season all over with salt and pepper. Heat the remaining oil in the frying pan, and fry the chicken fillets quickly until browned, about 6-8 mins.", "Roll out two-thirds of the pastry to line a 20-23cm springform or deep loose-based tart tin. Press in half the sausage mix and spread to level. Then add the chicken pieces in one layer and cover with the rest of the sausage. Press down lightly.", "Roll out the remaining pastry. Brush the edges of the pastry with beaten egg and cover with the pastry lid. Pinch the edges to seal, then trim. Brush the top of the pie with egg, then roll out the trimmings to make holly leaf shapes and berries. Decorate the pie and brush again with egg.", "Set the tin on a baking sheet and bake for 50-60 mins, then cool in the tin for 15 mins. Remove and leave to cool completely. Serve with a winter salad and pickles."]},
