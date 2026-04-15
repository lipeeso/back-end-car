from fastapi import APIRouter, status, HTTPException, Query, Depends
from car_api.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from car_api.models.cars import Brand
from sqlalchemy import select, exists
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