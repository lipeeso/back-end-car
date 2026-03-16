from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, String, Integer, Text, Numeric
from datetime import datetime
from typing import Optional
from car_api.models import Base


class Brand(Base):
    __tablename__ = 'brands'

    id: Mapped[int] = mapped_column(primary_key=True)   
    name: Mapped[str] = mapped_column(String(50),unique=True) #-> define o limite de caracter a 50 e o unique para não permitir repetição
    is_active: Mapped[bool] = mapped_column(default=True) #-> define o valor padrão como True
    description: Mapped[Optional[str]] = mapped_column(Text, default=None) #-> Text não tem limite de caracteres, 
    
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )