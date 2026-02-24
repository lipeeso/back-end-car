from fastapi import APIRouter, status

from car_api.schemas.users import UserListPublicSchema

router = APIRouter()

@router.get(
    path='/',
    status_code=status.HTTP_200_OK, 
    response_model=UserListPublicSchema
)
async def list_users():
     return {
        'users': [
            {
                'id': 1,
                'username': 'pycodebr',
                'email': 'pycodebr@gmail.com',
            },
            {
                'id': 2,
                'username': 'joao',
                'email': 'joao@gmail.com',
            },
            {
                'id': 3,
                'username': 'mario',
                'email': 'mario@gmail.com',
            },
        ]
    }
