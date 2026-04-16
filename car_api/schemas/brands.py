from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime




class BrandSchema(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

    @field_validator("name")
    def name_min_length(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Brand name must be at least 3 characters long")
        return value.strip()


class BrandUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    def name_min_length(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Brand name must be at least 3 characters long")
        return value.strip()
        
class BrandPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    name: str
    is_active: bool 
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

class BrandListPublicSchema(BaseModel):
    brands: List[BrandPublicSchema]
    offset: int
    limit: int
