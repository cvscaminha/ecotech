from apps.accounts.decorators import user_type_required
from apps.accounts.models import User
from django.shortcuts import render
from .models import AuditLog
@user_type_required(User.UserType.ADMIN)
def audit_list(request): return render(request,'auditoria/list.html',{'logs':AuditLog.objects.select_related('user')[:300]})
