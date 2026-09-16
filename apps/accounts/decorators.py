from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

ROLE_PERMISSIONS = {
    'ADMIN': {'users.manage','categories.manage','wastes.manage','collections.manage','points.manage','dashboard.admin','history.view'},
    'INSTITUICAO': {'collections.manage','points.view','wastes.view'},
    'EMPRESA': {'wastes.own','collections.own','points.view'},
    'RESIDENCIAL': {'wastes.own','collections.own','points.view'},
}

def has_role_permission(user, permission):
    if not getattr(user, 'is_authenticated', False): return False
    if user.is_superuser: return True
    return permission in ROLE_PERMISSIONS.get(user.user_type, set())

def permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request,*args,**kwargs):
            if not request.user.is_authenticated: return redirect('accounts:login')
            if has_role_permission(request.user, permission): return view_func(request,*args,**kwargs)
            messages.error(request,'Você não possui permissão para realizar esta operação.')
            return redirect('dashboard:home')
        return wrapper
    return decorator

def user_type_required(*allowed):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated: return redirect('accounts:login')
            if request.user.is_superuser or request.user.user_type in allowed: return view_func(request,*args,**kwargs)
            messages.error(request,'Você não possui permissão para acessar esta área.')
            return redirect('dashboard:home')
        return wrapper
    return decorator
