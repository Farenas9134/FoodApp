# Guide
# https://testdriven.io/blog/flask-pytest/

# How to Run
# Use 'python -m pytest' to run all test_* files in BackEnd directory
# Use 'python -m pytest --cov=app' to see the % of code actually ran when running tests

import os

import pytest

from app.models import User
from app import create_app
from app.extensions import db


@pytest.fixture(scope='module')
def test_client():
    # Set the Testing config prior to creating the Flask app
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an app context
        with flask_app.app_context():
            yield testing_client # this is where testing happens

@pytest.fixture(scope='function')
def new_user(test_client):
    user = User(name='pytester', email='pytests0@gmail.com')
    user.set_password('FlaskIsAwesome')

    # Populates defaults like user_id and is_admin
    db.session.add(user)
    db.session.flush()

    yield user

    # Cleans up after test completes
    db.session.rollback()