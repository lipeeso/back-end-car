import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.app import app
from car_api.core.database import get_session
from car_api.core.security import create_access_token, get_password_hash
from car_api.models import Base, User


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
    await session.refresh(db_user)  # atualiza o obj
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
