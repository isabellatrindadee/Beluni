from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_atividades, name='listar_atividades'),
    path('nova/', views.criar_atividade, name='criar_atividade'),
    path('<int:id>/', views.detalhar_atividade, name='detalhar_atividade'),
    path('<int:id>/editar/', views.editar_atividade, name='editar_atividade'),
    path('<int:id>/excluir/', views.excluir_atividade, name='excluir_atividade'),
]