
from django import forms
from .models import Disciplina


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina

        fields = ['nomedisciplina']

        labels = {
            'nomedisciplina': 'Nome da disciplina',
        }

        widgets = {
            'nomedisciplina': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o nome da disciplina',
                }
            ),
        }
