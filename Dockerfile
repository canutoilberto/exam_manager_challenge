# Dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copiar arquivos do projeto e instalar dependências com Poetry
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app/

# Coleta de arquivos estáticos (se necessário)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando para iniciar o servidor (usando uvicorn)
CMD ["uvicorn", "exam_manager.asgi:application", "--host", "0.0.0.0", "--port", "8000"]