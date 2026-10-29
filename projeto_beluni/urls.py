
from django.contrib import admin
from django.urls import path, include

from estudante.views import inicio, index


urlpatterns = [
    # Página pública de apresentação
    path('', index, name='index'),

    # Painel inicial após o login
    path('inicio/', inicio, name='inicio'),

    # Administração do Django
    path('admin/', admin.site.urls),

    # Aplicativos
    path('disciplinas/', include('disciplinas.urls')),
    path('atividades/', include('atividade.urls')),
    path('metas/', include('meta.urls')),
    path('estudantes/', include('estudante.urls')),
    path('notificacao/', include('notificacao.urls')),
]