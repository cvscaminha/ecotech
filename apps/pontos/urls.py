from django.urls import path
from . import views
app_name='pontos'
urlpatterns=[
    path('',views.map_points,name='map'),
    path('gestao/',views.manage_points,name='manage'),
    path('gestao/novo/',views.point_form,name='create'),
    path('gestao/<int:pk>/editar/',views.point_form,name='edit'),
]
