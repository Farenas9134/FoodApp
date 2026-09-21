from app import create_app, recipe_extraction
import pytest

'''
From the BackEnd directory

python -m pytest
'''
def test_get_recipes_with_fixture(test_client):
    """
    GIVEN a FLASK application configured for testing
    WHEN the '/recipes' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/recipes')
    assert response.status_code == 200
    assert b"current_page" in response.data
    assert b"recipe" in response.data


# NOT WORKING CURRENTLY, THE MODEL NEEDS UPDATING TO HANDLE LISTS OF TAGS #
# KNOWN TO BE BROKEN #
def test_extraction_and_submit_recipe(test_client, make_user):
    """
    Testing recipe extraction from a URL and then submitting the recipe to the database
    """
    make_user()
    login_info = {"email":"easy@email.com", "password":"easy"}
    login_response = test_client.post('/login', json=login_info)
    assert login_response.status_code == 201

    recipe = recipe_extraction.extract_recipe("https://www.americastestkitchen.com/recipes/16181-ancho-rubbed-flank-steak-and-cilantro-rice-with-avocado-sauce")

    # Submit recipe
    response = test_client.post('/recipes-submit', json=recipe)
    assert response.status_code == 201, f"Route failed with response {response.get_data(as_text=True)}"
    assert 'Recipe created successfully' in response.json['message']
    assert 'Steak and Cilantro Rice' in response.json['recipe']['title']

def test_submit_recipe(test_client, make_user):
    """
    GIVEN a logged in user with appropriate fields for a recipe
    WHEN submitting a recipe
    THEN successfully create a recipe record
    """
    # Successfully log in as a user
    make_user()
    login_info = {"email":"easy@email.com", "password":"easy"}
    login_response = test_client.post('/login', json=login_info)
    assert login_response.status_code == 201

    # Create recipe data
    recipe_data = {
        'title':'Cookies',
        'source_url':'test.com',
        'source_platform':'Test',
        'instructions': ['Step 1: Make cookies', 'Step 2: Eat cookies'],
        'image_url': 'test.com',
        'tags': 'test',
        'created_by':'Pytest',
        'recipe_ingredients': [
            '1 cup salted butter softened',
            '1 cup granulated sugar',
            '1 cup light brown sugar packed',
            '2 teaspoons pure vanilla extract',
            '2 large eggs',
            '3 cups all-purpose flour',
            '1 teaspoon baking soda',
            '½ teaspoon baking powder',
            '1 teaspoon sea salt',
            '2 cups chocolate chips (12 oz)'
        ],
        'nutrients': {'calories': '850 Calories', 'fatContent': '22 g', 'saturatedFatContent': '7 g',
                      'transFatContent': '0 g', 'cholesterolContent': '50 mg', 'sodiumContent': '70 mg', 
                      'carbohydrateContent': '15 g', 'fiberContent': '7 g', 'sugarContent': '21 g', 'proteinContent': '67 g'},
        'description': 'Yummy cookies',
        'total_time': 65,
        'category': 'Dessert',
        'rating': 4.2,
        'servings': '3 servings'
    }

    # Submit recipe
    response = test_client.post('/recipes-submit', json=recipe_data)
    assert response.status_code == 201, f"Route failed with response {response.get_data(as_text=True)}"
    assert 'Recipe created successfully' in response.json['message']
    assert 'Cookies' in response.json['recipe']['title']

def test_recipe_fixture(make_recipe):
    """
    GIVEN a request to make a recipe
    WHEN accessing the make_recipe ficture
    THEN successfully add a recipe to the DB
    """
    response = make_recipe()
    assert response.status_code == 201

def test_same_recipe_title(make_recipe):
    """
    GIVEN a recipe with the same name as an existing recipe
    WHEN submitting a recipe
    THEN throw an error
    """
    make_recipe()
    response = make_recipe(user_email='easy3@gmail.com')

    assert response.status_code == 400
    assert 'Failed to create recipe' in response.json['error']

# Set of Parametrized tests for several edge cases
@pytest.mark.parametrize("data, expected_status, expected_error", [
    # Case 1: No recipe data given
    ({}, 400, "Missing required fields"),
    # Case 2: Invalid data input
    (3, 400, "Request body must be valid"),
    # Case 3: Missing fields in recipe body
    ({'title':'Broken Recipe', 'created_by':'Broke'}, 400, "Missing required fields"),
    # Case 4: No ingredients given
    (
        {
        'title':'Cookies',
        'source_url':'test.com',
        'source_platform':'Test',
        'instructions': ['Step 1: Make cookies', 'Step 2: Eat cookies'],
        'image_url': 'test.com',
        'tags': 'test',
        'created_by':'Pytest',
        'recipe_ingredients': [],
        'nutrients': {'calories': '850 Calories', 'fatContent': '22 g', 'saturatedFatContent': '7 g',
                      'transFatContent': '0 g', 'cholesterolContent': '50 mg', 'sodiumContent': '70 mg', 
                      'carbohydrateContent': '15 g', 'fiberContent': '7 g', 'sugarContent': '21 g', 'proteinContent': '67 g'},
        'description': 'Yummy cookies',
        'total_time': 65,
        'category': 'Dessert',
        'rating': 4.2,
        'servings': '3 servings' 
        }, 400, "Failed to create recipe")
])
def test_recipe_submit_edge_cases(test_client, data, expected_status, expected_error, make_user):
    """
    GIVEN missing recipe data fields
    WHEN submitting a recipe as a authorized user
    THEN throw an appropraite error
    """
    make_user(email="logmein@gmail.com", password="easy")
    login_info = {'email':'logmein@gmail.com', 'password':'easy'}
    login_res = test_client.post('/login', json=login_info)
    assert login_res.status_code == 201

    recipe_res = test_client.post('recipes-submit', json=data)
    assert recipe_res.status_code == expected_status
    assert expected_error in recipe_res.json['error']

def test_get_recipes(test_client, make_user, make_recipe):
    """
    GIVEN a GET request
    WHEN targeting the get_recipes route
    THEN display current recipes in DB
    """
    # Successfully log in as a user
    # Honestly didn't need to make a user, because make_recipes() handles that, but good practice
    make_user()
    login_info = {"email":"easy@email.com", "password":"easy"}
    login_response = test_client.post('/login', json=login_info)
    assert login_response.status_code == 201

    # Submit a recipe with user (just changing default email to the one we used above)
    recipe_response = make_recipe(user_email='easy@gmail.com')
    assert recipe_response.status_code == 201

    # Now request recipes with 1 recipe in DB
    response = test_client.get('/recipes')

    assert response.status_code == 200
    assert b'recipes' in response.data
    assert b'current_page' in response.data
    # Access recipes field, then the first record, and then the title
    assert 'Cookies' in response.json['recipes'][0]['title']

def test_get_recipe_by_id(test_client, make_recipe, capsys):
    """
    GIVEN a proper GET recipe request
    WHEN targeting the get recipe route
    THEN return wanted recipe details
    """
    recipe_res = make_recipe()
    assert recipe_res.status_code == 201

    res = test_client.get('/recipes/1')
    assert res.status_code == 200
    assert b'recipe' in res.data
    assert b'ingredients' in res.data
    assert 'Cookie' in res.json['recipe']['title']
    # If you want to print out something, like this:
    # with capsys.disabled():
    #     print(res.json['ingredients'][0])

    # Need to properly search all ings, but this works for now
    assert 'salted butter' in res.json['ingredients'][0]['name']

def test_get_recipe_by_invalid_id(test_client):
    """
    GIVEN an invalid GET recipe request
    WHEN targeting the get recipe route with a non-existant id
    THEN return a 404 error
    """

    res = test_client.get('/recipes/1')
    assert res.status_code == 404
    assert b'Recipe does not exist' in res.data

# Need to think about this.
# If available to seach by ingredients, then user pantry is basically complete, but its not
# WIP
# def test_search_recipes(test_client, make_recipe):
#     """
#     GIVEN a proper search request
#     WHEN accessing /recipes/search
#     THEN return """

def test_delete_recipe(test_client, make_recipe):
    """
    GIVEN a logged in user
    WHEN deleting a recipe user created
    THEN successfully delete the recipe and recipeIngredient records from DB
    """
    # Create recipe
    recipe_res = make_recipe()
    assert recipe_res.status_code == 201

    # Delete recipe
    res = test_client.delete('/recipes/1')
    assert res.status_code == 200
    assert 'Recipe deleted successfully' in res.json['message']

    # Attempt to grab recipe
    double_check_res = test_client.get('recipes/1')
    assert double_check_res.status_code == 404

    # Check if recipeIngredients exist (None should exist)
    ing_res = test_client.get('/recipeIng')
    assert ing_res.status_code == 200

def test_delete_recipe_invalid_auth(test_client, make_recipe, make_user):
    """
    GIVEN a logged in user
    WHEN deleting a recipe user did NOT created
    THEN throw an error
    """
    # Create recipe
    recipe_res = make_recipe()
    assert recipe_res.status_code == 201

    # Make new user
    make_user(email="newUser@gmail.com")
    login_info = {'email':'newUser@gmail.com', 'password':'easy'}
    login_response = test_client.post('/login', json=login_info)
    assert login_response.status_code == 201

    # Attempt to delete recipe
    res = test_client.delete('/recipes/1')
    assert res.status_code == 401
    assert 'User did not submit this recipe' in res.json['error']

def test_update_recipe(test_client, make_recipe, capsys):
    """
    GIVEN proper recipe format with new recipe data
    WHEN accessing the update recipe route
    THEN successfully update the recipe
    """
    # Create recipe
    recipe_res = make_recipe()
    assert recipe_res.status_code == 201

    # Need to include all prev. ings. or it'll think you meant to remove/delete that ing 
    new_recipe_info = {
        'title':'Changed You!',
        'source_platform':'Instagram',
        'recipe_ingredients':
        [{'name':'GOLD GOLD GOLD', 'amount':'500', 'unit':'Tbsp'},
         {'name':'eggs', 'amount':'400'},
         {'name:':'salted butter'},
         {'name':'granulated sugar'},
         {'name':'light brown sugar'},
         {'name':'pure vanilla extract'},
         {'name':'all-purpose flour'},
         {'name':'baking soda'},
         {'name':'baking powder'},
         {'name':'sea salt'},
         {'name':'chocolate chips'},
        ]
    }
    # Update recipe
    res = test_client.put('/recipes/1', json=new_recipe_info)
    assert res.status_code == 200
    assert b'Changed You!' in res.data
    assert b'Instagram' in res.data
    assert b'gold gold gold' in res.data
    assert 400 == res.json['ingredients'][3]['amount']