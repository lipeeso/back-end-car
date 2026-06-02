from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import func  # -> função de banco de dados
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_api.models import Base

if TYPE_CHECKING:
    from car_api.models import Car


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    update_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    cars: Mapped[List['Car']] = relationship(
        'Car', back_populates='owner'
    )  # -> define o relacionamento com a tabela cars, e o back_populates para definir o nome do atributo na classe Car
