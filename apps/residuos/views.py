from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import WasteForm, CategoryForm
from .models import ElectronicWaste, Category
from apps.auditoria.services import log_action


def _scope(user):
    return ElectronicWaste.objects.all() if user.is_admin_profile else ElectronicWaste.objects.filter(user=user)

@login_required
def list_wastes(request):
    qs = _scope(request.user).select_related('category','user')
    q = request.GET.get('q','').strip()
    status = request.GET.get('status','')
    condition = request.GET.get('condition','')
    category = request.GET.get('category','')
    date_from = request.GET.get('date_from','')
    date_to = request.GET.get('date_to','')
    if q:
        qs = qs.filter(Q(equipment__icontains=q)|Q(manufacturer__icontains=q)|Q(model__icontains=q)|Q(user__username__icontains=q))
    if status == 'DISPONIVEL': qs = qs.filter(status='DISPONIVEL')
    elif status == 'DESTINADO': qs = qs.filter(status='DESTINADO')
    if condition: qs = qs.filter(condition=condition)
    if category: qs = qs.filter(category_id=category)
    if date_from: qs = qs.filter(created_at__date__gte=date_from)
    if date_to: qs = qs.filter(created_at__date__lte=date_to)
    return render(request,'residuos/list.html',{'wastes':qs,'q':q,'status':status,'categories':Category.objects.all(),'selected_category':category,'condition':condition,'date_from':date_from,'date_to':date_to})

@login_required
def create_waste(request):
    form = WasteForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        waste=form.save(commit=False); waste.user=request.user; waste.save()
        log_action(request.user,'RESIDUO_CRIADO',f'Resíduo #{waste.pk} ({waste.equipment}) cadastrado.')
        messages.success(request,'Resíduo cadastrado com sucesso.')
        return redirect('residuos:list')
    return render(request,'residuos/form.html',{'form':form,'title':'Cadastro de Resíduo'})

@login_required
def edit_waste(request, pk):
    waste=get_object_or_404(_scope(request.user),pk=pk)
    if waste.collected:
        messages.warning(request,'Resíduos já coletados não podem ser editados.')
        return redirect('residuos:list')
    form=WasteForm(request.POST or None, request.FILES or None, instance=waste)
    if request.method == 'POST' and form.is_valid():
        form.save(); log_action(request.user,'RESIDUO_EDITADO',f'Resíduo #{waste.pk} ({waste.equipment}) atualizado.'); messages.success(request,'Resíduo atualizado com sucesso.'); return redirect('residuos:list')
    return render(request,'residuos/form.html',{'form':form,'title':'Editar resíduo','waste':waste})

@login_required
def detail_waste(request, pk):
    waste=get_object_or_404(_scope(request.user),pk=pk)
    return render(request,'residuos/detail.html',{'waste':waste})

@login_required
def delete_waste(request, pk):
    waste=get_object_or_404(_scope(request.user),pk=pk)
    if request.method == 'POST' and not waste.collected:
        waste.delete(); messages.success(request,'Resíduo removido.')
    return redirect('residuos:list')


@login_required
def categories(request):
    if not request.user.is_admin_profile:
        return redirect('dashboard:home')
    qs=Category.objects.annotate(total_wastes=Count('wastes'))
    q=request.GET.get('q','').strip(); status=request.GET.get('status','')
    if q: qs=qs.filter(Q(name__icontains=q)|Q(description__icontains=q))
    if status=='ativa': qs=qs.filter(active=True)
    elif status=='inativa': qs=qs.filter(active=False)
    return render(request,'residuos/categories.html',{'categories':qs,'q':q,'status':status})

@login_required
def category_create(request):
    if not request.user.is_admin_profile:
        return redirect('dashboard:home')
    form=CategoryForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save()
        log_action(request.user,'CATEGORIA_CRIADA',f'Categoria {obj.name} criada.')
        messages.success(request,'Categoria cadastrada com sucesso.')
        return redirect('residuos:categories')
    return render(request,'residuos/category_form.html',{'form':form,'title':'Nova Categoria'})

@login_required
def category_edit(request, pk):
    if not request.user.is_admin_profile:
        return redirect('dashboard:home')
    obj=get_object_or_404(Category,pk=pk)
    form=CategoryForm(request.POST or None,instance=obj)
    if request.method=='POST' and form.is_valid():
        old_active=obj.active; updated=form.save()
        action='CATEGORIA_STATUS' if old_active != updated.active else 'CATEGORIA_EDITADA'
        log_action(request.user,action,f'Categoria {updated.name} atualizada. Status: {"Ativa" if updated.active else "Inativa"}.')
        messages.success(request,'Categoria atualizada com sucesso.')
        return redirect('residuos:categories')
    return render(request,'residuos/category_form.html',{'form':form,'title':'Editar Categoria'})

@login_required
def category_delete(request, pk):
    if not request.user.is_admin_profile:
        return redirect('dashboard:home')
    obj=get_object_or_404(Category,pk=pk)

    if request.method == 'POST':
        if obj.wastes.exists():
            messages.error(request, 'Não é possível excluir esta categoria. Existem resíduos vinculados a ela.')
            return redirect('residuos:categories')

        name=obj.name; obj.delete()
        log_action(request.user,'CATEGORIA_EXCLUIDA',f'Categoria {name} excluída.')
        messages.success(request, 'Categoria excluída com sucesso.')

    return redirect('residuos:categories')
