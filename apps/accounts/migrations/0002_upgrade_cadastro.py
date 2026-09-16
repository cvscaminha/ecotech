from django.db import migrations, models


def limpar_cpf_cnpj_duplicados(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    vistos = set()
    for usuario in User.objects.exclude(cpf_cnpj__isnull=True).exclude(cpf_cnpj='').order_by('id'):
        documento = usuario.cpf_cnpj.strip()
        if documento in vistos:
            User.objects.filter(pk=usuario.pk).update(cpf_cnpj=None)
        else:
            vistos.add(documento)


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cpf_cnpj',
            field=models.CharField(max_length=20, null=True, blank=True, verbose_name='CPF/CNPJ'),
        ),
        migrations.RunPython(limpar_cpf_cnpj_duplicados, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='telefone'),
        ),
    ]
