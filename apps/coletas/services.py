from django.utils import timezone
from apps.auditoria.services import log_action
from apps.notificacoes.services import notify
from .models import CollectionHistory, CollectionRequest

def change_status(collection, new_status, actor, notes=''):
    previous=collection.status
    # Garante persistência mesmo quando o fluxo recebe uma atualização parcial.
    collection.status=new_status
    if new_status==CollectionRequest.Status.COMPLETED:
        collection.completed_at=timezone.now()
    collection.save(update_fields=['status','completed_at','updated_at'])
    CollectionHistory.objects.create(collection=collection,previous_status=previous,new_status=new_status,user=actor,notes=notes)
    if new_status==CollectionRequest.Status.COMPLETED:
        collection.wastes.update(collected=True)
    notify(collection.user,'Atualização da coleta',f'A solicitação #{collection.pk} agora está: {collection.get_status_display()}.','COLETA')
    log_action(actor,'COLETA_STATUS',f'Coleta #{collection.pk}: {previous} -> {new_status}')
    return collection
