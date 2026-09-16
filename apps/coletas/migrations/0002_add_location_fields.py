from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[('coletas','0001_initial')]
    operations=[
        migrations.AddField(model_name='collectionrequest',name='cep',field=models.CharField(blank=True,max_length=9,verbose_name='CEP')),
        migrations.AddField(model_name='collectionrequest',name='number',field=models.CharField(blank=True,max_length=20,verbose_name='número')),
        migrations.AddField(model_name='collectionrequest',name='neighborhood',field=models.CharField(blank=True,max_length=100,verbose_name='bairro')),
        migrations.AddField(model_name='collectionrequest',name='latitude',field=models.DecimalField(blank=True,decimal_places=7,max_digits=10,null=True,verbose_name='latitude')),
        migrations.AddField(model_name='collectionrequest',name='longitude',field=models.DecimalField(blank=True,decimal_places=7,max_digits=10,null=True,verbose_name='longitude')),
    ]
