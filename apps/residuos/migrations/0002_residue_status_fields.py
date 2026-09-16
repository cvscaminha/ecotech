from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('residuos','0001_initial')]
    operations = [
        migrations.AlterField(model_name='electronicwaste', name='serial_number', field=models.CharField(blank=True, max_length=100, verbose_name='Nº de série (opcional)')),
        migrations.AlterField(model_name='electronicwaste', name='description', field=models.TextField(blank=True, max_length=500, verbose_name='Descrição do resíduo (opcional)')),
        migrations.AlterField(model_name='electronicwaste', name='weight', field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='peso estimado (kg) (opcional)')),
        migrations.AddField(model_name='electronicwaste', name='status', field=models.CharField(choices=[('DISPONIVEL','Disponível'),('DESTINADO','Destinados')], default='DISPONIVEL', max_length=20, verbose_name='status')),
    ]
