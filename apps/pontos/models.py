from django.db import models

class DropoffPoint(models.Model):
    name=models.CharField('nome',max_length=150)
    cep=models.CharField('CEP',max_length=9,blank=True)
    address=models.CharField('endereço',max_length=255)
    number=models.CharField('Nº',max_length=20,blank=True)
    neighborhood=models.CharField('bairro',max_length=120,blank=True)
    phone=models.CharField('telefone',max_length=20,blank=True)
    latitude=models.DecimalField(max_digits=10,decimal_places=7,null=True,blank=True)
    longitude=models.DecimalField(max_digits=10,decimal_places=7,null=True,blank=True)
    opening_hours=models.CharField('horário de funcionamento',max_length=150)
    responsible=models.CharField('responsável',max_length=150,blank=True)
    active=models.BooleanField('ativo',default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        ordering=['name']
        verbose_name='ponto de entrega'
        verbose_name_plural='pontos de entrega'
