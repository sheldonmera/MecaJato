from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente, name='cliente'),
    path('atualiza_cliente/', views.atualiza_cliente, name='atualiza_cliente'),
    path('update_carro/<int:id>', views.update_carro, name='update_carro'),
    path('delete_carro/<int:id>', views.delete_carro, name='delete_carro'),
]
