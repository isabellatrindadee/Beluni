from django.urls import path
from . import views


urlpatterns = [
    path('', views.listar_estudantes, name='listar_estudantes'),
    path('novo/', views.criar_estudante, name='criar_estudante'),
    path('<int:id>/', views.detalhar_estudante, name='detalhar_estudante'),
    path('<int:id>/editar/', views.editar_estudante, name='editar_estudante'),
    path('<int:id>/excluir/', views.excluir_estudante, name='excluir_estudante'),
]