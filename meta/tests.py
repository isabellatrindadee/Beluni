
from datetime import date

from django.test import TestCase

from estudante.models import Estudante
from .models import Meta


class TestesMeta(TestCase):
    """
    Testes automatizados do aplicativo de metas.
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes.
        """

        self.estudante = Estudante.objects.create_user(
            username='estudante_meta',
            email='meta@teste.com',
            password='Senha123456'
        )

        self.meta = Meta.objects.create(
            titulo='Estudar para a prova',
            detalhamento='Revisar os conteúdos de matemática.',
            data=date(2026, 12, 20),
            estudante=self.estudante
        )

    # ==========================================
    # TESTES DE CRIACAO
    # ==========================================

    def test_criar_meta(self):
        """Verifica a criação de uma meta."""

        self.assertEqual(
            self.meta.titulo,
            'Estudar para a prova'
        )

        self.assertEqual(
            self.meta.detalhamento,
            'Revisar os conteúdos de matemática.'
        )

        self.assertEqual(
            self.meta.data,
            date(2026, 12, 20)
        )

    def test_meta_inicia_como_nao_concluida(self):
        """Verifica o valor padrão do campo concluida."""

        self.assertFalse(
            self.meta.concluida
        )

    def test_meta_pertence_ao_estudante(self):
        """Verifica o relacionamento com o estudante."""

        self.assertEqual(
            self.meta.estudante,
            self.estudante
        )

    # ==========================================
    # TESTES DE REPRESENTACAO
    # ==========================================

    def test_representacao_meta(self):
        """Verifica o método __str__ da meta."""

        self.assertEqual(
            str(self.meta),
            'Estudar para a prova'
        )

    # ==========================================
    # TESTES DE ATUALIZACAO
    # ==========================================

    def test_alterar_titulo(self):
        """Verifica a alteração do título da meta."""

        self.meta.titulo = 'Estudar para o vestibular'
        self.meta.save()

        self.meta.refresh_from_db()

        self.assertEqual(
            self.meta.titulo,
            'Estudar para o vestibular'
        )

    def test_alterar_detalhamento(self):
        """Verifica a alteração do detalhamento."""

        self.meta.detalhamento = 'Revisar todas as matérias.'
        self.meta.save()

        self.meta.refresh_from_db()

        self.assertEqual(
            self.meta.detalhamento,
            'Revisar todas as matérias.'
        )

    def test_alterar_data(self):
        """Verifica a atualização da data da meta."""

        self.meta.data = date(2027, 1, 15)
        self.meta.save()

        self.meta.refresh_from_db()

        self.assertEqual(
            self.meta.data,
            date(2027, 1, 15)
        )

    def test_marcar_meta_como_concluida(self):
        """Verifica se uma meta pode ser marcada como concluída."""

        self.meta.concluida = True
        self.meta.save()

        self.meta.refresh_from_db()

        self.assertTrue(
            self.meta.concluida
        )

    def test_marcar_meta_como_nao_concluida(self):
        """Verifica se uma meta pode voltar a ficar pendente."""

        self.meta.concluida = True
        self.meta.save()

        self.meta.concluida = False
        self.meta.save()

        self.meta.refresh_from_db()

        self.assertFalse(
            self.meta.concluida
        )

    # ==========================================
    # TESTES DE CONSULTA
    # ==========================================

    def test_consultar_meta_por_titulo(self):
        """Verifica a consulta de uma meta pelo título."""

        resultado = Meta.objects.get(
            titulo='Estudar para a prova'
        )

        self.assertEqual(
            resultado.id,
            self.meta.id
        )

    def test_listar_metas_do_estudante(self):
        """Verifica a listagem pelo relacionamento metas."""

        self.assertEqual(
            self.estudante.metas.count(),
            1
        )

    def test_contar_metas(self):
        """Verifica a quantidade de metas cadastradas."""

        Meta.objects.create(
            titulo='Ler um livro',
            detalhamento='Ler 20 páginas por dia.',
            data=date(2026, 12, 25),
            estudante=self.estudante
        )

        self.assertEqual(
            Meta.objects.count(),
            2
        )

    def test_filtrar_metas_concluidas(self):
        """Verifica a consulta de metas concluídas."""

        self.meta.concluida = True
        self.meta.save()

        metas_concluidas = Meta.objects.filter(
            concluida=True
        )

        self.assertEqual(
            metas_concluidas.count(),
            1
        )

    def test_filtrar_metas_pendentes(self):
        """Verifica a consulta de metas pendentes."""

        metas_pendentes = Meta.objects.filter(
            concluida=False
        )

        self.assertEqual(
            metas_pendentes.count(),
            1
        )

    # ==========================================
    # TESTES DE EXCLUSAO
    # ==========================================

    def test_excluir_meta(self):
        """Verifica a exclusão de uma meta."""

        identificador = self.meta.id

        self.meta.delete()

        self.assertFalse(
            Meta.objects.filter(
                id=identificador
            ).exists()
        )

    def test_excluir_estudante_remove_metas(self):
        """Verifica a exclusão das metas junto ao estudante."""

        identificador = self.meta.id

        self.estudante.delete()

        self.assertFalse(
            Meta.objects.filter(
                id=identificador
            ).exists()
        )

    # ==========================================
    # TESTES DE ISOLAMENTO
    # ==========================================

    def test_estudantes_possuem_metas_independentes(self):
        """Verifica a separação das metas por estudante."""

        outro_estudante = Estudante.objects.create_user(
            username='outro_estudante_meta',
            email='outro_meta@teste.com',
            password='Senha123456'
        )

        Meta.objects.create(
            titulo='Aprender inglês',
            detalhamento='Estudar vocabulário.',
            data=date(2026, 12, 30),
            estudante=outro_estudante
        )

        self.assertEqual(
            self.estudante.metas.count(),
            1
        )

        self.assertEqual(
            outro_estudante.metas.count(),
            1
        )

    def test_meta_de_outro_estudante(self):
        """Verifica a identificação do responsável pela meta."""

        outro_estudante = Estudante.objects.create_user(
            username='segundo_estudante_meta',
            email='segundo@teste.com',
            password='Senha123456'
        )

        outra_meta = Meta.objects.create(
            titulo='Organizar rotina',
            detalhamento='Planejar horários de estudo.',
            data=date(2027, 1, 5),
            estudante=outro_estudante
        )

        self.assertNotEqual(
            self.meta.estudante,
            outra_meta.estudante
        )

