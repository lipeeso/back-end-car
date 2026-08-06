import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.app import app
from car_api.core.database import get_session
from car_api.core.security import create_access_token, get_password_hash
from car_api.models import Base, Brand, Car, User


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(session):

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'secret123',
        'email': 'test@example.com',
    }


@pytest_asyncio.fixture
async def user(session, user_data):
    hashed_password = get_password_hash(user_data['password'])

    db_user = User(
        username=user_data['username'],
        password=hashed_password,
        email=user_data['email'],
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest_asyncio.fixture
async def second_user(session):
    hashed_password = get_password_hash('secret456')

    db_user = User(
        username='testuser2',
        password=hashed_password,
        email='test2@example.com',
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest_asyncio.fixture
async def third_user(session):
    hashed_password = get_password_hash('secret789')

    db_user = User(
        username='testuser3',
        password=hashed_password,
        email='test3@example.com',
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest.fixture
def access_token(user):
    token = create_access_token({'sub': str(user.id)})
    return token


@pytest.fixture
def auth_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def second_user_token(second_user):
    return create_access_token({'sub': str(second_user.id)})


@pytest.fixture
def second_user_auth_headers(second_user_token):
    return {'Authorization': f'Bearer {second_user_token}'}


@pytest.fixture
def brand_data():
    return {
        'name': 'Toyota',
        'description': 'Japanese automaker',
        'is_active': True,
    }


@pytest_asyncio.fixture
async def brand(session, brand_data):
    db_brand = Brand(
        name=brand_data['name'],
        description=brand_data['description'],
        is_active=brand_data['is_active'],
    )

    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)
    return db_brand


@pytest_asyncio.fixture
async def second_brand(session):
    db_brand = Brand(
        name='Honda',
        description='Japanese automaker',
        is_active=True,
    )

    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)
    return db_brand


@pytest.fixture
def car_data(brand, user):
    return {
        'model': 'Corolla',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'White',
        'plate': 'ABC1D23',
        'fuel_type': 'flex',
        'transmission': 'automatic',
        'price': 150000.00,
        'description': 'Sedan',
        'is_available': True,
        'brand_id': brand.id,
        'owner_id': user.id,
    }


@pytest_asyncio.fixture
async def car(session, brand, user):
    db_car = Car(
        model='Corolla',
        factory_year=2023,
        model_year=2024,
        color='White',
        plate='ABC1D23',
        fuel_type='flex',
        transmission='automatic',
        price=150000.00,
        description='Sedan',
        is_available=True,
        brand_id=brand.id,
        owner_id=user.id,
    )

    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)
    return db_car
