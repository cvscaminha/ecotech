from django.contrib import admin
from .models import Category, ElectronicWaste
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): list_display=('name','active'); search_fields=('name',)
@admin.register(ElectronicWaste)
class WasteAdmin(admin.ModelAdmin):
    list_display=('equipment','category','user','quantity','weight','condition','collected')
    list_filter=('category','condition','collected')
    search_fields=('equipment','manufacturer','model','user__username')
