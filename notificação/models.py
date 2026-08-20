from django.db import models
from estudante.models import Estudante


class Notificacao(models.Model):
    mensagem = models.CharField(max_length=255)
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.mensagem