import pytest

def test_get_pantry(test_client, make_user):
    """
    GIVEN a logged in user
    WHEN accessing user's pantry
    THEN return all logged ingredients in pantry
    """
    make_user()
    login_info = {'email':'easy@email.com', 'password':'easy'}
    login_res = test_client.post('/login', json=login_info)
    assert login_res.status_code == 201

    res = test_client.get('/pantry')
    assert res.status_code == 201
    assert b'pantry' in res.data

def test_add_to_pantry(test_client, make_recipe, capsys):
    """
    GIVEN a logged in user and ingredient id
    WHEN accessing add_to_user_pantry
    THEN successfully add ingredient to user pantry
    """
    # Add ingredients into DB
    recipe_res = make_recipe()
    assert recipe_res.status_code == 201

    pantry_info = {
        'ingredients':[1,2,3]
    }

    res = test_client.post('/pantry', json=pantry_info)
    pantry_display = test_client.get('/pantry')

    assert pantry_display.status_code == 201
    assert res.status_code == 201
    assert 'Successfully added 3 ingredients into User Pantry' in res.json['message']
