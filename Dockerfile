# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

WORKDIR /app

# Instalar dependências do sistema e Poetry
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry \
    && poetry config virtualenvs.create false

# Copiar arquivos do projeto e instalar dependências
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-root --without dev

# Copiar o resto do código
COPY . .

# Criar diretório para arquivos estáticos
RUN mkdir -p staticfiles && python manage.py collectstatic --noinput

EXPOSE 8000

# Comando para iniciar o servidor (usando uvicorn)
CMD ["uvicorn", "exam_manager.asgi:application", "--host", "0.0.0.0", "--port", "8000"]