# Exam Manager

Sistema de gerenciamento de provas desenvolvido com Django.

## Requisitos

- Python >= 3.10
- Poetry para gerenciamento de dependências
- Redis para cache e Celery
- Elasticsearch para busca

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
poetry install
```

3. Configure as variáveis de ambiente
4. Execute as migrações:

```bash
poetry run python manage.py migrate
```

5. Inicie o servidor:

```bash
poetry run python manage.py runserver
```

## Funcionalidades

- Gerenciamento de provas
- Sistema de questões e alternativas
- Inscrições em provas
- Correção automática
- Cache com Redis
- Busca com Elasticsearch
