from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_notificacoes, name='listar_notificacoes'),
    path('criar/', views.criar_notificacao, name='criar_notificacao'),
    path('visualizar/<int:id>/', views.visualizar_notificacao, name='visualizar_notificacao'),
    path('editar/<int:id>/', views.editar_notificacao, name='editar_notificacao'),
    path('excluir/<int:id>/', views.excluir_notificacao, name='excluir_notificacao'),
]