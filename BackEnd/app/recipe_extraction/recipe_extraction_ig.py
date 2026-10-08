import requests
import json
import os

from api_key_ig import API_KEY
from recipe_cleanup import *

"""
    Extracts recipe information from instagram post descriptions like ingredients and instructions
    
    Currently only works when information is well separated and defined (i.e. explicit ingredient caption).
    Would need to use NLP or an LLM to extract information from descriptions that do not have sections
    clearly labeled
"""

def extract_recipe(instagram_link):

    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
    }

    data = json.dumps({
        "input": [{"url": instagram_link,"country":"US"}],
        "limit_per_input": 1,
    })

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lk5ns7kz21pck8jpis&notify=false&include_errors=true",
        headers=headers,
        data=data
    )

    data = response.json()

    author = data["user_posted"]
    desc = data["description"]
    hashtags = data["hashtags"]

    cleaned_desc = cleanup_caption(desc)

    sections = find_sections(cleaned_desc)

    ingredients = extract_ingredients(sections["ingredients_text"])
    instructions = extract_instructions(sections["instructions_text"])

    return {
        'title': "TBD",
        'source_url': instagram_link,
        'source_platform': "Instagram",
        'instructions': instructions,
        'image_url': None,
        'tags': hashtags,
        'created_by': author,
        'recipe_ingredients': ingredients,
        'nutrients': [],
        'description': "TBD",
        'total_time': 0,
        'category': 'TBD',
        'rating': 0,
        'servings': "TBD"
    }