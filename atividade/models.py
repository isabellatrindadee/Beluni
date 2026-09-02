from django.db import models
from disciplinas.models import Disciplina


class Atividade(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateField()
    detalhamento_atividade = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    prioridade = models.CharField(max_length=50)
    pontuacao = models.FloatField()

    disciplinas = models.ManyToManyField(
        Disciplina,
        through="AtividadeInterdisciplinar",
        related_name="atividades"
    )

    def __str__(self):
        return self.titulo


class AtividadeInterdisciplinar(models.Model):
    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.CASCADE
    )

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE
    )

    criterios_de_avaliacao = models.CharField(max_length=255)
    orientador = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.atividade} - {self.disciplina}"