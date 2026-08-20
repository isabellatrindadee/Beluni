from django.db import models
from estudante.models import Estudante


class Meta(models.Model):
    descricao = models.CharField(max_length=255)
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name="metas"
    )

    def __str__(self):
        return self.descricao
