from .models import AuditLog
def log_action(user,action,description): return AuditLog.objects.create(user=user if getattr(user,'is_authenticated',False) else None,action=action,description=description)
