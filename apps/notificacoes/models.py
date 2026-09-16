from django.conf import settings
from django.db import models
class Notification(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    title=models.CharField(max_length=150); message=models.TextField(); kind=models.CharField(max_length=50,blank=True); read=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
