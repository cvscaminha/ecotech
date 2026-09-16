# Arquitetura EcoTech

- `accounts`: usuários e perfis.
- `residuos`: categorias e inventário de resíduos.
- `coletas`: solicitações, histórico e destinação.
- `pontos`: pontos de entrega e mapa.
- `dashboard`: indicadores agregados e gráficos.
- `notificacoes`: comunicação interna.
- `relatorios`: exportação PDF.
- `auditoria`: trilha administrativa.

O desenvolvimento local usa SQLite. Em produção, `production.py` lê `DATABASE_URL`, permitindo PostgreSQL sem alteração de código.
