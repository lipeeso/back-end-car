from http import HTTPStatus


def test_token_success(client, user, user_data):
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = client.post('api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0
