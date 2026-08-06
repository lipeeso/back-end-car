from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt

from car_api.core.settings import Settings


def test_token_success(client, user, user_data):
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = client.post('/api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0


def test_token_invalid_email(client, user, user_data):
    login_data = {
        'email': 'wrong@example.com',
        'password': user_data['password'],
    }

    response = client.post('/api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid email or password'


def test_token_invalid_password(client, user, user_data):
    login_data = {
        'email': user_data['email'],
        'password': 'wrongpassword',
    }

    response = client.post('/api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid email or password'


def test_refresh_token(client, auth_headers):
    response = client.post('/api/v1/auth/refresh_token', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_refresh_token_without_auth(client):
    response = client.post('/api/v1/auth/refresh_token')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_contains_valid_jwt(client, user, user_data):
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = client.post('/api/v1/auth/token', json=login_data)
    data = response.json()

    settings = Settings()
    payload = jwt.decode(
        data['access_token'],
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    assert 'sub' in payload
    assert payload['sub'] == str(user.id)
    assert 'exp' in payload


def test_token_expired(client, user, user_data):
    settings = Settings()
    expired_token = jwt.encode(
        {
            'sub': str(user.id),
            'exp': datetime.now(timezone.utc) - timedelta(minutes=5),
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    headers = {'Authorization': f'Bearer {expired_token}'}
    response = client.post('/api/v1/auth/refresh_token', headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Token has expired'


def test_token_invalid(client):
    headers = {'Authorization': 'Bearer invalid.token.here'}
    response = client.post('/api/v1/auth/refresh_token', headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid token'


def test_token_missing_sub_claim(client, user):
    settings = Settings()
    token_no_sub = jwt.encode(
        {'exp': 9999999999},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    headers = {'Authorization': f'Bearer {token_no_sub}'}
    response = client.post('/api/v1/auth/refresh_token', headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid token: missing user ID'


def test_token_invalid_sub_type(client, user):
    settings = Settings()
    token_bad_sub = jwt.encode(
        {'sub': 'not_a_number', 'exp': 9999999999},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    headers = {'Authorization': f'Bearer {token_bad_sub}'}
    response = client.post('/api/v1/auth/refresh_token', headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert (
        response.json()['detail']
        == 'Invalid token: user ID must be an integer'
    )


def test_token_user_not_found(client, user):
    settings = Settings()
    token = jwt.encode(
        {'sub': '99999', 'exp': 9999999999},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/v1/auth/refresh_token', headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'User not found'


def test_login_short_password(client, user):
    login_data = {
        'email': 'test@example.com',
        'password': '12345',
    }

    response = client.post('/api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
