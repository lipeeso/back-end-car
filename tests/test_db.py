import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from car_api.models import Brand, Car, User


@pytest.mark.asyncio
async def test_tables_exist(session):
    result = await session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    )
    tables = [row[0] for row in result.fetchall()]

    assert 'users' in tables
    assert 'brands' in tables
    assert 'cars' in tables


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

    assert user.id == 1
    assert user.username == 'testuser'
    assert user.password == 'secret123'
    assert user.email == 'test@example.com'


@pytest.mark.asyncio
async def test_create_brand(session):
    brand = Brand(
        name='Toyota', description='Japanese automaker', is_active=True
    )

    session.add(brand)
    await session.commit()

    db_brand = await session.scalar(
        select(Brand).where(Brand.name == 'Toyota')
    )

    assert db_brand.id == 1
    assert db_brand.name == 'Toyota'
    assert db_brand.is_active is True
    assert db_brand.description == 'Japanese automaker'


@pytest.mark.asyncio
async def test_create_car_with_relationships(session):
    user = User(
        username='testuser', password='secret123', email='test@example.com'
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    brand = Brand(name='Toyota', description='Japanese', is_active=True)
    session.add(brand)
    await session.commit()
    await session.refresh(brand)

    car = Car(
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

    session.add(car)
    await session.commit()
    await session.refresh(car)

    assert car.id == 1
    assert car.brand_id == brand.id
    assert car.owner_id == user.id
    assert car.model == 'Corolla'


@pytest.mark.asyncio
async def test_user_unique_email(session):
    user1 = User(username='user1', password='pass1', email='same@example.com')
    session.add(user1)
    await session.commit()

    user2 = User(username='user2', password='pass2', email='same@example.com')
    session.add(user2)

    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_user_unique_username(session):
    user1 = User(username='sameuser', password='pass1', email='a@example.com')
    session.add(user1)
    await session.commit()

    user2 = User(username='sameuser', password='pass2', email='b@example.com')
    session.add(user2)

    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_brand_unique_name(session):
    brand1 = Brand(name='Toyota', is_active=True)
    session.add(brand1)
    await session.commit()

    brand2 = Brand(name='Toyota', is_active=True)
    session.add(brand2)

    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_car_unique_plate(session):
    user = User(username='user1', password='pass1', email='a@example.com')
    session.add(user)
    await session.commit()
    await session.refresh(user)

    brand = Brand(name='Toyota', is_active=True)
    session.add(brand)
    await session.commit()
    await session.refresh(brand)

    car1 = Car(
        model='Corolla',
        factory_year=2023,
        model_year=2024,
        color='White',
        plate='ABC1D23',
        fuel_type='flex',
        transmission='automatic',
        price=150000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car1)
    await session.commit()

    car2 = Car(
        model='Civic',
        factory_year=2023,
        model_year=2024,
        color='Black',
        plate='ABC1D23',
        fuel_type='flex',
        transmission='automatic',
        price=120000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car2)

    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_delete_user(session):
    user = User(
        username='testuser', password='secret123', email='test@example.com'
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    await session.delete(user)
    await session.commit()

    result = await session.scalar(
        select(User).where(User.email == 'test@example.com')
    )
    assert result is None


@pytest.mark.asyncio
async def test_delete_brand(session):
    brand = Brand(name='Toyota', is_active=True)
    session.add(brand)
    await session.commit()
    await session.refresh(brand)

    await session.delete(brand)
    await session.commit()

    result = await session.scalar(select(Brand).where(Brand.name == 'Toyota'))
    assert result is None
