import pytest
from sqlalchemy import select

from car_api.models import User


@pytest.mark.asyncio
async def test_create_user(session):

    new_user = User(
        username='testuser', password='secret123', email='test@example.com'
    )

    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.email == 'test@example.com')
    )

    user_data = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email,
    }

    assert user_data == {
        'id': 1,
        'username': 'testuser',
        'password': 'secret123',
        'email': 'test@example.com',
    }
