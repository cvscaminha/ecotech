from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views
from .forms import LoginForm

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='landing'),
    path('cadastro/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.profile, name='profile'),
    path('perfil/desativar/', views.deactivate_account, name='deactivate_account'),
    path('usuarios/gestao/', views.manage_users, name='manage_users'),
    path('usuarios/novo/', views.create_user_admin, name='create_user_admin'),
    path('usuarios/<int:pk>/alternar/', views.toggle_user, name='toggle_user'),
    path('senha/reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.txt',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done'),
    ), name='password_reset'),
    path('senha/reset/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('senha/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('senha/reset/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
