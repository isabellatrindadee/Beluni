from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_metas, name='listar_metas'),
    path('nova/', views.criar_meta, name='criar_meta'),
]