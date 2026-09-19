from app import create_app
import os

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
        ]
    }

    # Submit recipe
    response = test_client.post('/recipes-submit', json=recipe_data)
    assert response.status_code == 201, f"Route failed with response {response.get_data(as_text=True)}"
    assert 'Recipe created successfully' in response.json['message']
    assert 'Cookies' in response.json['recipe']['title']

def test_recipe_fixture(make_recipe):
    response = make_recipe()
    assert response.status_code == 201, f"Route failed with response {response.get_data(as_text=True)}"

def test_same_recipe_title(make_recipe):
    make_recipe()
    response = make_recipe(user_email='easy3@gmail.com')

    assert response.status_code == 400
    assert 'Failed to create recipe' in response.json['error']