from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.listar_notificacoes,
        name='listar_notificacoes'
    ),

    path(
        '<int:id>/',
        views.detalhar_notificacao,
        name='detalhar_notificacao'
    ),

    path(
        '<int:id>/editar/',
        views.editar_notificacao,
        name='editar_notificacao'
    ),

    path(
        '<int:id>/excluir/',
        views.excluir_notificacao,
        name='excluir_notificacao'
    ),
] 