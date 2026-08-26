from django import forms
from .models import Estudante


class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = ['usuario', 'cpf', 'nome']

        labels = {
            'usuario': 'Usuário',
            'cpf': 'CPF',
            'nome': 'Nome',
        }