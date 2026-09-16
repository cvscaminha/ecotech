from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('accounts', '0004_alter_user_address_alter_user_city_and_more')]

    operations = [
        migrations.AddField(model_name='user', name='cep', field=models.CharField(blank=True, default='', max_length=9, verbose_name='CEP')),
        migrations.AddField(model_name='user', name='number', field=models.CharField(blank=True, default='', max_length=20, verbose_name='número')),
        migrations.AddField(model_name='user', name='neighborhood', field=models.CharField(blank=True, default='', max_length=120, verbose_name='bairro')),
    ]
