from http import HTTPStatus


def test_create_brand(client, brand_data, auth_headers):
    response = client.post(
        '/api/v1/brands/', json=brand_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == brand_data['name']
    assert data['description'] == brand_data['description']
    assert data['is_active'] is True
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data


def test_create_brand_duplicate_name(client, brand, brand_data, auth_headers):
    response = client.post(
        '/api/v1/brands/', json=brand_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Brand already exists'


def test_create_brand_without_auth(client, brand_data):
    response = client.post('/api/v1/brands/', json=brand_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_brand_short_name(client, auth_headers):
    data = {'name': 'AB', 'description': 'Short'}

    response = client.post('/api/v1/brands/', json=data, headers=auth_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_brands(client, brand, auth_headers):
    response = client.get('/api/v1/brands/', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'brands' in data
    assert len(data['brands']) >= 1
    assert data['offset'] == 0
    assert data['limit'] == 100


def test_list_brands_with_search(client, brand, second_brand, auth_headers):
    response = client.get('/api/v1/brands/?search=Honda', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['brands']) == 1
    assert data['brands'][0]['name'] == 'Honda'


def test_list_brands_filter_active(client, brand, auth_headers):
    response = client.get(
        '/api/v1/brands/?is_active=true', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert all(b['is_active'] for b in data['brands'])


def test_list_brands_filter_inactive(client, brand, auth_headers):
    response = client.get(
        '/api/v1/brands/?is_active=false', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['brands']) == 0


def test_list_brands_with_pagination(
    client, brand, second_brand, auth_headers
):
    response = client.get(
        '/api/v1/brands/?offset=0&limit=1', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['brands']) == 1
    assert data['limit'] == 1


def test_get_brand_by_id(client, brand, auth_headers):
    response = client.get(f'/api/v1/brands/{brand.id}', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == brand.id
    assert data['name'] == brand.name


def test_get_brand_not_found(client, auth_headers):
    response = client.get('/api/v1/brands/999', headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Brand not found'


def test_update_brand(client, brand, auth_headers):
    update_data = {
        'name': 'Updated Toyota',
        'description': 'Updated description',
        'is_active': False,
    }

    response = client.put(
        f'/api/v1/brands/{brand.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['name'] == 'Updated Toyota'
    assert data['description'] == 'Updated description'
    assert data['is_active'] is False


def test_update_brand_not_found(client, auth_headers):
    response = client.put(
        '/api/v1/brands/999',
        json={'name': 'Updated'},
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_brand_duplicate_name(
    client, brand, second_brand, auth_headers
):
    update_data = {'name': second_brand.name}

    response = client.put(
        f'/api/v1/brands/{brand.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Brand name already exists'


def test_update_brand_partial(client, brand, auth_headers):
    update_data = {'description': 'Only description updated'}

    response = client.put(
        f'/api/v1/brands/{brand.id}',
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['description'] == 'Only description updated'
    assert data['name'] == brand.name


def test_delete_brand(client, brand, auth_headers):
    response = client.delete(
        f'/api/v1/brands/{brand.id}', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_brand_not_found(client, auth_headers):
    response = client.delete('/api/v1/brands/999', headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Brand not found'


def test_delete_brand_with_cars(client, brand, car, auth_headers):
    response = client.delete(
        f'/api/v1/brands/{brand.id}', headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.json()['detail'] == 'Cannot delete brand with associated cars'
    )


def test_list_brands_without_auth(client):
    response = client.get('/api/v1/brands/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
