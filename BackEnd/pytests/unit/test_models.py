from app.models import User


def test_new_user():
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed password, and role fields are defined correctly
    '''
    user = User(name='pytester', email='pytests0@gmail.com')
    user.set_password('FlaskIsAwesome')

    assert user.name == 'pytester'
    assert user.email == 'pytests0@gmail.com'
    assert user.password != 'FlaskIsAwesome'
    assert user.check_password('FlaskIsAwesome')

def test_new_user_with_fixture(new_user):
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed password, and role fields are defined correctly
    '''
    assert new_user.name == 'pytester'
    assert new_user.email == 'pytests0@gmail.com'
    assert new_user.password != 'FlaskIsAwesome'
    assert new_user.is_admin == False
    assert new_user.check_password('FlaskIsAwesome')