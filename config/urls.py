from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('dashboard', RedirectView.as_view(pattern_name='dashboard:home', permanent=False)),
    path('painel/', RedirectView.as_view(pattern_name='dashboard:home', permanent=False)),
    path('residuos/', include('apps.residuos.urls')),
    path('coletas/', include('apps.coletas.urls')),
    path('pontos/', include('apps.pontos.urls')),
    path('notificacoes/', include('apps.notificacoes.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
    path('auditoria/', include('apps.auditoria.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
