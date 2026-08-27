from django.contrib import admin

from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('disciplinas/', include('disciplinas.urls')),
    path('atividades/', include('atividade.urls')),
    path('metas/', include('meta.urls')),
    path('estudantes/', include('estudante.urls')),
     path('notificacao/', include('notificacao.urls')),
]