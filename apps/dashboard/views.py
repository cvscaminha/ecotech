from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import dashboard_context

@login_required
def dashboard(request):
    return render(request, 'dashboard/home.html', dashboard_context(request.user))

@login_required
def environmental(request):
    return render(request, 'dashboard/environmental.html', dashboard_context(request.user))
