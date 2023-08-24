from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente, name='cliente'),
    path('busca_cliente/', views.busca_cliente, name='busca_cliente'),
    path('update_cliente/<int:id>', views.update_cliente, name='update_cliente'),
    path('update_carro/<int:id>', views.update_carro, name='update_carro'),
    path('delete_carro/<int:id>', views.delete_carro, name='delete_carro'),
]
