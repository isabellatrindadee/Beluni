
from datetime import date

from django.test import TestCase

from estudante.models import Estudante
from disciplinas.models import Disciplina
from atividade.models import Atividade

from .models import Notificacao


class TestesNotificacao(TestCase):
    """
    Testes automatizados do aplicativo de notificações.
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes.
        """

        self.estudante = Estudante.objects.create_user(
            username='estudante_notificacao',
            email='notificacao@teste.com',
            password='Senha123456'
        )

        self.disciplina = Disciplina.objects.create(
            nomedisciplina='Matemática',
            estudante=self.estudante
        )

        self.atividade = Atividade.objects.create(
            titulo='Prova de Matemática',
            data=date(2026, 12, 10),
            detalhamento_atividade='Avaliação de matemática.',
            status='Pendente',
            prioridade='Alta',
            pontuacao=10.0
        )

        self.notificacao = Notificacao.objects.create(
            mensagem='Você possui uma nova atividade.',
            estudante=self.estudante,
            atividade=self.atividade
        )

    # ==========================================
    # TESTES DE CRIACAO
    # ==========================================

    def test_criar_notificacao(self):
        """Verifica a criação de uma notificação."""

        self.assertEqual(
            self.notificacao.mensagem,
            'Você possui uma nova atividade.'
        )

        self.assertEqual(
            self.notificacao.estudante,
            self.estudante
        )

    def test_notificacao_inicia_como_nao_lida(self):
        """Verifica o valor padrão do campo lida."""

        self.assertFalse(
            self.notificacao.lida
        )

    def test_criar_notificacao_sem_atividade(self):
        """Verifica a criação sem uma atividade relacionada."""

        notificacao = Notificacao.objects.create(
            mensagem='Lembrete de estudos.',
            estudante=self.estudante
        )

        self.assertIsNone(
            notificacao.atividade
        )

    def test_criar_notificacao_com_atividade(self):
        """Verifica o vínculo com uma atividade."""

        self.assertEqual(
            self.notificacao.atividade,
            self.atividade
        )

    # ==========================================
    # TESTES DE REPRESENTACAO
    # ==========================================

    def test_representacao_notificacao(self):
        """Verifica o método __str__."""

        self.assertEqual(
            str(self.notificacao),
            'Você possui uma nova atividade.'
        )

    # ==========================================
    # TESTES DE ATUALIZACAO
    # ==========================================

    def test_alterar_mensagem(self):
        """Verifica a atualização da mensagem."""

        self.notificacao.mensagem = 'Atividade atualizada.'
        self.notificacao.save()

        self.notificacao.refresh_from_db()

        self.assertEqual(
            self.notificacao.mensagem,
            'Atividade atualizada.'
        )

    def test_marcar_notificacao_como_lida(self):
        """Verifica se a notificação pode ser marcada como lida."""

        self.notificacao.lida = True
        self.notificacao.save()

        self.notificacao.refresh_from_db()

        self.assertTrue(
            self.notificacao.lida
        )

    def test_marcar_notificacao_como_nao_lida(self):
        """Verifica se a notificação pode voltar a ficar não lida."""

        self.notificacao.lida = True
        self.notificacao.save()

        self.notificacao.lida = False
        self.notificacao.save()

        self.notificacao.refresh_from_db()

        self.assertFalse(
            self.notificacao.lida
        )

    # ==========================================
    # TESTES DE CONSULTA
    # ==========================================

    def test_consultar_notificacao_por_mensagem(self):
        """Verifica a consulta pelo conteúdo da mensagem."""

        resultado = Notificacao.objects.get(
            mensagem='Você possui uma nova atividade.'
        )

        self.assertEqual(
            resultado.id,
            self.notificacao.id
        )

    def test_listar_notificacoes_do_estudante(self):
        """Verifica o relacionamento com o estudante."""

        self.assertEqual(
            self.estudante.notificacoes.count(),
            1
        )

    def test_filtrar_notificacoes_lidas(self):
        """Verifica a consulta de notificações lidas."""

        self.notificacao.lida = True
        self.notificacao.save()

        notificacoes_lidas = Notificacao.objects.filter(
            lida=True
        )

        self.assertEqual(
            notificacoes_lidas.count(),
            1
        )

    def test_filtrar_notificacoes_nao_lidas(self):
        """Verifica a consulta de notificações não lidas."""

        notificacoes_nao_lidas = Notificacao.objects.filter(
            lida=False
        )

        self.assertEqual(
            notificacoes_nao_lidas.count(),
            1
        )

    def test_listar_notificacoes_de_uma_atividade(self):
        """Verifica o relacionamento com a atividade."""

        self.assertEqual(
            self.atividade.notificacoes.count(),
            1
        )

    # ==========================================
    # TESTES DE EXCLUSAO
    # ==========================================

    def test_excluir_notificacao(self):
        """Verifica a exclusão de uma notificação."""

        identificador = self.notificacao.id

        self.notificacao.delete()

        self.assertFalse(
            Notificacao.objects.filter(
                id=identificador
            ).exists()
        )

    def test_excluir_estudante_remove_notificacoes(self):
        """Verifica se as notificações são excluídas com o estudante."""

        identificador = self.notificacao.id

        self.estudante.delete()

        self.assertFalse(
            Notificacao.objects.filter(
                id=identificador
            ).exists()
        )

    def test_excluir_atividade_remove_notificacoes(self):
        """Verifica se as notificações relacionadas são excluídas."""

        identificador = self.notificacao.id

        self.atividade.delete()

        self.assertFalse(
            Notificacao.objects.filter(
                id=identificador
            ).exists()
        )

    # ==========================================
    # TESTES DE ISOLAMENTO
    # ==========================================

    def test_estudantes_possuem_notificacoes_independentes(self):
        """Verifica a separação das notificações por estudante."""

        outro_estudante = Estudante.objects.create_user(
            username='outro_estudante_notificacao',
            email='outro@teste.com',
            password='Senha123456'
        )

        Notificacao.objects.create(
            mensagem='Nova notificação para outro estudante.',
            estudante=outro_estudante
        )

        self.assertEqual(
            self.estudante.notificacoes.count(),
            1
        )

        self.assertEqual(
            outro_estudante.notificacoes.count(),
            1
        )

    def test_contagem_de_notificacoes(self):
        """Verifica a quantidade de notificações cadastradas."""

        Notificacao.objects.create(
            mensagem='Segunda notificação.',
            estudante=self.estudante
        )

        self.assertEqual(
            Notificacao.objects.count(),
            2
        )