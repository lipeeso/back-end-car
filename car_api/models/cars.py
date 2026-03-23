from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, String, Integer, Text, Numeric
from datetime import datetime
from decimal import Decimal
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

class Car(Base):
    __tablename__="cars"

    id: Mapped[int] = mapped_column(primary_key=True)

    model: Mapped[str] = mapped_column(String(100)) #-> define o limite de caracter a 100
    factory_year: Mapped[int] = mapped_column(Integer) #-> define o tipo como inteiro
    model_year: Mapped[int] = mapped_column(Integer)
    color: Mapped[str] = mapped_column(String(25))
    plate: Mapped[str] = mapped_column(String(10), unique=True, index=True) #-> index=True para criar um índice no campo, o que melhora a performance nas querys

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2)) #-> define o tipo como decimal com 10 dígitos no total e 2 casas decimais
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    is_available: Mapped[bool] = mapped_column(default=True)
    
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

