# Validação técnica da v1.0.3

Validações realizadas no pacote antes da entrega:

- todos os arquivos Python passam por compilação sintática (`compileall`);
- referências `{% url %}` dos templates foram confrontadas com os `app_name` e nomes das rotas existentes;
- todos os templates referenciados por `render()` existem no pacote;
- a rota `/dashboard` possui redirecionamento explícito para `/dashboard/`;
- `Instalar.bat` gera migrations antes de executar `migrate` e interrompe em caso de falha;
- dependências locais foram reduzidas às necessárias para Windows/Python 3.13;
- dependências de produção ficaram separadas em `requirements/production.txt`.

## Limitação do ambiente de geração
O ambiente usado para montar este pacote não possui acesso ao PyPI, portanto não foi possível instalar Django aqui e executar `manage.py test` localmente. O próprio pacote inclui `Testar.bat` para executar a homologação runtime no Windows após `Instalar.bat`.
