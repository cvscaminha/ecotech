#!/usr/bin/env bash
set -o errexit

echo "=== EcoTech: instalando dependencias ==="
pip install -r requirements/production.txt

echo "=== EcoTech: aplicando migrations ==="
python manage.py migrate --noinput

echo "=== EcoTech: criando administrador inicial, se necessario ==="
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ECOTECH_ADMIN_USERNAME", "admin")
email = os.environ.get("ECOTECH_ADMIN_EMAIL", "")
password = os.environ.get("ECOTECH_ADMIN_PASSWORD")

if not password:
    print("ECOTECH_ADMIN_PASSWORD nao definida. Administrador nao foi criado.")
elif User.objects.filter(username=username).exists():
    print(f"Usuario '{username}' ja existe. Nenhuma alteracao realizada.")
else:
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print(f"Administrador '{username}' criado com sucesso.")
PY

echo "=== EcoTech: coletando arquivos estaticos ==="
python manage.py collectstatic --noinput

echo "=== Build do EcoTech concluido ==="
