from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class Category(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    description = models.TextField('Descrição do resíduo (opcional)', blank=True, max_length=500)
    active = models.BooleanField('ativo', default=True)
    def __str__(self): return self.name
    class Meta: ordering = ['name']; verbose_name='categoria'; verbose_name_plural='categorias'

class ElectronicWaste(models.Model):
    class Condition(models.TextChoices):
        WORKING = 'FUNCIONANDO', 'Funcionando'
        DEFECTIVE = 'COM_DEFEITO', 'Com defeito'
        BROKEN = 'QUEBRADO', 'Quebrado'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wastes')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='wastes')
    equipment = models.CharField('equipamento', max_length=150)
    manufacturer = models.CharField('fabricante/marca', max_length=100, blank=True)
    model = models.CharField('modelo', max_length=100, blank=True)
    serial_number = models.CharField('Nº de série (opcional)', max_length=100, blank=True)
    description = models.TextField('Descrição do resíduo (opcional)', blank=True, max_length=500)
    quantity = models.PositiveIntegerField('quantidade', default=1, validators=[MinValueValidator(1)])
    weight = models.DecimalField('peso estimado (kg) (opcional)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0.01)], blank=True, null=True)
    condition = models.CharField('situação', max_length=20, choices=Condition.choices)
    image = models.ImageField('imagem', upload_to='residuos/%Y/%m/')
    class Status(models.TextChoices):
        AVAILABLE = 'DISPONIVEL', 'Disponível'
        DESTINATED = 'DESTINADO', 'Destinados'
    status = models.CharField('status', max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    collected = models.BooleanField('coletado/destinado', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f'{self.equipment} ({self.user})'
    class Meta: ordering = ['-created_at']; verbose_name='resíduo eletrônico'; verbose_name_plural='resíduos eletrônicos'
