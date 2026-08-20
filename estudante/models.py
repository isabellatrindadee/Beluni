from django.db import models
from django.contrib.auth.models import User


class Estudante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

