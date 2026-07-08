# Estrutura do Projeto

Abaixo está uma visão geral da estrutura de pastas e arquivos do projeto:

```text
/
├── car_api/
│   ├── core/      # Configurações do banco, segurança e app
│   ├── models/    # Definição dos modelos ORM (SQLAlchemy)
│   ├── routers/   # Definição dos endpoints da API
│   ├── schemas/   # Definição dos esquemas (Pydantic)
│   └── app.py     # Ponto de entrada da aplicação
├── migrations/    # Migrações do banco de dados (Alembic)
├── tests/         # Testes automatizados
├── pyproject.toml # Gerenciador de dependências e ferramentas (Poetry)
└── mkdocs.yml     # Configuração da documentação
```
