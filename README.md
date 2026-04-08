# Car API

API REST para gerenciamento de usuários e da base inicial de carros do projeto `car-api`.

O projeto usa:

- FastAPI
- SQLAlchemy async
- Alembic para migrations
- SQLite com `aiosqlite`
- Pydantic v2 e `pydantic-settings`
- `pwdlib` para hash de senha com Argon2

## Visão geral

Neste momento a aplicação expõe:

- `GET /health_check`
- CRUD parcial de usuários em `/api/v1/users`

A base de dados já possui os modelos:

- `users`
- `brands`
- `cars`

As tabelas de `brands` e `cars` já existem no modelo e nas migrations, mesmo que ainda não haja rotas públicas para elas.

## Requisitos

- Python `3.13`
- Poetry

## Estrutura

```text
back_end_car/
├── car_api/
│   ├── app.py
│   ├── core/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── settings.py
│   ├── models/
│   │   ├── base.py
│   │   ├── cars.py
│   │   └── users.py
│   ├── routers/
│   │   └── users.py
│   └── schemas/
│       └── users.py
├── migrations/
├── alembic.ini
├── pyproject.toml
└── README.md
```

## Configuração

O projeto carrega variáveis de ambiente a partir do arquivo `.env`.

Variável obrigatória:

- `DATABASE_URL`

Exemplo atual do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///car.db
```

## Instalação

1. Instale as dependências:

```bash
poetry install
```

2. Garanta que o arquivo `.env` exista na raiz do projeto e contenha `DATABASE_URL`.

## Banco de dados

O projeto usa Alembic para versionamento do schema.

Aplicar as migrations:

```bash
poetry run alembic upgrade head
```

Criar uma nova migration:

```bash
poetry run alembic revision --autogenerate -m "descricao_da_migration"
```

## Executando a API

Você pode iniciar a aplicação com o FastAPI CLI:

```bash
poetry run fastapi dev car_api/app.py
```

Se preferir, também é possível usar o Uvicorn diretamente:

```bash
poetry run uvicorn car_api.app:app --reload
```

Por padrão, a API fica disponível em:

- `http://127.0.0.1:8000`

Documentação interativa:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### Health check

`GET /health_check`

Resposta:

```json
{ "status": "ok" }
```

### Usuários

Base path: `/api/v1/users`

#### Criar usuário

`POST /api/v1/users/`

Body:

```json
{
  "username": "felipe",
  "email": "felipe@example.com",
  "password": "senha_forte"
}
```

Validações aplicadas:

- `username` precisa ser único
- `email` precisa ser único
- `password` é armazenada com hash

Resposta:

```json
{
  "id": 1,
  "username": "felipe",
  "email": "felipe@example.com"
}
```

#### Listar usuários

`GET /api/v1/users/`

Query params:

- `offset` padrão `0`
- `limit` padrão `100`
- `search` opcional, pesquisa por `username` ou `email`

Resposta:

```json
{
  "users": [],
  "offset": 0,
  "limit": 100
}
```

#### Buscar usuário por ID

`GET /api/v1/users/{user_id}`

Resposta:

```json
{
  "id": 1,
  "username": "felipe",
  "email": "felipe@example.com"
}
```

#### Atualizar usuário

`PUT /api/v1/users/{user_id}`

Observação:

- a rota existe no código, mas ainda está com implementação pendente

#### Remover usuário

`DELETE /api/v1/users/{user_id}`

Resposta:

- `204 No Content`

## Modelos de dados

### `users`

- `id`
- `username`
- `password`
- `email`
- `created_at`
- `update_at`

### `brands`

- `id`
- `name`
- `is_active`
- `description`
- `created_at`
- `updated_at`

### `cars`

- `id`
- `model`
- `factory_year`
- `model_year`
- `color`
- `plate`
- `fuel_type`
- `transmission`
- `price`
- `description`
- `is_available`
- `brand_id`
- `owner_id`
- `created_at`
- `updated_at`

## Regras de negócio já implementadas

- senha de usuário é criptografada antes de salvar
- `username` e `email` não podem se repetir
- `plate` do carro é única e indexada
- relacionamentos entre `User`, `Brand` e `Car` já estão modelados

## Desenvolvimento

Arquivos principais:

- `car_api/app.py` define a aplicação FastAPI e o health check
- `car_api/core/settings.py` carrega variáveis de ambiente
- `car_api/core/database.py` cria a engine e a sessão async
- `car_api/core/security.py` cuida do hash e verificação de senha
- `car_api/routers/users.py` expõe as rotas de usuários

## Testes

Não há suíte de testes automatizada configurada neste momento.

## Licença

Ainda não definida.

