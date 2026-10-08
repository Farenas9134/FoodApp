from recipe_cleanup import *
from recipe_extraction_vars import INGREDIENT_HEADERS, INSTRUCTION_HEADERS, UNITS, UNIT_ALIASES, UNIT_PATTERN, QUANTITY_PATTERN, INGREDIENT_PATTERN

import json

def main():
    with open('tiktok_recipe.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    author = data['account_id']
    source_url = data["url"]
    desc = data["description"]

    cleaned_desc = cleanup_caption(desc)

    print("CLEAN", cleaned_desc)
    
    sections = find_sections(cleaned_desc)

    ingredients = extract_ingredients(sections["ingredients_text"])
    instructions = extract_instructions(sections["instructions_text"])

    # print("INGREDIENTS", ingredients)
    # print("INSTRUCTIONS", instructions)


if __name__ == "__main__":
    main()