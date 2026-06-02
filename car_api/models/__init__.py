"""dunder init
Para facilitar a migração"""

from car_api.models.base import Base
from car_api.models.cars import Brand, Car
from car_api.models.users import User

__all__ = ['Base', 'User', 'Brand', 'Car']
