from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func
from sqlalchemy.orm import selectinload #-> Faz carregamento de dados de outras tabelas
from typing import List, Optional

from car_api.core.database import get_session   
from car_api.models.cars import Car, Brand, FuelType, TransmissionType
from car_api.models.users import User
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


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=CarListSchema,
    summary='Get a list of cars'
)
async def list_cars(
    db: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    search: Optional[str] = Query(None, description="Search term for model or color"),
    is_available: Optional[bool] = Query(None, description="Filter by availability"),
    brand_id: Optional[int] = Query(None, description="Filter by brand ID"),
    owner_id: Optional[int] = Query(None, description="Filter by owner ID"),
    fuel_type: Optional[FuelType] = Query(None, description="Filter by fuel type"),
    transmission_type: Optional[TransmissionType] = Query(None, description="Filter by transmission type"),
    model_year_min: Optional[int] = Query(None, description="Minimum model year"),
    model_year_max: Optional[int] = Query(None, description="Maximum model year"),
    price_min: Optional[float] = Query(None, ge=0, description="Minimum price"),
    price_max: Optional[float] = Query(None, ge=0, description="Maximum price"),
):
    query = select(Car).options(selectinload(Car.brand), selectinload(Car.owner))

    query = query.offset(offset).limit(limit)

    if is_available is not None:
        query = query.where(Car.is_available == is_available)

    if brand_id is not None:
        query = query.where(Car.brand_id == brand_id)

    if owner_id is not None:
        query = query.where(Car.owner_id == owner_id)

    if fuel_type is not None:
        query = query.where(Car.fuel_type == fuel_type)
    
    if transmission_type is not None:
        query = query.where(Car.transmission == transmission_type)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Car.model.ilike(search_filter)) | (Car.plate.ilike(search_filter) | (Car.color.ilike(search_filter)))
        )

    if model_year_min is not None:
        query = query.where(Car.model_year >= model_year_min)

    if model_year_max is not None:
        query = query.where(Car.model_year <= model_year_max)

    if price_min is not None:
        query = query.where(Car.price >= price_min)

    if price_max is not None:
        query = query.where(Car.price <= price_max)

    result = await db.execute(query)

    cars = result.scalars().all()

    return {
        "cars": cars,
        "offset": offset,
        "limit": limit,
    }


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