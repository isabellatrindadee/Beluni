
from django import forms
from django.forms import inlineformset_factory

from .models import Atividade, AtividadeInterdisciplinar


class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade

        fields = [
            'titulo',
            'data',
            'detalhamento_atividade',
            'status',
            'prioridade',
            'pontuacao',
        ]

        labels = {
            'titulo': 'Título',
            'data': 'Data',
            'detalhamento_atividade': 'Detalhamento da atividade',
            'status': 'Status',
            'prioridade': 'Prioridade',
            'pontuacao': 'Pontuação',
        }

        widgets = {
            'titulo': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'detalhamento_atividade': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'status': forms.Select(
                choices=[
                    ('pendente', 'Pendente'),
                    ('em_andamento', 'Em andamento'),
                    ('concluida', 'Concluída'),
                ],
                attrs={'class': 'form-select'},
            ),
            'prioridade': forms.Select(
                choices=[
                    ('baixa', 'Baixa'),
                    ('media', 'Média'),
                    ('alta', 'Alta'),
                ],
                attrs={'class': 'form-select'},
            ),
            'pontuacao': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': 'any',
                }
            ),
        }


class AtividadeInterdisciplinarForm(forms.ModelForm):
    class Meta:
        model = AtividadeInterdisciplinar

        fields = [
            'disciplina',
            'criterios_de_avaliacao',
            'orientador',
        ]

        labels = {
            'disciplina': 'Disciplina',
            'criterios_de_avaliacao': 'Critérios de avaliação',
            'orientador': 'Orientador',
        }

        widgets = {
            'disciplina': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'criterios_de_avaliacao': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe os critérios (opcional)',
                }
            ),
            'orientador': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nome do orientador (opcional)',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['criterios_de_avaliacao'].required = False
        self.fields['orientador'].required = False


AtividadeInterdisciplinarFormSet = inlineformset_factory(
    Atividade,
    AtividadeInterdisciplinar,
    form=AtividadeInterdisciplinarForm,
    extra=1,
    can_delete=True,
)
