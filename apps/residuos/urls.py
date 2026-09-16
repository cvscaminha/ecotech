from django.urls import path
from . import views
app_name='residuos'
urlpatterns=[
    path('',views.list_wastes,name='list'),
    path('novo/',views.create_waste,name='create'),
    path('<int:pk>/',views.detail_waste,name='detail'),
    path('<int:pk>/editar/',views.edit_waste,name='edit'),
    path('<int:pk>/excluir/',views.delete_waste,name='delete'),
    path('categorias/',views.categories,name='categories'),
    path('categorias/nova/',views.category_create,name='category_create'),
    path('categorias/<int:pk>/editar/',views.category_edit,name='category_edit'),
    path('categorias/<int:pk>/excluir/',views.category_delete,name='category_delete'),
]
