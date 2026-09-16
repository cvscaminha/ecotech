from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[('pontos','0001_initial')]
    operations=[
        migrations.AddField(model_name='dropoffpoint',name='cep',field=models.CharField(blank=True,max_length=9,verbose_name='CEP')),
        migrations.AddField(model_name='dropoffpoint',name='phone',field=models.CharField(blank=True,max_length=20,verbose_name='telefone')),
        migrations.AlterField(model_name='dropoffpoint',name='latitude',field=models.DecimalField(blank=True,decimal_places=7,max_digits=10,null=True)),
        migrations.AlterField(model_name='dropoffpoint',name='longitude',field=models.DecimalField(blank=True,decimal_places=7,max_digits=10,null=True)),
    ]
