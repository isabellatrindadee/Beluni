from django import forms
from .models import Meta


class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['titulo', 'descricao', 'data', 'estudante']

        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'data': 'Data',
            'estudante': 'Estudante',
        }

        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }