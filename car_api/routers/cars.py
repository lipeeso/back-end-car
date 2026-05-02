from fastapi import APIRouter, status, HTTPException, Query, Depends
from car_api.core.database import get_session   
from sqlalchemy.ext.asyncio import AsyncSession 
from car_api.models.cars import Car, Brand
from car_api.models.users import User
from sqlalchemy import select, exists, func
from sqlalchemy.orm import selectinload #-> Faz carregamento de dados de outras tabelas
from car_api.schemas.cars import (
    CarListSchema,
    CarPublicSchema,
    CarSchema,
    CarUpdateSchema
)   

router = APIRouter()

@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=CarPublicSchema,
    summary='Create a new car'
)
async def create_car(
    car: CarSchema,
    db: AsyncSession = Depends(get_session)
):
    
    plate_exists = await db.scalar(
        select(exists().where(Car.plate == car.plate))
    )

    if plate_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car with this plate already exists"
        )
    
    brand_exists = await db.scalar(
        select(exists().where(Brand.id == car.brand_id))
    )

    if not brand_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brand not found"
        )
    
    owner_exists = await db.scalar(
        select(exists().where(User.id == car.owner_id))
    )

    if not owner_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner not found"
        )

    db_car = Car(
        model = car.model,
        factory_year = car.factory_year,
        model_year = car.model_year,
        color = car.color,
        plate = car.plate,
        fuel_type = car.fuel_type,
        transmission = car.transmission,
        price = car.price,
        description = car.description,
        is_available = car.is_available,
        brand_id = car.brand_id,
        owner_id = car.owner_id
    )

    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)

    '''Options serve para os extras que não estão na tabela, mas são relacionados a ela, como o brand e o owner '''
    result = await db.execute(
        select(Car)
        .options(selectinload(Car.brand), selectinload(Car.owner))
        .where(Car.id == db_car.id)
    )

    car_with_relations = result.scalar_one() #Pega o primeiro registro encontrado

    return car_with_relations


@router.get(
    path='/{car_id}',
    status_code=status.HTTP_200_OK,
    response_model=CarPublicSchema,
    summary='Get a list of cars'
)
async def get_car(
    car_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Car)
        .options(selectinload(Car.brand), selectinload(Car.owner))
        .where(Car.id == car_id)
    )

    car = result.scalar_one_or_none()
    
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )

    return car


@router.delete(
    path='/{car_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a car'
)
async def delete_car(
    car_id: int,
    db: AsyncSession = Depends(get_session)
):
    car = await db.get(Car, car_id)

    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )

    await db.delete(car)
    await db.commit()

    return None