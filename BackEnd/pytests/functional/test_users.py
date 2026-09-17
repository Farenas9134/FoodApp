from app.models import User

def test_new_user(test_client, make_user):
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed password, and attached fields are defined correctly
    '''
    new_user = make_user(name='user1', email='user1@gmail.com')
    assert new_user.name == 'user1'
    assert new_user.email == 'user1@gmail.com'
    assert new_user.password != 'FlaskIsAwesome'
    assert new_user.check_password('FlaskIsAwesome')
    assert new_user.is_admin == False

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
    assert response.json['message'] == 'User created successfully'
