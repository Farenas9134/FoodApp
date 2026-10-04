import re
"""
    This file contains variables that are used
    in finding sections of the recipe as well as
    determining what is an ingredient

    Variables are lists that are very long hence 
    why they are in their own file
"""

INGREDIENT_HEADERS = [
    "ingredients",
    "ingredient list",
    "what you'll need",
    "what you need",
    "you'll need"
]

INSTRUCTION_HEADERS = [
    "instructions",
    "directions",
    "method",
    "steps",
    "preparation",
    "how to make"
]

UNITS = [
    "teaspoons", "teaspoon", "tsp",
    "tablespoons", "tablespoon", "tbsp",
    "cups", "cup",
    "ounces", "ounce", "oz",
    "pounds", "pound", "lbs", "lb",
    "grams", "gram", "g",
    "kilograms", "kilogram", "kg",
    "milliliters", "milliliter", "ml",
    "liters", "liter", "l",
    "cloves", "clove",
    "pieces", "piece",
    "slices", "slice"
]

UNIT_ALIASES = {
    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "cups": "cup",
    "ounces": "oz",
    "ounce": "oz",
    "pounds": "lb",
    "pound": "lb",
    "lbs": "lb",
    "grams": "g",
    "gram": "g",
    "kilograms": "kg",
    "kilogram": "kg",
    "milliliters": "ml",
    "milliliter": "ml",
    "liters": "l",
    "liter": "l",
    "cloves": "clove",
    "pieces": "piece",
    "slices": "slice"
}

UNIT_PATTERN = "|".join(sorted(UNITS, key=len, reverse=True))

QUANTITY_PATTERN = r"\d+(?:\.\d+)?(?:/\d+)?|½|⅓|⅔|¼|¾"

INGREDIENT_PATTERN = re.compile(
    rf"^\s*"
    rf"(?P<quantity>{QUANTITY_PATTERN})?"
    rf"\s*(?P<unit>{UNIT_PATTERN}\b)?"
    rf"\s*(?P<name>.+?)\s*$",
    re.IGNORECASE
)