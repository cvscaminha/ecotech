from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_upgrade_cadastro'),
    ]

    operations = [
        # A restricao UNIQUE foi removida desta migration.
        # A validacao de duplicidade e realizada na camada da aplicacao
        # para preservar bancos SQLite ja populados.
    ]
