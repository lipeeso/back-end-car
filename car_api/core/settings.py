'''Configurações globais'''
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):   #-> Vai carregar todas as variaveis de ambientes do projeto
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str


