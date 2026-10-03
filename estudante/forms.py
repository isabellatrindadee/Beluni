from django import forms
from .models import Estudante


class EstudanteForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuário',
        max_length=150
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Estudante
        fields = ['username', 'senha', 'cpf', 'nome']

        labels = {
            'username': 'Usuário',
            'cpf': 'CPF',
            'nome': 'Nome',
        }