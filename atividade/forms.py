from django import forms
from .models import Atividade


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
            'disciplinas',
        ]

        labels = {
            'titulo': 'Título',
            'data': 'Data',
            'detalhamento_atividade': 'Detalhamento da atividade',
            'status': 'Status',
            'prioridade': 'Prioridade',
            'pontuacao': 'Pontuação',
            'disciplinas': 'Disciplinas',
        }

        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'status': forms.Select(
                choices=[
                    ('pendente', 'Pendente'),
                    ('em_andamento', 'Em andamento'),
                    ('concluida', 'Concluída'),
                ]
            ),
            'prioridade': forms.Select(
                choices=[
                    ('baixa', 'Baixa'),
                    ('media', 'Média'),
                    ('alta', 'Alta'),
                ]
            ),
        }