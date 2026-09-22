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

def test_add_to_pantry(test_client, make_recipe):
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

@pytest.mark.parametrize("data, expected_status, expected_error", [
    # Case 1: invalid JSON body
    (2, 400, 'Request body must be valid JSON'),
    # Case 2: No ingredients provided
    ({}, 200, "No ingredients provided"),
    # Case 3: No valid ingredient ids provided
    ({'ingredients':[999,9991,92939,19139]}, 400, 'None of the provided ingredients are valid'),
    # Case 4: All ingredients already exist in pantry
    ({'ingredients':[1]}, 200, 'All ingredients are already in your pantry')
])

def test_add_to_pantry_errors(test_client, make_recipe, data, expected_status, expected_error):
    # Add ingredients into DB
    recipe_res = make_recipe()
    assert recipe_res.status_code == 201

    # Add 1 ingredient to pantry
    pantry_info = {
            'ingredients':[1]
        }
    
    res = test_client.post('/pantry', json=pantry_info)
    assert res.status_code == 201

    res = test_client.post('/pantry', json=data)
    assert res.status_code == expected_status
    # searches to res.data need byte encoded strings, but can't apply both b & f to string so used encode()
    assert f'{expected_error}'.encode('utf-8') in res.data

def test_remove_from_pantry(test_client, make_and_add_user_pantry):
    # Add ingredients into DB
    add_res = make_and_add_user_pantry()
    assert add_res.status_code == 201

    # Delete 2 ingredients from pantry
    data = {'ingredients':[1,2]}
    res = test_client.delete('/pantry', json=data)
    assert res.status_code == 200
    assert 'Successfully removed given ingredients from pantry' in res.json['message']

def test_pantry_fixture(make_and_add_user_pantry):
    res = make_and_add_user_pantry()
    assert res.status_code == 201

@pytest.mark.parametrize("data, expected_status, expected_error", [
    # Case 1: Invalid JSON body
    (2, 400, 'Request body must be valid JSON'),
    # Case 2: Empty ingredients
    ({'ingredients':[]}, 200, 'No ingredients provided'),
    # Case 3: Ingredients that don't exist/aren't in pantry
    ({'ingredients':[7,6,9]}, 200, 'Given ingredients do not exist in your pantry'),
    # Case 4: Mix of valid & invalid ingredients
    ({'ingredients':[1,2,999]}, 200, 'Successfully removed given ingredients from pantry')
])
def test__remove_from_pantry_cases(test_client, make_and_add_user_pantry, data, expected_status, expected_error):
    initial_res = make_and_add_user_pantry()
    assert initial_res.status_code == 201

    res = test_client.delete('/pantry', json=data)
    assert res.status_code == expected_status
    assert f'{expected_error}'.encode('utf-8') in res.data

