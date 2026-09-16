from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.accounts.decorators import user_type_required
from apps.accounts.models import User
from apps.auditoria.services import log_action
from apps.notificacoes.services import notify
from .forms import CollectionRequestForm, DestinationForm, StatusUpdateForm
from .models import CollectionHistory, CollectionRequest, DestinationRecord
from .services import change_status

@login_required
def my_collections(request):
    qs=CollectionRequest.objects.filter(user=request.user).prefetch_related('wastes')
    return render(request,'coletas/list.html',{'collections':qs})

@login_required
def create_collection(request):
    form=CollectionRequestForm(request.POST or None,user=request.user)
    if request.method=='POST' and form.is_valid():
        collection=form.save(commit=False); collection.user=request.user; collection.save(); form.save_m2m()
        CollectionHistory.objects.create(collection=collection,previous_status='',new_status=collection.status,user=request.user,notes='Solicitação criada pelo usuário.')
        log_action(request.user,'COLETA_CRIADA',f'Solicitação de coleta #{collection.pk} criada.')
        notify(request.user,'Solicitação recebida',f'Sua solicitação #{collection.pk} foi registrada.','COLETA')
        messages.success(request,'Solicitação de coleta enviada com sucesso.')
        return redirect('coletas:detail',pk=collection.pk)
    return render(request,'coletas/form.html',{'form':form})

@login_required
def detail_collection(request,pk):
    collection=get_object_or_404(CollectionRequest.objects.prefetch_related('wastes','history'),pk=pk)
    if not (request.user.is_admin_profile or request.user.user_type==User.UserType.INSTITUTION or collection.user_id==request.user.id):
        messages.error(request,'Acesso não autorizado.'); return redirect('dashboard:home')
    return render(request,'coletas/detail.html',{'collection':collection})



@login_required
def print_collection(request, pk):
    collection=get_object_or_404(CollectionRequest.objects.prefetch_related('wastes'), pk=pk)
    if not (request.user.is_admin_profile or request.user.user_type==User.UserType.INSTITUTION or collection.user_id==request.user.id):
        messages.error(request,'Acesso não autorizado.')
        return redirect('dashboard:home')
    return render(request,'coletas/print_collection.html',{'collection':collection})

@login_required
def cancel_collection(request, pk):
    collection = get_object_or_404(CollectionRequest, pk=pk, user=request.user)
    if request.method == 'POST':
        blocked = [CollectionRequest.Status.IN_PROGRESS, CollectionRequest.Status.COMPLETED, CollectionRequest.Status.CANCELED]
        if collection.status in blocked:
            messages.error(request, 'Esta solicitação não pode mais ser cancelada.')
        else:
            change_status(collection, CollectionRequest.Status.CANCELED, request.user, 'Cancelada pelo solicitante.')
            messages.success(request, 'Solicitação cancelada.')
    return redirect('coletas:detail', pk=pk)

@user_type_required(User.UserType.ADMIN,User.UserType.INSTITUTION)
def manage_collections(request):
    qs=CollectionRequest.objects.select_related('user','responsible').prefetch_related('wastes')
    status=request.GET.get('status',''); q=request.GET.get('q','').strip(); date_from=request.GET.get('date_from',''); date_to=request.GET.get('date_to','')
    if status: qs=qs.filter(status=status)
    if q:
        from django.db.models import Q
        qs=qs.filter(Q(user__username__icontains=q)|Q(user__first_name__icontains=q)|Q(address__icontains=q)|Q(city__icontains=q))
    if date_from: qs=qs.filter(created_at__date__gte=date_from)
    if date_to: qs=qs.filter(created_at__date__lte=date_to)
    return render(request,'coletas/manage.html',{'collections':qs,'status_choices':CollectionRequest.Status.choices,'selected_status':status,'q':q,'date_from':date_from,'date_to':date_to})

@user_type_required(User.UserType.ADMIN,User.UserType.INSTITUTION)
def update_status(request,pk):
    collection=get_object_or_404(CollectionRequest,pk=pk)
    form=StatusUpdateForm(request.POST or None,instance=collection)
    if request.method=='POST' and form.is_valid():
        new_status=form.cleaned_data['status']
        if request.user.user_type==User.UserType.INSTITUTION and not request.user.is_superuser and new_status!=CollectionRequest.Status.COMPLETED:
            messages.error(request,'A instituição só pode confirmar a finalização da coleta.')
            return redirect('coletas:manage')
        # Atualiza os dados do formulário antes da mudança de status.
        # Evita que o status selecionado na tela seja perdido antes da persistência.
        collection.responsible=form.cleaned_data.get('responsible')
        collection.save(update_fields=['responsible'])

        change_status(collection,new_status,request.user,form.cleaned_data.get('notes',''))
        messages.success(request,'Status atualizado com sucesso.')
        return redirect('coletas:detail',pk=pk)
    return render(request,'coletas/status_form.html',{'form':form,'collection':collection})

@user_type_required(User.UserType.ADMIN,User.UserType.INSTITUTION)
def register_destination(request,pk):
    collection=get_object_or_404(CollectionRequest,pk=pk,status=CollectionRequest.Status.COMPLETED)
    instance=getattr(collection,'destination',None)
    form=DestinationForm(request.POST or None,instance=instance)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.collection=collection; obj.institution=request.user; obj.save()
        log_action(request.user,'DESTINACAO',f'Destinação registrada para coleta #{collection.pk}')
        notify(collection.user,'Destinação registrada',f'Os materiais da coleta #{collection.pk} tiveram a destinação registrada.','DESTINACAO')
        messages.success(request,'Destinação registrada com sucesso.')
        return redirect('coletas:detail',pk=pk)
    return render(request,'coletas/destination_form.html',{'form':form,'collection':collection})
