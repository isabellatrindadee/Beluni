from django.db import models
from estudante.models import Estudante
from atividade.models import Atividade


class Notificacao(models.Model):
    mensagem = models.CharField(max_length=255)

    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name="notificacoes"
    )

    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.CASCADE,
        related_name="notificacoes",
        null=True,
        blank=True
    )

    lida = models.BooleanField(default=False)

    def __str__(self):
        return self.mensagem