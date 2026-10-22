from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_estudante, name='login_estudante'),
    path('logout/', views.logout_estudante, name='logout_estudante'),
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('meu-perfil/editar/', views.editar_meu_perfil, name='editar_meu_perfil'),
    path('', views.listar_estudantes, name='listar_estudantes'),
    path('novo/', views.criar_estudante, name='criar_estudante'),
    path('<int:id>/', views.detalhar_estudante, name='detalhar_estudante'),
    path('<int:id>/editar/', views.editar_estudante, name='editar_estudante'),
    path('<int:id>/excluir/', views.excluir_estudante, name='excluir_estudante'),
]