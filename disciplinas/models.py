from django.db import models


class Disciplina(models.Model):
    NomeDisciplina = models.CharField(max_length=100)
    estudante = models.ForeignKey(
        'estudante.Estudante',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.NomeDisciplina