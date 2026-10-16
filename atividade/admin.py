from django.contrib import admin
from .models import Atividade, AtividadeInterdisciplinar

class AtividadeInterdisciplinarInline(admin.TabularInline):
    model = AtividadeInterdisciplinar
    extra = 1


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'status', 'prioridade')
    inlines = [AtividadeInterdisciplinarInline]


@admin.register(AtividadeInterdisciplinar)
class AtividadeInterdisciplinarAdmin(admin.ModelAdmin):
    list_display = (
        'atividade',
        'disciplina',
        'criterios_de_avaliacao',
        'orientador',
    )
    list_filter = ('disciplina',)
