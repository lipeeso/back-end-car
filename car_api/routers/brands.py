from fastapi import APIRouter, status, HTTPException, Query, Depends
from car_api.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from car_api.models.cars import Brand, Car
from sqlalchemy import select, exists, func
from car_api.schemas.brands import(
    BrandListPublicSchema,
    BrandPublicSchema,
    BrandSchema,
    BrandUpdateSchema
)



router = APIRouter()

@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=BrandPublicSchema,
    summary='Create a new brand'
)
async def create_brand(
    brand: BrandSchema,
    db: AsyncSession = Depends(get_session)
):
    brand_exists = await db.scalar(
        select(exists().where(Brand.name == brand.name))
    )

    if brand_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brand already exists"
        )

    db_brand = Brand(
        name = brand.name,
        description = brand.description,
        is_active = brand.is_active
    )

    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)

    return db_brand


@router.delete(
    path='/{brand_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a brand by ID'
)
async def delete_brand(
    brand_id: int,
    db: AsyncSession = Depends(get_session)
):
    brand = await db.get(Brand, brand_id)

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Brand not found'
        )
    
    cars_count = await db.scalar(
        select(func.count()).select_from(Car).where(Car.brand_id == brand_id)
        )

    if cars_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete brand with associated cars'
        )
    
    
    await db.delete(brand)
    await db.commit()

    return None

