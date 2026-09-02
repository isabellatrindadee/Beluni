from django import forms
from .models import Meta


class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['titulo', 'detalhamento', 'data', 'estudante']

        labels = {
            'titulo': 'Título',
            'detalhamento': 'Descrição',
            'data': 'Data',
            'estudante': 'Estudante',
        }

        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }