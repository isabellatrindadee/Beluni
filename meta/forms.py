
from django import forms
from .models import Meta


class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta

        fields = [
            'titulo',
            'detalhamento',
            'data',
        ]

        labels = {
            'titulo': 'Título',
            'detalhamento': 'Descrição',
            'data': 'Data',
        }

        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o título da meta',
                }
            ),
            'detalhamento': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Descreva sua meta',
                }
            ),
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
        }
