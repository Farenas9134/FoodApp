import json
import emoji
import re
import unicodedata

from recipe_extraction_vars import INGREDIENT_HEADERS, INSTRUCTION_HEADERS, UNITS, UNIT_PATTERN, UNIT_ALIASES, QUANTITY_PATTERN, INGREDIENT_PATTERN, fractions

"""
    This function cleans up captions by removing URLs, standardizing bullet points, and 
    cleaning up excessive space 
"""
def cleanup_caption(caption):
    # Cleaning up fractions
    for fraction, replacement in fractions.items():
        caption = caption.replace(fraction, replacement)

    # Normalizing UNICODE characters
    caption = unicodedata.normalize("NFKC", caption)
    
    # Removing URLs
    caption = re.sub(r"https?://\S+|www\.\S+", "", caption)
    
    # Removing hashtag symbols
    caption = re.sub(r"#\w+", "", caption)
    caption = re.sub(r"#+", "", caption)

    # Normalizing bullet characters to be the same
    caption = re.sub(r"^[\s]*[•▪◦]\s*", "- ", caption, flags=re.MULTILINE)

    # Removing excessive space but keeping newlines
    caption = re.sub(r"[ \t]+", " ", caption)

    # Removing excessive blank lines (more than 3 blank lines)
    caption = re.sub(r"\n{3,}", "\n\n", caption)

    return caption.strip()

"""
    Helper function for find_sections()
"""
def normalize_header(line):
    line = line.lower().strip()
    line = re.sub(r"^[^\w]+|[^\w]+$", "", line)

    return line

def is_ingredient_header(line):

    return 0

"""
    This function identifies ingredient and instruction sections
    Doesn't currently work when sections are not labeled explicitly
    -> may need to use an LLM or NLP to take care of that case in the future
"""
def find_sections(caption):
    sections = {
        "ingredients_text": [],
        "instructions_text": []
    }

    current_section = None

    for line in caption.splitlines():
        clean_line = normalize_header(line)

        # print("RAW:", repr(line))
        # print("CLEANED", repr(clean_line))

        if clean_line in INGREDIENT_HEADERS:
            current_section = "ingredients_text"
            continue

        if clean_line in INSTRUCTION_HEADERS:
            current_section = "instructions_text"
            continue

        if clean_line in ["notes", "nutrition", "tips", "storage"]:
            current_section = None
            continue

        if line.strip() and current_section:
            sections[current_section].append(line.strip())

    return {
        "ingredients_text": "\n".join(sections["ingredients_text"]),
        "instructions_text": "\n".join(sections["instructions_text"])
    }

"""
    Parse an ingredient and split it into components like quantity, unit,
    and name of the recipe 
    Helper function for extract_ingredients()

    Not necessarily needed at the moment but could be used in the future
"""
# def parse_ingredient(line):

#     line = re.sub(r"^\s*(?:[-*•]\s*|\d+[.)]\s*)", "", line)

#     if not line:
#         return None

#     match = INGREDIENT_PATTERN.match(line)

#     if not match:
#         return {
#             "quantity": None,
#             "unit": None,
#             "name": line,
#             "original": line
#         }

#     quantity = match.group("quantity")
#     unit = match.group("unit")
#     name = match.group("name")
#     name = name.strip(" ,")

#     return {
#         "quantity": quantity,
#         "unit": unit.lower() if unit else None,
#         "name": name,
#         "original": line
#     }

"""
    Extracts only the ingredients from the ingredients_text section of the caption
"""
def extract_ingredients(ingredients_text):
    
    ingredients = []

    for line in ingredients_text.splitlines():
        line = line.strip()

        if not line:
            continue

        line = re.sub(r"^\s*(?:[-*•]\s*|\d+[.)]\s*)", "", line)


        ingredients.append(line)

        # ingredient = parse_ingredient(line)

        # if ingredient:
        #     ingredients.append(ingredient)

    return ingredients

"""
    Extracts only the instructions from the instructions_text section of the caption
"""
def extract_instructions(instructions_text):
    if not instructions_text.strip():
        return []

    lines = instructions_text.splitlines()

    steps = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Getting rid of numbers or bullet points
        line = re.sub(r"^(?:\d+[.)]\s*|[-*•▪◦]\s*)", "", line).strip()

        if line:
            steps.append(line)

        # If instructions are a long paragraph
        # Potential issue if a step has multiple sentences
        if len(lines) == 1:
            sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", steps[0])

            if len(sentences) > 1:
                steps = sentences

        return steps

"""
    Normalizes each recipe so they all use the same unit representation
"""
# def normalize_recipe(ingredients, instructions):
#     normalized_ingredients = []

#     for ingredient in ingredients:
#         unit = ingredient["unit"]

#         if unit:
#             unit = UNIT_ALIASES.get(unit.lower(), unit.lower())

#         normalized_ingredients.append({
#             **ingredient,
#             "unit": unit,
#             "name": ingredient["name"].strip()
#         })

#     normalized_instructions = [
#         step.strip() for step in instructions if step.strip()
#     ]

#     return {
#         "ingredients": normalized_ingredients,
#         "instructions": normalized_instructions
#     }

# def validate_recipe(recipe):
    

# def main():
#     with open('test.json', 'r', encoding="utf-8") as file:
#         data = json.load(file)

#     author = data["user_posted"]
#     desc = data["description"]

#     cleaned_desc = cleanup_caption(desc)

#     # print(cleaned_desc)

#     sections = find_sections(cleaned_desc)

#     ingredients = extract_ingredients(sections["ingredients_text"])

#     instructions = extract_instructions(sections["instructions_text"])

#     # recipe = normalize_recipe(ingredients, instructions)

#     # fin_recipe = {
#     #     "ingredients": recipe["ingredients"],
#     #     "instructions": recipe["instructions"],
#     #     "raw_caption": cleaned_desc
#     # }

#     print("Ingredients", ingredients)

#     print("Instructions", instructions)

# if __name__ == "__main__":
#     main()