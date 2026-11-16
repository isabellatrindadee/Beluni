
from datetime import date

from django.test import TestCase

from estudante.models import Estudante
from disciplinas.models import Disciplina

from .models import Atividade, AtividadeInterdisciplinar


class TestesAtividade(TestCase):
    """
    Testes automatizados do aplicativo atividade.
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes.
        """

        self.estudante = Estudante.objects.create_user(
            username='estudante_atividade',
            email='atividade@teste.com',
            password='Senha123456'
        )

        self.disciplina = Disciplina.objects.create(
            nomedisciplina='Matemática',
            estudante=self.estudante
        )

        self.atividade = Atividade.objects.create(
            titulo='Prova de Matemática',
            data=date(2026, 12, 10),
            detalhamento_atividade='Avaliação do conteúdo estudado.',
            status='Pendente',
            prioridade='Alta',
            pontuacao=10.0
        )

    # ==========================================
    # TESTES DO MODEL ATIVIDADE
    # ==========================================

    def test_criar_atividade(self):
        """Verifica a criação de uma atividade."""

        self.assertEqual(
            self.atividade.titulo,
            'Prova de Matemática'
        )

        self.assertEqual(
            self.atividade.status,
            'Pendente'
        )

        self.assertEqual(
            self.atividade.prioridade,
            'Alta'
        )

        self.assertEqual(
            self.atividade.pontuacao,
            10.0
        )

    def test_representacao_atividade(self):
        """Verifica o método de representação da atividade."""

        self.assertEqual(
            str(self.atividade),
            'Prova de Matemática'
        )

    def test_alterar_titulo_atividade(self):
        """Verifica se o título pode ser atualizado."""

        self.atividade.titulo = 'Trabalho de Matemática'
        self.atividade.save()

        self.atividade.refresh_from_db()

        self.assertEqual(
            self.atividade.titulo,
            'Trabalho de Matemática'
        )

    def test_alterar_status_atividade(self):
        """Verifica a atualização do status."""

        self.atividade.status = 'Concluída'
        self.atividade.save()

        self.atividade.refresh_from_db()

        self.assertEqual(
            self.atividade.status,
            'Concluída'
        )

    def test_alterar_prioridade_atividade(self):
        """Verifica a atualização da prioridade."""

        self.atividade.prioridade = 'Baixa'
        self.atividade.save()

        self.atividade.refresh_from_db()

        self.assertEqual(
            self.atividade.prioridade,
            'Baixa'
        )

    def test_alterar_pontuacao(self):
        """Verifica a atualização da pontuação."""

        self.atividade.pontuacao = 8.5
        self.atividade.save()

        self.atividade.refresh_from_db()

        self.assertEqual(
            self.atividade.pontuacao,
            8.5
        )

    def test_consultar_atividade_por_titulo(self):
        """Verifica a consulta de atividade pelo título."""

        resultado = Atividade.objects.get(
            titulo='Prova de Matemática'
        )

        self.assertEqual(
            resultado.id,
            self.atividade.id
        )

    def test_excluir_atividade(self):
        """Verifica a exclusão de uma atividade."""

        identificador = self.atividade.id

        self.atividade.delete()

        self.assertFalse(
            Atividade.objects.filter(
                id=identificador
            ).exists()
        )

    def test_criar_varias_atividades(self):
        """Verifica o cadastro de várias atividades."""

        Atividade.objects.create(
            titulo='Trabalho de História',
            data=date(2026, 12, 15),
            detalhamento_atividade='Pesquisa histórica.',
            status='Pendente',
            prioridade='Média',
            pontuacao=5.0
        )

        self.assertEqual(
            Atividade.objects.count(),
            2
        )

    # ==========================================
    # TESTES DE RELACIONAMENTO
    # ==========================================

    def test_vincular_disciplina_atividade(self):
        """Verifica o vínculo entre atividade e disciplina."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        self.assertEqual(
            vinculo.atividade,
            self.atividade
        )

        self.assertEqual(
            vinculo.disciplina,
            self.disciplina
        )

    def test_atividade_possui_disciplina(self):
        """Verifica o acesso às disciplinas relacionadas."""

        AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        self.assertEqual(
            self.atividade.disciplinas.count(),
            1
        )

    def test_adicionar_varias_disciplinas(self):
        """Verifica uma atividade relacionada a várias disciplinas."""

        outra_disciplina = Disciplina.objects.create(
            nomedisciplina='História',
            estudante=self.estudante
        )

        AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=outra_disciplina
        )

        self.assertEqual(
            self.atividade.disciplinas.count(),
            2
        )

    # ==========================================
    # TESTES DO MODEL INTERDISCIPLINAR
    # ==========================================

    def test_criar_atividade_interdisciplinar(self):
        """Verifica a criação de um vínculo interdisciplinar."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina,
            criterios_de_avaliacao='Participação e pesquisa.',
            orientador='Professor responsável'
        )

        self.assertEqual(
            vinculo.criterios_de_avaliacao,
            'Participação e pesquisa.'
        )

        self.assertEqual(
            vinculo.orientador,
            'Professor responsável'
        )

    def test_representacao_interdisciplinar(self):
        """Verifica o método __str__ do vínculo."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        self.assertEqual(
            str(vinculo),
            'Prova de Matemática - Matemática'
        )

    def test_campos_opcionais_interdisciplinar(self):
        """Verifica os valores padrão dos campos opcionais."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        self.assertEqual(
            vinculo.criterios_de_avaliacao,
            ''
        )

        self.assertEqual(
            vinculo.orientador,
            ''
        )

    def test_excluir_vinculo_interdisciplinar(self):
        """Verifica a exclusão de um vínculo."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        identificador = vinculo.id

        vinculo.delete()

        self.assertFalse(
            AtividadeInterdisciplinar.objects.filter(
                id=identificador
            ).exists()
        )

    def test_excluir_atividade_remove_vinculos(self):
        """Verifica se os vínculos são excluídos com a atividade."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        identificador = vinculo.id

        self.atividade.delete()

        self.assertFalse(
            AtividadeInterdisciplinar.objects.filter(
                id=identificador
            ).exists()
        )

    def test_excluir_disciplina_remove_vinculos(self):
        """Verifica se os vínculos são excluídos com a disciplina."""

        vinculo = AtividadeInterdisciplinar.objects.create(
            atividade=self.atividade,
            disciplina=self.disciplina
        )

        identificador = vinculo.id

        self.disciplina.delete()

        self.assertFalse(
            AtividadeInterdisciplinar.objects.filter(
                id=identificador
            ).exists()
        )
