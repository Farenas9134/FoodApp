"""
    Script for testing purposes only

    Adds n ingredients into db.
    Recipes from the USDA Foundation Foods dataset
    Script is hyper-tuned to only work with only this dataset

    A LOTTTTT of info is in the dataset, I only got simple stuff

    Run in BackEnd directory:
        python -m staples.seed
"""

import json

from app import create_app
from app.extensions import db
from app.models import Ingredient

app = create_app()

staples_json = 'testing/staple_dataset/staples.json'

STAPLES_TO_ADD = 363

# ['foodClass', 'description', 'foodNutrients', 'foodAttributes', 
# 'nutrientConversionFactors', 'isHistoricalReference', 'ndbNumber', 'foodCategory', 
# 'fdcId', 'dataType', 'foodPortions', 'publicationDate', 'inputFoods']

'''
    What I need: Name, calories, protein gram, carbs gram, fat gram, 
                 is_verified, created_by"
'''

if __name__ == '__main__':
    # Communicate with app from testing its db
    with app.app_context():
        # Open the dataset and load it in
        with open(staples_json, 'r') as f:
            staples_data = json.load(f)

        print('Extracting ingredient info')

        for i in range(STAPLES_TO_ADD):
            for field, value in staples_data[i].items():
                if field == 'description':
                    name = value.replace(',', '')

                if field == 'foodNutrients':
                    # Grab macro nutrients per 100g
                    for row in value:
                        if row['nutrient']['name'] == 'Protein':
                            protein= row['amount']
                        if row['nutrient']['name'] == 'Carbohydrate, by difference':
                            carbs = row['amount']
                        if row['nutrient']['name'] == 'Total fat (NLEA)':
                            fat = row['amount']
                        if row['nutrient']['number'] == '208':
                            calories = row['amount']

                if field == 'foodCategory':
                    category = value['description']

            # Create ingredient instance
            ingredient = Ingredient.query.filter_by(name=name).first()
            if ingredient: print(f"Skipped existing {name} ingredient.")
            if not ingredient:
                # Created by 1 -> admin id, and is_verified True as a staple ingredient
                ingredient = Ingredient(name=name, calories=calories, protein_g = protein, carbs_g = carbs, fat_g=fat, is_verified=True, created_by=1)
                db.session.add(ingredient)
                db.session.flush()
                print(f"Successfully added {name} with {calories} calories")

        db.session.commit()
        print("Successfully ran staples script!")                