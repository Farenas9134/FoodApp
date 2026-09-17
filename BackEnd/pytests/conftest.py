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

@pytest.fixture(scope='session')
def app():
    """Creates a single Flask app instance configured for in-memory testing"""
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
        db.drop_all()

@pytest.fixture(autouse=True)
def app_context(app):
    """Guarantees a clean app context exists for every single test"""
    # Context object to track global values like request, current_app, etc.
    context = app.app_context()
    # Pushes context to Flask's global stack so models & routes know which app is running
    context.push()

    yield context

    # Clean up SQLAlchemy session before popping context
    db.session.remove()
    # Removes context after test ends to clean up memory
    context.pop()

@pytest.fixture(autouse=True)
def db_transaction(app_context):
    """Wraps each test in an isolated connection transaction.
    Interprets route db.session.commit() calls safely and rolls them back after test finishes"""
    # Opens direct connection to RAM sqlite db
    connection = db.engine.connect()
    # starts top-level SQL transaction. Any db writes after this live in uncomitted sandbox
    transaction = connection.begin()

    # Forces all queries/actions to run strictly through our connection instead of new ones
    options = dict(bind=connection, binds={})

    # Creates custom SQLAlchemy session bound to our connection and replaces Flask global db.session with it
    #   calls like db.session.commit() commits in our open transaction instead of writing to disk
    session = db._make_scoped_session(options=options)
    db.session = session

    # Setup done, passes env. to test. All requests, db queries, and route logic execute inside the sandbox
    yield

    session.remove()
    # Undoes all insert/update/delete performed during test, resetting in-memory db to default empty state
    transaction.rollback()
    # Closes connection
    connection.close()

@pytest.fixture
def test_client(app):
    """Returns test_client bound to the shared testing app"""
    return app.test_client()

@pytest.fixture()
def make_user():
    """Function-scoped factory so users exist for duration of current test"""
    def _make_user(name='pytester', email='pytests0@gmail.com'):
        user = User(name=name, email=email)
        user.set_password('FlaskIsAwesome')
        # Populates defaults like user_id and is_admin
        db.session.add(user)
        db.session.flush()

        return user
    return _make_user