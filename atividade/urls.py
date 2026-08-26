from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_atividades, name='listar_atividades'),
    path('nova/', views.criar_atividade, name='criar_atividade'),
]