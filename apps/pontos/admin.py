from django.contrib import admin
from .models import DropoffPoint
@admin.register(DropoffPoint)
class DropoffPointAdmin(admin.ModelAdmin): list_display=('name','address','opening_hours','active'); list_filter=('active',); search_fields=('name','address')
