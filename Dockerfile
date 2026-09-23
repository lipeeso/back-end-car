FROM python:3.13-alpine3.24

#Se algum comando do pipe falhar, o shell retornará um erro e o processo será interrompido.
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

ENV POETRY_VERSION=2.4.2 \ 
PATH="/root/.local/bin:$PATH"

RUN apk add curl=8.22.0-r0\
    --no-cache &&\
    rm -rf /var/cache/apk/* &&\
    curl -sSL https://install.python-poetry.org | python3 -

# Define o diretório de trabalho da aplicação dentro do container.
WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Instala as dependências do projeto com Poetry.
RUN poetry install\ 
    --without dev  \ 
    --no-root       \
    --no-ansi


# Copia todo o conteúdo do projeto para o diretório de trabalho.
COPY . .

# Executa a aplicação pela tarefa definida no projeto.
CMD ["poetry", "run", "fastapi", "dev", "car_api/app.py", "--host", "0.0.0.0"]
