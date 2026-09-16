#!/usr/bin/env bash
set -o errexit
pip install -r requirements/production.txt
python manage.py makemigrations accounts residuos coletas pontos notificacoes auditoria --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
