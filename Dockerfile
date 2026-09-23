FROM python:3.13-alpine3.24

#Se algum comando do pipe falhar, o shell retornará um erro e o processo será interrompido.
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

ENV POETRY_VERSION=2.4.2 \ 
PATH="/root/.local/bin:$PATH"

RUN apk add curl=8.22.0-r0\
    --no-cache &&\
    rm -rf /var/cache/apk/* &&\
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Instala as dependências do projeto com Poetry.
COPY pyproject.toml poetry.lock ./

RUN poetry install\ 
    --without dev  \ 
    --no-root       \
    --no-ansi

COPY . .

CMD ["poetry", "run", "fastapi", "dev", "car_api/app.py", "--host", "0.0.0.0"]
