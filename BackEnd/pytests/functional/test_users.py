
def test_user_homepage(test_client, make_user):
    '''
    GIVEN a logged in user
    WHEN a visits their homepage
    THEN recieve a hello message
    '''
    make_user(name='PyTester', email="easy@email.com", password="Pie")
    login_info = {"email":"easy@email.com", "password":"Pie"}
    login_response = test_client.post('/login', json=login_info)
    assert login_response.status_code == 201

    response = test_client.get('/user')
    assert response.status_code == 200
    assert 'hello PyTester' in response.json['message']

def test_user_recipes(test_client, make_user):
    """
    GIVEN a user with saved recipes
    WHEN accessing a user's saved recipes page
    THEN display said user's recipes

    NOTE: Just tests if route runs through code. Whether recipes show correctly is not tested
    """
    make_user()
    login_info = {"email":"easy@email.com", "password":"easy"}
    login_res = test_client.post('/login', json=login_info)

    assert login_res.status_code == 201

    res = test_client.get('/user/recipes')

    assert res.status_code == 200
    assert 'total' in res.json
    assert 'saved recipes' in res.json
