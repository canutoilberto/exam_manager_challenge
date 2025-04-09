#!/bin/bash

# Configuração do ambiente de desenvolvimento para Exam Manager

echo "Configurando ambiente de desenvolvimento para Exam Manager..."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Por favor, instale o Python 3.10 ou superior."
    exit 1
fi

# Verificar a versão do Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PYTHON_VERSION < 3.10" | bc -l) -eq 1 ]]; then
    echo "Python 3.10 ou superior é necessário. Versão atual: $PYTHON_VERSION"
    exit 1
fi

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Aplicar migrations
echo "Aplicando migrações..."
python manage.py migrate

# Criar arquivo .env a partir do .env.example se não existir
if [ ! -f .env ]; then
    echo "Criando arquivo .env a partir do .env.example..."
    cp .env.example .env
fi

# Criar superusuário
echo "Deseja criar um superusuário? (s/n)"
read create_superuser
if [[ $create_superuser == "s" || $create_superuser == "S" ]]; then
    python manage.py createsuperuser
fi

echo "Configuração concluída. Para iniciar o servidor, execute:"
echo "source venv/bin/activate && python manage.py runserver" 