from fastapi import APIRouter, status, HTTPException, Query, Depends
from typing import List, Optional
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


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=BrandListPublicSchema,
    summary="Get a list of all brands",
)
async def list_brands(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of items"),
    search: Optional[str] = Query(None, description="Search term for brand name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_session),
):

    query = select(Brand)

    if search:
        search_filter = f"%{search}%"
        query = query.where(Brand.name.ilike(search_filter))

    if is_active is not None:
        query = query.where(Brand.is_active == is_active)

    query.offset(offset).limit(limit)
    result = await db.execute(query)
    brands = result.scalars().all()

    return {"brands": brands, "offset": offset, "limit": limit}


@router.get(
    path='/{brand_id}',
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary='Get a brand by ID'
)
async def get_brand(
    brand_id: int,
    db: AsyncSession = Depends(get_session)
):
    brand = await db.get(Brand, brand_id)

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Brand not found'
        )

    return brand

@router.put(
    path='/{brand_id}',
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary='Update a brand by ID'
)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdateSchema,
    db: AsyncSession = Depends(get_session)
):
    brand = await db.get(Brand, brand_id)

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Brand not found'
        )
    
    brand_update = brand_update.model_dump(exclude_unset=True)

    if "name" in brand_update:
        name_exists = await db.scalar(
            select(
                exists().where((Brand.name == brand_update['name']) & (Brand.id != brand_id))
            )
        )

        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Brand name already exists'
            )
        
    if "description" in brand_update:
        brand.description = brand_update["description"]

    if "is_active" in brand_update:
        brand.is_active = brand_update["is_active"]

    for key, value in brand_update.items():
        setattr(brand, key, value)
    
    await db.commit()
    await db.refresh(brand)
    return brand


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
