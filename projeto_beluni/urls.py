from django.contrib import admin
from django.urls import path, include
from estudante.views import inicio
from estudante.views import index


    
urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('disciplinas/', include('disciplinas.urls')),
    path('atividades/', include('atividade.urls')),
    path('metas/', include('meta.urls')),
    path('estudantes/', include('estudante.urls')),
    path('notificacao/', include('notificacao.urls')),
]
