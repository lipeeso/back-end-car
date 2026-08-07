from http import HTTPStatus


def test_create_user(client, user_data):
    response = client.post('/api/v1/users/', json=user_data)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['username'] == user_data['username']
    assert data['email'] == user_data['email']
    assert 'id' in data
    assert 'created_at' in data
    assert 'update_at' in data
    assert 'password' not in data


def test_create_user_duplicate_username(client, user, user_data):
    new_data = {
        'username': user_data['username'],
        'email': 'other@example.com',
        'password': 'secret123',
    }

    response = client.post('/api/v1/users/', json=new_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_create_user_duplicate_email(client, user, user_data):
    new_data = {
        'username': 'otheruser',
        'email': user_data['email'],
        'password': 'secret123',
    }

    response = client.post('/api/v1/users/', json=new_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_list_users(client, user, auth_headers):
    response = client.get('/api/v1/users/', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'users' in data
    assert len(data['users']) >= 1
    assert data['offset'] == 0
    assert data['limit'] == 100


def test_list_users_with_search(client, user, second_user, auth_headers):
    response = client.get(
        '/api/v1/users/?search=testuser2', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['users']) == 1
    assert data['users'][0]['username'] == 'testuser2'


def test_list_users_with_pagination(
    client, user, second_user, third_user, auth_headers
):
    response = client.get(
        '/api/v1/users/?offset=0&limit=2', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['users']) == 2
    assert data['limit'] == 2


def test_get_user_by_id(client, user, auth_headers):
    response = client.get(f'/api/v1/users/{user.id}', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == user.id
    assert data['username'] == user.username
    assert data['email'] == user.email


def test_get_user_not_found(client, auth_headers):
    response = client.get('/api/v1/users/999', headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_update_user(client, user, auth_headers):
    update_data = {
        'username': 'updateduser',
        'email': 'updated@example.com',
    }

    response = client.put(
        f'/api/v1/users/{user.id}', json=update_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['username'] == 'updateduser'
    assert data['email'] == 'updated@example.com'


def test_update_user_password(client, user, auth_headers):
    update_data = {'password': 'newsecret123'}

    response = client.put(
        f'/api/v1/users/{user.id}', json=update_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_not_found(client, auth_headers):
    response = client.put(
        '/api/v1/users/999',
        json={'username': 'updated'},
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_duplicate_username(
    client, user, second_user, auth_headers
):
    update_data = {'username': second_user.username}

    response = client.put(
        f'/api/v1/users/{user.id}', json=update_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_update_user_duplicate_email(client, user, second_user, auth_headers):
    update_data = {'email': second_user.email}

    response = client.put(
        f'/api/v1/users/{user.id}', json=update_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_delete_user(client, user, auth_headers):
    response = client.delete(f'/api/v1/users/{user.id}', headers=auth_headers)

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client, auth_headers):
    response = client.delete('/api/v1/users/999', headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_list_users_without_auth(client):
    response = client.get('/api/v1/users/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_user_invalid_email(client):
    data = {
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'secret123',
    }

    response = client.post('/api/v1/users/', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_short_password(client):
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '12345',
    }

    response = client.post('/api/v1/users/', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_short_username(client):
    data = {
        'username': 'ab',
        'email': 'test@example.com',
        'password': 'secret123',
    }

    response = client.post('/api/v1/users/', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
