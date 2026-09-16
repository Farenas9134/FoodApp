from app import create_app
import os

def test_get_recipes():
    """
    GIVEN a FLASK application configured for testing
    WHEN the '/recipes' page is requested (GET)
    THEN check that the response is valid
    """
    # Set the Testing config prior to creating the Flask app
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask app configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/recipes')
        assert response.status_code == 200
        assert b"current_page" in response.data
        assert b"recipe" in response.data

def test_get_recipes_post():
    """
    GIVEN a FLASK application configured for testing
    WHEN the '/recipes' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """
    # Set the Testing config prior to creating the Flask app
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask app configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/recipes')
        assert response.status_code == 405
        assert b"current_page" not in response.data

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