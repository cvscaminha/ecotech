from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_cpf_cnpj

class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        RESIDENTIAL = 'RESIDENCIAL', 'Usuário Residencial'
        COMPANY = 'EMPRESA', 'Empresa Parceira'
        INSTITUTION = 'INSTITUICAO', 'Instituição Ambiental'
        COLLECTION_TEAM = 'COLETA', 'Equipe de Coleta'

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.RESIDENTIAL)
    phone = models.CharField('telefone', max_length=20, blank=False)

    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=20, blank=True, null=True, validators=[validate_cpf_cnpj])
    cep = models.CharField('CEP', max_length=9, blank=True, default='')
    address = models.CharField('endereço', max_length=255, blank=False)
    number = models.CharField('número', max_length=20, blank=True, default='')
    neighborhood = models.CharField('bairro', max_length=120, blank=True, default='')
    city = models.CharField('cidade', max_length=100, blank=False)
    state = models.CharField('UF', max_length=2, blank=False)
    approved = models.BooleanField('aprovado', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_admin_profile(self):
        return self.is_superuser or self.user_type == self.UserType.ADMIN

    def __str__(self):
        return self.get_full_name() or self.username
