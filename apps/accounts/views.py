from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .decorators import user_type_required
from .forms import ProfileForm, RegistrationForm, AdminUserForm
from .models import User
from apps.auditoria.services import log_action


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'accounts/landing.html')


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Conta criada com sucesso. Bem-vindo ao EcoTech!')
        return redirect('dashboard:home')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def deactivate_account(request):
    if request.method == 'POST':
        request.user.is_active = False
        request.user.save(update_fields=['is_active'])
        messages.success(request, 'Conta desativada com sucesso.')
        from django.contrib.auth import logout
        logout(request)
    return redirect('accounts:login')


@user_type_required(User.UserType.ADMIN)
def manage_users(request):
    users = User.objects.order_by('-date_joined')
    q = request.GET.get('q', '').strip()
    role = request.GET.get('role','')
    active = request.GET.get('active','')
    if q:
        from django.db.models import Q
        users = users.filter(Q(username__icontains=q)|Q(email__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q))
    if role: users=users.filter(user_type=role)
    if active=='1': users=users.filter(is_active=True)
    elif active=='0': users=users.filter(is_active=False)
    return render(request, 'accounts/manage_users.html', {'users': users, 'q': q,'role':role,'active':active,'role_choices':User.UserType.choices})


@user_type_required(User.UserType.ADMIN)
def toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and user.pk != request.user.pk:
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        log_action(request.user,'USUARIO_STATUS',f'Usuário {user.username}: {"ativado" if user.is_active else "inativado"}.')
        messages.success(request, 'Situação do usuário atualizada com sucesso.')
    return redirect('accounts:manage_users')


@user_type_required(User.UserType.ADMIN)
def create_user_admin(request):
    form = AdminUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        return redirect('accounts:manage_users')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Novo usuário'})
