from recipe_cleanup import *

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

    # print(sections)

    ingredients = extract_ingredients(sections["ingredients_text"])
    instructions = extract_instructions(sections["instructions_text"])

    # print("ING", ingredients)
    # print("INS", instructions)

if __name__ == "__main__":
    main()