# Guide
# https://testdriven.io/blog/flask-pytest/

# How to Run
# Use 'python -m pytest' to run all test_* files in BackEnd directory
# Use 'python -m pytest --cov=app' to see the % of code actually ran when running tests

import os
import pytest

from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture(scope='function')
def app():
    """Creates a fresh Flask app and isolated in-memory DB for each test"""
    test_config = {
        'TESTING':True,
        # runs purely in RAM
        'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:',
        # disable CSRF tokens during route testing (Flask default authentication security, but not needed here for tests)
        'WTF_CSRF_ENABLED': False
    }
    
    flask_app = create_app(test_config)

    # Create all database tables in RAM once for the entire test session
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_client(app):
    """Returns test_client bound to the shared testing app"""
    return app.test_client()

@pytest.fixture()
def make_user():
    """Function-scoped factory so users exist for duration of current test"""
    def _make_user(name='user', email='easy@email.com', password = 'easy'):
        user = User(name=name, email=email)
        user.set_password(password)
        # Populates defaults like user_id and is_admin
        db.session.add(user)
        db.session.flush()

        return user
    return _make_user

@pytest.fixture()
def make_recipe(test_client, make_user):
    """Submits a recipe to recipe route and adds to DB"""
    def _make_recipe(
        title='Cookies',
        source_url='test.com',
        source_platform='Test',
        instructions= ['Step 1: Make cookies', 'Step 2: Eat cookies'],
        image_url= 'test.com',
        tags= 'test',
        created_by='Pytest',
        recipe_ingredients= [
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
        user_email = "easy2@gmail.com",
    ):
        make_user(email=user_email, password="easy")
        login_info = {"email":user_email, "password":"easy"}
        test_client.post('/login', json=login_info)

        recipe_data = {
            'title':title,
            'source_url':source_url,
            'source_platform': source_platform,
            'instructions': instructions,
            'image_url': image_url,
            'tags': tags,
            'created_by': created_by,
            'recipe_ingredients': recipe_ingredients
        }

        response = test_client.post('/recipes-submit', json=recipe_data)
        return response
    return _make_recipe