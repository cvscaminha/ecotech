from django.conf import settings
from django.db import models
from apps.residuos.models import ElectronicWaste

class CollectionRequest(models.Model):
    class Status(models.TextChoices):
        REQUESTED='SOLICITADA','Solicitada'
        ANALYSIS='ANALISE','Em análise'
        APPROVED='APROVADA','Aprovada'
        SCHEDULED='AGENDADA','Coleta agendada'
        IN_PROGRESS='ANDAMENTO','Em coleta'
        COMPLETED='FINALIZADA','Finalizada'
        CANCELED='CANCELADA','Cancelada'
    class Period(models.TextChoices):
        MORNING='MANHA','Manhã'
        AFTERNOON='TARDE','Tarde'
        EVENING='NOITE','Noite'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='collection_requests')
    wastes=models.ManyToManyField(ElectronicWaste,related_name='collection_requests')
    cep=models.CharField('CEP',max_length=9,blank=True)
    address=models.CharField('endereço de retirada',max_length=255)
    number=models.CharField('número',max_length=20,blank=True)
    neighborhood=models.CharField('bairro',max_length=100,blank=True)
    city=models.CharField('cidade',max_length=100)
    latitude=models.DecimalField('latitude',max_digits=10,decimal_places=7,null=True,blank=True)
    longitude=models.DecimalField('longitude',max_digits=10,decimal_places=7,null=True,blank=True)
    preferred_date=models.DateField('data preferencial',blank=True,null=True)
    period=models.CharField('período',max_length=20,choices=Period.choices,default=Period.MORNING)
    notes=models.TextField('observações',blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.REQUESTED)
    responsible=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_collections')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    def __str__(self): return f'Coleta #{self.pk} - {self.get_status_display()}'
    class Meta: ordering=['-created_at']; verbose_name='solicitação de coleta'; verbose_name_plural='solicitações de coleta'

class CollectionHistory(models.Model):
    collection=models.ForeignKey(CollectionRequest,on_delete=models.CASCADE,related_name='history')
    previous_status=models.CharField(max_length=20, choices=CollectionRequest.Status.choices, blank=True)
    new_status=models.CharField(max_length=20, choices=CollectionRequest.Status.choices)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['created_at']

class DestinationRecord(models.Model):
    collection=models.OneToOneField(CollectionRequest,on_delete=models.CASCADE,related_name='destination')
    institution=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='destinations')
    destination=models.CharField('destino final',max_length=255)
    destination_date=models.DateField('data da destinação')
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Destinação da coleta #{self.collection_id}'
