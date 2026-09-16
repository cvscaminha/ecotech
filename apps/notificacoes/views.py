from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Notification
@login_required
def notification_list(request): return render(request,'notificacoes/list.html',{'notifications':request.user.notifications.all()})
@login_required
def mark_read(request,pk):
    n=get_object_or_404(Notification,pk=pk,user=request.user); n.read=True; n.save(update_fields=['read']); return redirect('notificacoes:list')
