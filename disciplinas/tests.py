
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from estudante.models import Estudante
from .models import Disciplina


class TestesDisciplina(TestCase):
    """
    Testes automatizados do aplicativo disciplinas.
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes.
        """

        self.estudante = Estudante.objects.create_user(
            username='estudante_disciplina',
            email='disciplina@teste.com',
            password='Senha123456'
        )

        self.disciplina = Disciplina.objects.create(
            nomedisciplina='Matemática',
            estudante=self.estudante
        )

    # ==========================================
    # TESTES DO MODEL
    # ==========================================

    def test_criar_disciplina(self):
        """Verifica a criação de uma disciplina."""

        self.assertEqual(
            self.disciplina.nomedisciplina,
            'Matemática'
        )

        self.assertEqual(
            self.disciplina.estudante,
            self.estudante
        )

    def test_representacao_disciplina(self):
        """Verifica o retorno do método __str__."""

        self.assertEqual(
            str(self.disciplina),
            'Matemática'
        )

    def test_disciplina_vinculada_ao_estudante(self):
        """Verifica o relacionamento entre estudante e disciplina."""

        self.assertEqual(
            self.estudante.disciplina_set.count(),
            1
        )

    def test_criar_varias_disciplinas(self):
        """Verifica se um estudante pode possuir várias disciplinas."""

        Disciplina.objects.create(
            nomedisciplina='História',
            estudante=self.estudante
        )

        Disciplina.objects.create(
            nomedisciplina='Geografia',
            estudante=self.estudante
        )

        self.assertEqual(
            Disciplina.objects.filter(
                estudante=self.estudante
            ).count(),
            3
        )

    def test_excluir_disciplina(self):
        """Verifica a exclusão de uma disciplina."""

        identificador = self.disciplina.id

        self.disciplina.delete()

        self.assertFalse(
            Disciplina.objects.filter(
                id=identificador
            ).exists()
        )

    def test_exclusao_do_estudante(self):
        """Verifica se as disciplinas são excluídas junto ao estudante."""

        identificador = self.disciplina.id

        self.estudante.delete()

        self.assertFalse(
            Disciplina.objects.filter(
                id=identificador
            ).exists()
        )

    def test_disciplinas_de_estudantes_diferentes(self):
        """Verifica a separação das disciplinas por estudante."""

        outro_estudante = Estudante.objects.create_user(
            username='outro_estudante',
            email='outro@teste.com',
            password='Senha123456'
        )

        Disciplina.objects.create(
            nomedisciplina='Física',
            estudante=outro_estudante
        )

        self.assertEqual(
            Disciplina.objects.filter(
                estudante=self.estudante
            ).count(),
            1
        )

        self.assertEqual(
            Disciplina.objects.filter(
                estudante=outro_estudante
            ).count(),
            1
        )

    def test_nome_da_disciplina_com_100_caracteres(self):
        """Verifica o tamanho máximo permitido para o nome."""

        nome = 'A' * 100

        disciplina = Disciplina.objects.create(
            nomedisciplina=nome,
            estudante=self.estudante
        )

        self.assertEqual(
            len(disciplina.nomedisciplina),
            100
        )

    def test_consultar_disciplina_por_nome(self):
        """Verifica a consulta de disciplinas pelo nome."""

        resultado = Disciplina.objects.get(
            nomedisciplina='Matemática'
        )

        self.assertEqual(
            resultado.id,
            self.disciplina.id
        )

    def test_contagem_de_disciplinas(self):
        """Verifica a quantidade de disciplinas cadastradas."""

        Disciplina.objects.create(
            nomedisciplina='Português',
            estudante=self.estudante
        )

        self.assertEqual(
            Disciplina.objects.count(),
            2
        )

