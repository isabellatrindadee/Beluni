from django import forms
from .models import Disciplina


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['NomeDisciplina', 'estudante']

        labels = {
            'NomeDisciplina': 'Nome da disciplina',
            'estudante': 'Estudante',
        }