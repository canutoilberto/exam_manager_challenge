#!/usr/bin/env python3
"""
Verifica se todas as dependências estão instaladas corretamente.
"""

import sys
import importlib
import subprocess


def check_dependency(module_name, pip_name=None):
    """Verifica se o módulo está instalado e tenta instalá-lo se não estiver."""
    if pip_name is None:
        pip_name = module_name

    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} está instalado.")
        return True
    except ImportError:
        print(f"❌ {module_name} não está instalado. Tentando instalar...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"✅ {module_name} foi instalado com sucesso.")
            return True
        except subprocess.CalledProcessError:
            print(
                f"❌ Falha ao instalar {module_name}. Verifique se o pip está atualizado."
            )
            return False


def main():
    """Verifica todas as dependências principais do projeto."""
    dependencies = [
        ("django", "django>=5.0,<5.1"),
        ("ninja", "django-ninja>=1.4.0,<2.0.0"),
        ("celery", "celery>=5.5.0,<6.0.0"),
        ("django_celery_beat", "django-celery-beat>=2.5.0,<3.0.0"),
        ("django_elasticsearch_dsl", "django-elasticsearch-dsl>=8.0,<9.0"),
        ("redis", "redis>=5.2.1,<6.0.0"),
        ("django_redis", "django-redis>=5.4.0,<6.0.0"),
        ("uvicorn", "uvicorn>=0.34.0,<0.35.0"),
        ("jwt", "pyjwt>=2.10.1,<3.0.0"),
        ("requests", "requests>=2.32.3,<3.0.0"),
        ("dj_database_url", "dj-database-url>=2.1.0,<3.0.0"),
    ]

    all_passed = True
    for module, pip_package in dependencies:
        if not check_dependency(module, pip_package):
            all_passed = False

    if all_passed:
        print("\n✅ Todas as dependências estão instaladas corretamente!")
        return 0
    else:
        print(
            "\n❌ Algumas dependências estão faltando. Por favor, corrija os problemas acima."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
