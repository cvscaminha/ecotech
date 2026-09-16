# EcoTech v1.0.3 — Plataforma Inteligente para Gestão de Resíduos Eletroeletrônicos

Versão integrada e corrigida para **Windows 11 + Python 3.13.5 + Django 5.2 + SQLite** e preparada para deploy com PostgreSQL.

## Instalação local
1. Extraia o ZIP em uma pasta nova. Não misture com versões anteriores.
2. Confirme no Prompt: `python --version` (esperado Python 3.13.x).
3. Execute **Instalar.bat**.
4. Aguarde a mensagem `INSTALACAO CONCLUIDA COM SUCESSO`.
5. Execute **Executar.bat**.
6. O navegador abrirá `http://127.0.0.1:8000/dashboard/`.

## Contas demonstrativas
- Administrador: `admin` / `EcoTech@2026`
- Residencial: `joao` / `EcoTech@2026`
- Empresa: `empresa` / `EcoTech@2026`
- Instituição: `instituicao` / `EcoTech@2026`

O login aceita **nome de usuário ou e-mail**.

## Módulos
- cadastro/login/perfil e permissões;
- gestão de usuários pelo administrador;
- CRUD de resíduos com foto;
- solicitação e acompanhamento de coletas;
- gestão administrativa de status;
- registro de destinação por instituição/admin;
- pontos de entrega e mapa Leaflet/OpenStreetMap;
- dashboards e gráficos;
- notificações;
- auditoria;
- relatório ambiental PDF;
- Django Admin.

## Rotas úteis
- `/` página inicial
- `/login/` login
- `/dashboard/` painel
- `/dashboard/impacto/` impacto ambiental
- `/residuos/`
- `/coletas/`
- `/pontos/`
- `/admin/` Django Admin

`/dashboard` sem barra também é aceito e redireciona corretamente.

## Testes
Execute `Testar.bat` após a instalação.

## Produção
Veja `docs/DEPLOY.md`. O projeto possui `config.settings.production`, WhiteNoise, Gunicorn, PostgreSQL via `DATABASE_URL`, `build.sh`, `Procfile` e `render.yaml`.
