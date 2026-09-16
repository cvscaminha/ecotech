from django.contrib import admin
from .models import CollectionHistory, CollectionRequest, DestinationRecord
class HistoryInline(admin.TabularInline): model=CollectionHistory; extra=0; readonly_fields=('previous_status','new_status','user','notes','created_at')
@admin.register(CollectionRequest)
class CollectionAdmin(admin.ModelAdmin):
    list_display=('id','user','status','preferred_date','responsible','created_at')
    list_filter=('status','period','city'); search_fields=('user__username','address','city'); inlines=(HistoryInline,)
admin.site.register(DestinationRecord)
