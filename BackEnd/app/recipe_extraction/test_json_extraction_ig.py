import json
import emoji
import re
import unicodedata

from recipe_extraction_vars import INGREDIENT_HEADERS, INSTRUCTION_HEADERS, UNITS, UNIT_PATTERN, QUANTITY_PATTERN, INGREDIENT_PATTERN

"""
    This function cleans up captions by removing URLs, standardizing bullet points, and 
    cleaning up excessive space 
"""
def cleanup_caption(caption):
    # Normalizing UNICODE characters
    caption = unicodedata.normalize("NFKC", caption)
    
    # Removing URLs
    caption = re.sub(r"https?://\S+|www\.\S+", "", caption)
    
    # Removing hashtag symbols
    caption = re.sub(r"#\w+", "", caption)

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
"""
def parse_ingredient(line):

    line = re.sub(r"^\s*[-*•\d.)]+\s*", "", line).strip()

    if not line:
        return None

    match = INGREDIENT_PATTERN.match(line)

    if not match:
        return {
            "quantity": None,
            "unit": None,
            "name": line,
            "original": line
        }

    quantity = match.group("quantity")
    unit = match.group("unit")
    name = match.group("name")
    name = name.strip(" ,")

    return {
        "quantity": quantity,
        "unit": unit.lower() if unit else None,
        "name": name,
        "original": line
    }

"""
    Extracts only the ingredients from the ingredients_text section of the caption
"""
def extract_ingredients(ingredients_text):
    
    ingredients = []

    for line in ingredients_text.splitlines():
        line = line.strip()

        if not line:
            continue

        ingredient = parse_ingredient(line)

        if ingredient:
            ingredients.append(ingredient)

    return ingredients

def main():
    with open('test.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    desc = data["description"]

    cleaned_desc = cleanup_caption(desc)

    print(cleaned_desc)

    sections = find_sections(cleaned_desc)

    print(extract_ingredients(sections["ingredients_text"]))


if __name__ == "__main__":
    main()