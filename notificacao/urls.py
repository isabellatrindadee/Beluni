
from django.urls import path
from . import views

app_name = 'notificacao'

urlpatterns = [
    path(
        '',
        views.listar_notificacoes,
        name='listar_notificacoes'
    ),
    path(
        '<int:pk>/',
        views.detalhar_notificacao,
        name='visualizar_notificacao'
    ),
    path(
        '<int:pk>/editar/',
        views.editar_notificacao,
        name='editar_notificacao'
    ),
    path(
        '<int:pk>/excluir/',
        views.excluir_notificacao,
        name='excluir_notificacao'
    ),
]
