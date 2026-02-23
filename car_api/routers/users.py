from fastapi import APIRouter, status


router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK)
async def list_users():
     return {
        'users': [
            {
                'id': 1,
                'email': 'pycodebr@gmail.com',
            },
            {
                'id': 2,
                'email': 'joao@gmail.com',
            },
            {
                'id': 3,
                'email': 'mario@gmail.com',
            },
        ]
    }
