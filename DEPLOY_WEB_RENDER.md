
# EcoTech 1.5.44 - Preparação para Deploy Web

## Objetivo
Versão preparada para publicação da plataforma EcoTech na internet.

## Ambiente recomendado
Render + PostgreSQL + Gunicorn.

## Arquivos de deploy incluídos

- render.yaml
- build.sh
- runtime.txt
- requirements/
- configuração production do Django

## Passos

1. Criar repositório no GitHub.
2. Enviar todos os arquivos desta pasta.
3. No Render, criar um novo Web Service conectado ao repositório.
4. Aplicar o arquivo render.yaml.
5. Aguardar instalação das dependências.
6. Executar migrações.
7. Criar usuário administrador.

## Variáveis esperadas

DJANGO_SETTINGS_MODULE=config.settings.production

DATABASE_URL será criada pelo banco PostgreSQL do Render.

## Validação antes da apresentação

- Login funcionando;
- Cadastro funcionando;
- Resíduos funcionando;
- Coletas funcionando;
- Destinação funcionando;
- Mapa carregando;
- Dashboard funcionando.
