import asyncio
from http import HTTPStatus

from car_api.models import Car


def test_create_car(client, car_data, auth_headers):
    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['model'] == car_data['model']
    assert data['color'] == car_data['color']
    assert data['plate'] == car_data['plate']
    assert 'id' in data
    assert 'brand' in data
    assert 'owner' in data
    assert data['brand']['name'] == 'Toyota'


def test_create_car_duplicate_plate(client, car, car_data, auth_headers):
    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Car with this plate already exists'


def test_create_car_brand_not_found(client, user, auth_headers):
    car_data = {
        'model': 'Corolla',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'White',
        'plate': 'XYZ9W99',
        'fuel_type': 'flex',
        'transmission': 'automatic',
        'price': 150000.00,
        'brand_id': 999,
        'owner_id': user.id,
    }

    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Brand not found'


def test_create_car_owner_not_found(client, brand, auth_headers):
    car_data = {
        'model': 'Corolla',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'White',
        'plate': 'XYZ9W99',
        'fuel_type': 'flex',
        'transmission': 'automatic',
        'price': 150000.00,
        'brand_id': brand.id,
        'owner_id': 999,
    }

    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Owner not found'


def test_create_car_without_auth(client, car_data):
    response = client.post('/api/v1/cars/', json=car_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_car_by_id(client, car, auth_headers):
    response = client.get(f'/api/v1/cars/{car.id}', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == car.id
    assert data['model'] == car.model
    assert 'brand' in data
    assert 'owner' in data


def test_get_car_not_found(client, auth_headers):
    response = client.get('/api/v1/cars/999', headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Car not found'


def test_get_car_not_owner(client, car, second_user_auth_headers):
    response = client.get(
        f'/api/v1/cars/{car.id}', headers=second_user_auth_headers
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert (
        response.json()['detail']
        == 'You do not have permission to access this resource'
    )


def test_list_cars(client, car, auth_headers):
    response = client.get('/api/v1/cars/', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'cars' in data
    assert len(data['cars']) >= 1
    assert data['offset'] == 0
    assert data['limit'] == 10


def test_list_cars_with_search(client, car, auth_headers):
    response = client.get('/api/v1/cars/?search=Corolla', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_filter_by_brand(client, car, brand, auth_headers):
    response = client.get(
        f'/api/v1/cars/?brand_id={brand.id}', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_filter_by_owner(client, car, user, auth_headers):
    response = client.get(
        f'/api/v1/cars/?owner_id={user.id}', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_filter_by_availability(client, car, auth_headers):
    response = client.get(
        '/api/v1/cars/?is_available=true', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert all(c['is_available'] for c in data['cars'])


def test_list_cars_filter_by_fuel_type(client, car, auth_headers):
    response = client.get('/api/v1/cars/?fuel_type=flex', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_filter_by_transmission(client, car, auth_headers):
    response = client.get(
        '/api/v1/cars/?transmission_type=automatic',
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_filter_by_year_range(client, car, auth_headers):
    response = client.get(
        '/api/v1/cars/?model_year_min=2020&model_year_max=2025',
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_filter_by_price_range(client, car, auth_headers):
    response = client.get(
        '/api/v1/cars/?price_min=100000&price_max=200000',
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['cars']) >= 1


def test_list_cars_with_pagination(client, car, auth_headers):
    response = client.get(
        '/api/v1/cars/?offset=0&limit=1', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['limit'] == 1


def test_update_car(client, car, auth_headers):
    update_data = {
        'model': 'Updated Corolla',
        'color': 'Black',
        'price': 160000.00,
    }

    response = client.put(
        f'/api/v1/cars/{car.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['model'] == 'Updated Corolla'
    assert data['color'] == 'Black'
    assert 'brand' in data
    assert 'owner' in data


def test_update_car_not_found(client, auth_headers):
    response = client.put(
        '/api/v1/cars/999',
        json={'model': 'Updated'},
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_car_not_owner(client, car, second_user_auth_headers):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        json={'model': 'Updated'},
        headers=second_user_auth_headers,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_car_duplicate_plate(
    client, car, brand, user, auth_headers, session
):
    other_car = Car(
        model='Civic',
        factory_year=2023,
        model_year=2024,
        color='Black',
        plate='XYZ9W99',
        fuel_type='flex',
        transmission='automatic',
        price=120000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(other_car)

    asyncio.get_event_loop().run_until_complete(session.commit())

    update_data = {'plate': 'XYZ9W99'}

    response = client.put(
        f'/api/v1/cars/{car.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Car with this plate already exists'


def test_update_car_brand_not_found(client, car, auth_headers):
    update_data = {'brand_id': 999}

    response = client.put(
        f'/api/v1/cars/{car.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Brand not found'


def test_update_car_owner_not_found(client, car, auth_headers):
    update_data = {'owner_id': 999}

    response = client.put(
        f'/api/v1/cars/{car.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Owner not found'


def test_delete_car(client, car, auth_headers):
    response = client.delete(f'/api/v1/cars/{car.id}', headers=auth_headers)

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_car_not_found(client, auth_headers):
    response = client.delete('/api/v1/cars/999', headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_car_not_owner(client, car, second_user_auth_headers):
    response = client.delete(
        f'/api/v1/cars/{car.id}', headers=second_user_auth_headers
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_list_cars_without_auth(client):
    response = client.get('/api/v1/cars/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_car_invalid_plate(client, brand, user, auth_headers):
    car_data = {
        'model': 'Corolla',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'White',
        'plate': 'AB',
        'fuel_type': 'flex',
        'transmission': 'automatic',
        'price': 150000.00,
        'brand_id': brand.id,
        'owner_id': user.id,
    }

    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_car_invalid_year(client, brand, user, auth_headers):
    car_data = {
        'model': 'Corolla',
        'factory_year': 1800,
        'model_year': 2024,
        'color': 'White',
        'plate': 'ABC1D23',
        'fuel_type': 'flex',
        'transmission': 'automatic',
        'price': 150000.00,
        'brand_id': brand.id,
        'owner_id': user.id,
    }

    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_car_zero_price(client, brand, user, auth_headers):
    car_data = {
        'model': 'Corolla',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'White',
        'plate': 'ABC1D23',
        'fuel_type': 'flex',
        'transmission': 'automatic',
        'price': 0,
        'brand_id': brand.id,
        'owner_id': user.id,
    }

    response = client.post(
        '/api/v1/cars/', json=car_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
