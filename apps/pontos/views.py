from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import user_type_required
from apps.accounts.models import User
from .forms import DropoffPointForm
from .models import DropoffPoint

@login_required
def map_points(request):
    points=list(DropoffPoint.objects.filter(active=True).values('id','name','address','number','neighborhood','latitude','longitude','phone','opening_hours','responsible'))
    for p in points:
        try:
            p['latitude'] = float(p['latitude']) if p['latitude'] is not None else None
            p['longitude'] = float(p['longitude']) if p['longitude'] is not None else None
        except (TypeError, ValueError):
            p['latitude'] = None
            p['longitude'] = None
    return render(request,'pontos/map.html',{'points':points})

@user_type_required(User.UserType.ADMIN)
def manage_points(request):
    return render(request,'pontos/manage.html',{'points':DropoffPoint.objects.all()})

@user_type_required(User.UserType.ADMIN)
def point_form(request,pk=None):
    obj=get_object_or_404(DropoffPoint,pk=pk) if pk else None
    form=DropoffPointForm(request.POST or None,instance=obj)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Ponto salvo com sucesso.'); return redirect('pontos:manage')
    return render(request,'pontos/form.html',{'form':form,'point':obj})
