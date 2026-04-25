from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal

class CarSchema(BaseModel):
    model: str 
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: str
    transmission: str
    price: Decimal
    description: Optional[str] = None
    is_available: Optional[bool] = True

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
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None

    @field_validator("model")
    def model_min_length(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Model name must be at least 3 characters long")
        return value.strip()

class CarPublicSchema(BaseModel):
    id: int
    model: str 
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: str
    transmission: str
    price: Decimal
    description: Optional[str] = None
    is_available: bool
    created_at: datetime
    updated_at: datetime

class CarListSchema(BaseModel):
    cars: List[CarPublicSchema]
    offset: int
    limit: int