from django.conf import settings
from django.db import models
class AuditLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    action=models.CharField(max_length=80); description=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
