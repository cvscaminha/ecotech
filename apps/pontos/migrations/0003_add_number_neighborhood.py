from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[('pontos','0002_add_cep_phone')]
    operations=[
        migrations.AddField(model_name='dropoffpoint',name='number',field=models.CharField(blank=True,max_length=20,verbose_name='Nº')),
        migrations.AddField(model_name='dropoffpoint',name='neighborhood',field=models.CharField(blank=True,max_length=120,verbose_name='bairro')),
    ]
