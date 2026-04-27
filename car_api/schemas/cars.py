from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal
from car_api.models.cars import FuelType, TransmissionType
from car_api.schemas.brands import BrandPublicSchema
from car_api.schemas.users import UserPublicSchema

class CarSchema(BaseModel):
    model: str 
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: FuelType
    transmission: TransmissionType
    price: Decimal
    description: Optional[str] = None
    is_available: Optional[bool] = True
    brand_id: int
    owner_id: int

    @field_validator("model")
    def model_min_length(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Model name must be at least 3 characters long")
        return value.strip()


class CarUpdateSchema(BaseModel):
    model: Optional[str] = None
    factory_year: Optional[int] = None
    model_year: Optional[int] = None
    color: Optional[str] = None
    plate: Optional[str] = None
    fuel_type: Optional[FuelType] = None
    transmission: Optional[TransmissionType] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None
    brand_id: Optional[int] = None
    owner_id: Optional[int] = None

    @field_validator("model")
    def model_min_length(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Model name must be at least 3 characters long")
        return value.strip()

class CarPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    model: str 
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: FuelType
    transmission: TransmissionType
    price: Decimal
    description: Optional[str] = None
    is_available: Optional[bool] = True
    created_at: datetime
    updated_at: datetime
    brand: BrandPublicSchema
    owner: UserPublicSchema

class CarListSchema(BaseModel):
    cars: List[CarPublicSchema]
    offset: int
    limit: int