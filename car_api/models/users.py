from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import func #-> função de banco de dados
from sqlalchemy.orm import mapped_column, Mapped, relationship
from car_api.models import Base

if TYPE_CHECKING:
    from car_api.models import Car

class User(Base):
    __tablename__ = 'users' # -> Nome da tabela que vai ser criado

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] #-> não tem uma propriedade especial no campo então pode deixar assim
    email: Mapped[str] = mapped_column(unique=True)
    update_at : Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )
    created_at : Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    cars: Mapped[List['Car']] = relationship("Car", back_populates="owner") #-> define o relacionamento com a tabela cars, e o back_populates para definir o nome do atributo na classe Car