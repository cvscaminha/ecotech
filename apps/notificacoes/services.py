from .models import Notification
def notify(user,title,message,kind=''):
    return Notification.objects.create(user=user,title=title,message=message,kind=kind)
