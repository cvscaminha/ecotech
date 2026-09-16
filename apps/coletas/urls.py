from django.urls import path
from . import views
app_name='coletas'
urlpatterns=[
    path('',views.my_collections,name='list'),
    path('nova/',views.create_collection,name='create'),
    path('<int:pk>/',views.detail_collection,name='detail'),
    path('<int:pk>/imprimir/',views.print_collection,name='print'),
    path('<int:pk>/cancelar/',views.cancel_collection,name='cancel'),
    path('gestao/',views.manage_collections,name='manage'),
    path('gestao/<int:pk>/status/',views.update_status,name='status'),
    path('gestao/<int:pk>/destinacao/',views.register_destination,name='destination'),
]
