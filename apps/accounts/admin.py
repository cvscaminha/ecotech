from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class EcoTechUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('EcoTech', {'fields': ('user_type','phone','cpf_cnpj','address','city','state','approved')}),)
    list_display = ('username','email','user_type','approved','is_active')
    list_filter = ('user_type','approved','is_active')
