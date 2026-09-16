def notifications_context(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {'unread_notifications': 0}
    return {'unread_notifications': request.user.notifications.filter(read=False).count()}
