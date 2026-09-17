import pytest

def test_sign_up(test_client):
    """
    GIVEN data for a new User
    WHEN a user wants to sign up
    THEN a new User instance is created
    """
    data = {
        "name": "manualUser",
        "email": "testing@gmail.com",
        "password": "passwordsrule"
    }

    response = test_client.post('/signup', json=data)

    assert response.status_code == 201
    assert "User created successfully" in response.json['message']

# Set of Parametrized tests for no repeated code to test each individually
@pytest.mark.parametrize("data, expected_status, expected_error", [
    # Case 1: Missing email
    ({"name":"test", "password":"pass"}, 400, "Missing required fields"),
    # Case 2: Missing name
    ({"email":"test@gmail.com", "password":"pass"}, 400, "Missing required fields"),
    # Case 3: Missing password
    ({"name":"test", "email":"pass@gmail.com"}, 400, "Missing required fields"),
    # Case 4: Empty string values
    ({"name":"", "password":"pass", "email":"email@gmail.com"}, 400, "Missing required fields"),
    # Case 5: No data
    ({}, 400, "Missing required fields"),
    # Case 6: Empty string data
    ("", 400, "Request body must be valid JSON"),
    # Case 7: Wrong data type input
    (67, 400, "Request body must be valid JSON")
])

def test_sign_up_missing_fields_validation(test_client, data, expected_status, expected_error):
    """
    GIVEN missing user data fields
    WHEN signing up as a user 
    THEN throw an error for missing data
    """
    response = test_client.post('/signup', json=data)
    
    assert response.status_code == expected_status
    assert expected_error in response.json['error']

def test_identical_email_on_signup(test_client):
    """
    GIVEN previously used email
    WHEN signing up as a new user
    THEN throw an error for email used
    """
    data = {
        "name":"myEmail",
        "email":"email@email.com",
        "password":"pass"
    }
    test_client.post('/signup', json=data)
    response = test_client.post('/signup', json=data)

    assert response.status_code == 400
    assert "Email attached to existing user" in response.json['error']

def test_sign_in(test_client, make_user):
    """
    GIVEN correct user login info
    WHEN signing in
    THEN successfully log user in
    """
    # Don't need the 'name=' stuff, but there for explicit showing
    make_user(name="LogMeIn", email="LogMe@In.com", password="LogMeIn")
    data = {"email":"LogMe@In.com", "password":"LogMeIn"}

    response = test_client.post('/login', json=data)

    assert response.status_code == 201
    assert "Successful login" in response.json['message']

# Set of Parametrized tests for no repeated code to test each individually
@pytest.mark.parametrize("data, expected_status, expected_error", [
    # Case 1: Missing email
    ({"password":"pass"}, 400, "Missing either email or password"),
    # Case 2: Missing password
    ({"email":"pass@gmail.com"}, 400, "Missing either email or password"),
    # Case 3: Empty JSON
    ({}, 400,"Missing either email or password"),
    # Case 4: Non-JSON body
    (67, 400, "Request body must be valid JSON"),
])

def test_invalid_json_input_login(test_client, data, expected_status, expected_error):
    """
    GIVEN missing user data fields
    WHEN logging in
    THEN throw an error for missing data
    """
    response = test_client.post('/login', json=data)

    assert response.status_code == expected_status
    assert expected_error in response.json['error']

def test_invalid_email_login(test_client):
    """
    GIVEN invalid user email
    WHEN logging in
    THEN throw error
    """
    data = {
        "email":"doesnotexist@gmail.com",
        "password":"DNE"
    }

    response = test_client.post('/login', json=data)

    assert response.status_code == 400
    assert 'Nonexisting user, please sign up first' in response.json['error']

def test_invalid_password_login(test_client, make_user):
    """
    GIVEN invalid user password
    WHEN logging in
    THEN throw incorrect password error
    """
    make_user('LogMeIn', 'LogMeIn@gmail.com', 'LogMeIn')
    data = {
        "email":"LogMeIn@gmail.com",
        "password":"WrongPassword"
    }

    response = test_client.post('/login', json=data)

    assert response.status_code == 400
    assert "Incorrect password, please try again" in response.json['error']

def test_logout(test_client, make_user):
    """
    GIVEN logged in user credentials
    WHEN accessing logout route
    THEN successfully log user out
    """
    make_user()
    login_info = {
        "email":"easy@email.com",
        "password":"easy"
    }

    login_response = test_client.post('/login', json=login_info)
    assert login_response.status_code == 201

    logout_response = test_client.get('/logout')

    assert logout_response.status_code == 201
    assert "Successful logout" in logout_response.json['message']

# Need Forgot-Password, Reset-Password tests