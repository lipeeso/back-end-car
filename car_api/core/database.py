'''Sessão do banco de dados'''
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from car_api.core.settings import Settings


engine = create_async_engine(Settings().DATABASE_URL) #-> Cria a engine de conexão com o banco de dados usando a URL fornecida nas configurações

'''
expire_on_commit=False -> Impede que a conexão expire após o commit'''

async def get_session():    #-> Cria uma sessão assíncrona para interagir com o banco de dados
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
