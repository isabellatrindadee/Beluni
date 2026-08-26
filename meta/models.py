from django.db import models
from estudante.models import Estudante


class Meta(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    data = models.DateField()
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name="metas"
    )

    def __str__(self):
        return self.titulo