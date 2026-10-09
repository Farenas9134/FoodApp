import requests
import json
import time

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

    max_attempts = 2
    num_attempts = 0
    snapshot_id = ""

    # In case snapshot is not ready to be downloaded yet
    if response.status_code == 202:
        snapshot_id = response.json()['snapshot_id']
        print("Snapshot is not quite ready to download, trying again in 30 seconds")

    # Wait for 1 minute if snapshot not ready to be downloaded
    while response.status_code == 202 and num_attempts < max_attempts:
        time.sleep(30)
        num_attempts += 1

        print(f"Job is running with Snapshot ID: {snapshot_id}")
        # print("Trying again...")

        url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"

        headers = {"Authorization": "Bearer " + API_KEY}

        response = requests.get(url, headers=headers)

    # In case scraping takes too long, will modify timeout time later
    if num_attempts == max_attempts:
        print("Scraping took too long, try again later")
        exit(1)

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