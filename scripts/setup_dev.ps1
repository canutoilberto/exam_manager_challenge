# Configuração do ambiente de desenvolvimento para Exam Manager no Windows

Write-Host "Configurando ambiente de desenvolvimento para Exam Manager..." -ForegroundColor Green

# Verificar se o Python está instalado
try {
    $pythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    Write-Host "Python $pythonVersion detectado." -ForegroundColor Green
} catch {
    Write-Host "Python não encontrado. Por favor, instale o Python 3.10 ou superior." -ForegroundColor Red
    exit 1
}

# Verificar a versão do Python
if ([version]$pythonVersion -lt [version]"3.10") {
    Write-Host "Python 3.10 ou superior é necessário. Versão atual: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Criar ambiente virtual
Write-Host "Criando ambiente virtual..." -ForegroundColor Green
python -m venv venv

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Green
pip install -r requirements.txt

# Aplicar migrations
Write-Host "Aplicando migrações..." -ForegroundColor Green
python manage.py migrate

# Criar arquivo .env a partir do .env.example se não existir
if (-not (Test-Path .\.env)) {
    Write-Host "Criando arquivo .env a partir do .env.example..." -ForegroundColor Green
    Copy-Item .\.env.example .\.env
}

# Criar superusuário
$createSuperuser = Read-Host "Deseja criar um superusuário? (s/n)"
if ($createSuperuser -eq "s" -or $createSuperuser -eq "S") {
    python manage.py createsuperuser
}

Write-Host "Configuração concluída!" -ForegroundColor Green
Write-Host "Para iniciar o servidor, execute:" -ForegroundColor Yellow
Write-Host ".\venv\Scripts\Activate.ps1 ; python manage.py runserver" -ForegroundColor Yellow 