# Usa a imagem base do Python 3.13.11 para o ambiente da aplicação.
FROM python:3.13-alpine3.24

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

# Define a versão do Poetry que será instalada no container.
ARG POETRY_VERSION=2.4.2

# Instala o Poetry no ambiente Python do container usando o script oficial.
RUN apk add curl && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

# Adiciona o diretório de binários do Poetry ao PATH para facilitar o uso no container.
ENV PATH="/root/.local/bin:$PATH"

# Define o diretório de trabalho da aplicação dentro do container.
WORKDIR /app

# Copia todo o conteúdo do projeto para o diretório de trabalho.
COPY . .

# Instala as dependências do projeto com Poetry.
RUN poetry install

# Executa a aplicação pela tarefa definida no projeto.
CMD ["poetry", "run", "task", "run"]
