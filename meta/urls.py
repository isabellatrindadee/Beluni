from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_metas, name='listar_metas'),
    path('nova/', views.criar_meta, name='criar_meta'),
    path('<int:id>/', views.detalhar_meta, name='detalhar_meta'),
    path('<int:id>/editar/', views.editar_meta, name='editar_meta'),
    path('<int:id>/excluir/', views.excluir_meta, name='excluir_meta'),
]