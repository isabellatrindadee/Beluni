from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Estudante


@admin.register(Estudante)
class EstudanteAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do estudante', {
            'fields': ('cpf', 'nome'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações do estudante', {
            'fields': ('cpf', 'nome'),
        }),
    )

    list_display = ('username', 'nome', 'cpf', 'is_active', 'is_staff')