from django import forms
from .models import Notificacao


class NotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = ['lida']

        labels = {
            'lida': 'Status',
        }

        widgets = {
            'lida': forms.Select(choices=[
                (False, 'Não lida'),
                (True, 'Lida'),
            ]),
        }