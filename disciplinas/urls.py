from django.urls import path

from . import views


urlpatterns = [
    path('', views.listar_disciplinas, name='listar_disciplinas'),
    path('nova/', views.criar_disciplina, name='criar_disciplina'),
    path('<int:id>/', views.detalhar_disciplina, name='detalhar_disciplina'),
    path('<int:id>/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('<int:id>/excluir/', views.excluir_disciplina, name='excluir_disciplina'),
]
