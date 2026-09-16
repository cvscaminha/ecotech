# Deploy EcoTech

## Stack de produção
- Python 3.13
- Django 5.2
- PostgreSQL
- Gunicorn
- WhiteNoise

## Variáveis obrigatórias
- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `SECRET_KEY=<valor forte>`
- `DATABASE_URL=<postgresql://...>`
- `ALLOWED_HOSTS=seu-dominio.com`
- `CSRF_TRUSTED_ORIGINS=https://seu-dominio.com`

## Build
`bash build.sh`

## Start
`gunicorn config.wsgi:application`

Antes da publicação definitiva, altere senhas demonstrativas e configure armazenamento persistente para uploads de mídia.
