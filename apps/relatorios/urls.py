from django.urls import path
from . import views
app_name='relatorios'
urlpatterns=[path('ambiental.pdf',views.environmental_pdf,name='environmental_pdf')]
