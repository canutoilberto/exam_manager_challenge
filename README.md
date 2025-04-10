# Exam Manager

Sistema de gerenciamento de provas e exames.

## Configuração do Ambiente

### Opção 1: Usando Scripts de Configuração Automática (Recomendado)

#### No Linux/Mac:

```bash
# Execute o script de configuração
chmod +x scripts/setup_dev.sh
./scripts/setup_dev.sh
```

#### No Windows:

```powershell
# Execute o script de configuração
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup_dev.ps1
```

### Opção 2: Usando Poetry

1. Instale o Poetry seguindo as instruções em https://python-poetry.org/docs/#installation

2. Clone o repositório e acesse a pasta do projeto:

```bash
git clone <repo-url>
cd exam_manager
```

3. Instale as dependências usando Poetry:

```bash
poetry install
```

4. Ative o ambiente virtual:

```bash
# Para Poetry 1.x
poetry shell

# Para Poetry 2.x
poetry env activate
```

5. Execute as migrações:

```bash
poetry run python manage.py migrate
```

6. Inicie o servidor:

```bash
poetry run python manage.py runserver
```

### Opção 3: Usando venv e pip

1. Clone o repositório e acesse a pasta do projeto:

```bash
git clone <repo-url>
cd exam_manager
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute as migrações:

```bash
python manage.py migrate
```

6. Inicie o servidor:

```bash
python manage.py runserver
```

## Verificação de Dependências

Para verificar se todas as dependências estão instaladas corretamente:

```bash
python scripts/check_dependencies.py
```

## Dependências Principais

- Django 5.0+
- django-ninja
- django-celery-beat
- django-redis
- django-elasticsearch-dsl
- Celery
- Redis

## Estrutura do Projeto

- `apps/provas/`: Aplicativo principal para gerenciamento de provas
- `exam_manager/`: Configurações do projeto Django
- `docker-compose.yml`: Configuração para execução com Docker
- `scripts/`: Scripts úteis para configuração e manutenção do projeto

## Executando com Docker

```bash
docker-compose up -d
```

## API Endpoints

A documentação da API está disponível em `/api/docs`

## Funcionalidades

- Gerenciamento de provas
- Sistema de questões e alternativas
- Inscrições em provas
- Correção automática
- Cache com Redis
- Busca com Elasticsearch
