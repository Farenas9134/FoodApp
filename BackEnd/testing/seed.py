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

RECIPES_TO_ADD = 1

# measures = ["tbsp","tablespoon","tsp","teaspoon","oz",
#             "ounce","fl. oz","fluid ounce","cup","qt", 
#             "quart","pt","pint","gal","gallon","mL","ml",
#             "milliliter","g","grams","kg","kilogram","l","liter"]

# sorted_measures = sorted(measures, key=len, reverse=True)
# units_regex = "|".join(re.escape(m) for m in sorted_measures)

# REGEX IS ANNOYING YET AWESOME
# WELL I GUESS SOMEONE ALREADY DID THIS
# (?P<something>...) <- defines a capture group to search for whatever rule after its name
# Made each group optional to not fail for ingredients without a count listed
# pattern = rf"^(?:(?P<amount>\d+(?:\/\d+|\.\d+)?)\s*)?(?P<unit>(?:{units_regex})\b\s*)?(?P<name>.*?)(?:,\s*(?P<notes>.*))?$"

if __name__ == "__main__":
    # lets python know we want the code to run and communicate with the app and its db
    with app.app_context():
        with open(recipe_json, 'r') as f:
            recipes_data = json.load(f)

        tables_to_reset = [
            Recipe.__table__
        ]

        db.metadata.drop_all(bind=db.engine, tables=tables_to_reset)
        db.metadata.create_all(bind=db.engine, tables=tables_to_reset)

        print("Recipe tables reset successfully.")

        # grabs all the attrs from recipe minus the ones mentioned
        recipe_fields = set(Recipe.__table__.columns.keys()) - {'recipe_id', 'created_at', 'last_updated'}

        # {'tags', 'instructions', 'source_platform', 'image_url', 'title', 'source_url', 'submitted_by','created_by'}

        for i in range(RECIPES_TO_ADD):
            ingredient_matches = []
            for field, value in recipes_data[i].items():
                # print(field,": ", value, '\n')
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

            # For each ingredient info, make ingredient instance or not
            for match in ingredient_matches:
                name = match.name[0].text.lower()
                amount = match.amount[0].quantity if len(match.amount) ==1 else 0
                unit = match.amount[0].unit if len(result.amount) ==1 else ''
                comment = match.comment.text if match.comment ==1 else ''

                ingredient = Ingredient.query.filter_by(name=name).first()

                if not ingredient:
                    ingredient = Ingredient(name=name)
                    db.session.add(ingredient)
                    db.session.flush()
                else:
                    print(f"Skipping existing ingredient")

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
