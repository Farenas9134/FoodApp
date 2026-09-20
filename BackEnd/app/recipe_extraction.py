from recipe_scrapers import scrape_html 
from urllib.request import urlopen
from ingredient_parser import parse_ingredient

import json

##### NOTES FOR FUTURE WORK ####
# UPDATE MODELS TO INCLUDE ALL INFO RETRIEVED BY SCRAPER AND UPDATE MODELS 

#### IMPORTANT ####
# This package currently only allows the extraction from websites found in this link
# https://docs.recipe-scrapers.com/getting-started/supported-sites/ 
# Due to privacy, terms of service, and other concerns, these are the only sites that should be scraped

staples_json = '../testing/staple_dataset/staples.json'

def extract_recipe(link):
    '''
    Want a recipe in the following format

    recipe = {
        'title': '<title>',
        'source_url': '<url>',
        'source_platform': '<platform>',
        'instructions': '<list_of_instructions>',
        'image_url': '<image_url>',
        'tags': '<tags>',
        'created_by':'<author>',
        'recipe_ingredients': '<list_of_ingredients>'
    }
    '''

    # CURRENTLY ONLY WORKS FOR RECIPES FROM americastestkitchen.com

    url = link
    html = urlopen(url).read().decode("utf-8")
    scraper = scrape_html(html, org_url=url)

    title = scraper.title()
    source_url = scraper.canonical_url()
    platform = scraper.host()
    instructions = scraper.instructions_list()
    image = scraper.image()
    tags = scraper.keywords()
    author = scraper.author()
    ing_list = scraper.ingredients()
    print("TEST", scraper.canonical_url())
    recipe = {
        'title': title,
        'source_url': source_url,
        'source_platform':  platform,
        'instructions': instructions,
        'image_url': image,
        'tags': tags,
        'created_by': author,
        'recipe_ingredients': ing_list
    }    

    return recipe

def main():
    # recipe = extract_recipe("https://www.americastestkitchen.com/recipes/16181-ancho-rubbed-flank-steak-and-cilantro-rice-with-avocado-sauce")

    recipe2 = extract_recipe("https://www.delish.com/cooking/recipe-ideas/a61807164/best-pumpkin-smores-cookies-recipe/")
    # print(recipe)

if __name__ == "__main__":
    main()