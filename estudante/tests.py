
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from .models import Estudante


class TestesEstudante(TestCase):
    """
    Testes automatizados das funcionalidades do aplicativo estudante.
    """

    def setUp(self):
        """
        Prepara os usuários e grupos necessários para os testes.
        """

        # Criar os grupos do sistema
        self.grupo_estudante, _ = Group.objects.get_or_create(
            name='estudante'
        )

        self.grupo_administrador, _ = Group.objects.get_or_create(
            name='Administrador'
        )

        # Criar um administrador para os testes
        self.administrador = User.objects.create_user(
            username='administrador_teste',
            email='admin@teste.com',
            password='SenhaAdmin123'
        )

        self.administrador.groups.add(
            self.grupo_administrador
        )

        # Criar um estudante para os testes
        self.estudante = Estudante(
            username='estudante_teste',
            email='estudante@teste.com',
            nome='Estudante de Teste',
            cpf='12345678900'
        )

        self.estudante.set_password('SenhaEstudante123')
        self.estudante.save()

        self.estudante.groups.add(
            self.grupo_estudante
        )

    # ==========================================
    # TESTES DE ACESSO
    # ==========================================

    def test_pagina_inicial_publica(self):
        """
        Verifica se a página pública pode ser acessada.
        """

        resposta = self.client.get(
            reverse('index')
        )

        self.assertEqual(resposta.status_code, 200)

    def test_pagina_de_login(self):
        """
        Verifica se a página de login está disponível.
        """

        resposta = self.client.get(
            reverse('login_estudante')
        )

        self.assertEqual(resposta.status_code, 200)

    # ==========================================
    # TESTES DE AUTENTICACAO
    # ==========================================

    def test_login_com_dados_corretos(self):
        """
        Verifica se um usuário consegue entrar com
        suas credenciais corretas.
        """

        resposta = self.client.post(
            reverse('login_estudante'),
            {
                'username': 'estudante_teste',
                'senha': 'SenhaEstudante123'
            }
        )

        self.assertRedirects(
            resposta,
            reverse('inicio')
        )

        self.assertTrue(
            resposta.wsgi_request.user.is_authenticated
        )

    def test_login_com_senha_incorreta(self):
        """
        Verifica se o sistema impede o acesso
        quando a senha está incorreta.
        """

        resposta = self.client.post(
            reverse('login_estudante'),
            {
                'username': 'estudante_teste',
                'senha': 'senha_errada'
            }
        )

        self.assertEqual(
            resposta.status_code,
            200
        )

        self.assertContains(
            resposta,
            'Usuário ou senha inválidos.'
        )

    # ==========================================
    # TESTES DE CADASTRO
    # ==========================================

    def test_cadastro_de_novo_estudante(self):
        """
        Verifica se um novo estudante pode ser cadastrado.
        """

        resposta = self.client.post(
            reverse('criar_estudante'),
            {
                'nome': 'Novo Estudante',
                'username': 'novo_estudante',
                'email': 'novo@teste.com',
                'cpf': '98765432100',
                'senha': 'SenhaNova123',
                'confirmar_senha': 'SenhaNova123'
            }
        )

        self.assertRedirects(
            resposta,
            reverse('login_estudante')
        )

        novo_estudante = Estudante.objects.get(
            username='novo_estudante'
        )

        self.assertTrue(
            novo_estudante.check_password('SenhaNova123')
        )

        self.assertTrue(
            novo_estudante.groups.filter(
                name='estudante'
            ).exists()
        )

    # ==========================================
    # TESTES DE PERMISSOES
    # ==========================================

    def test_administrador_acessa_gerenciamento(self):
        """
        Verifica se o administrador consegue acessar
        a listagem de usuários.
        """

        self.client.force_login(
            self.administrador
        )

        resposta = self.client.get(
            reverse('listar_estudantes')
        )

        self.assertEqual(
            resposta.status_code,
            200
        )

    def test_estudante_nao_acessa_gerenciamento(self):
        """
        Verifica se um estudante comum é impedido
        de acessar a área administrativa.
        """

        self.client.force_login(
            self.estudante
        )

        resposta = self.client.get(
            reverse('listar_estudantes')
        )

        self.assertEqual(
            resposta.status_code,
            302
        )

    # ==========================================
    # TESTES DO DASHBOARD
    # ==========================================

    def test_administrador_acessa_dashboard(self):
        """
        Verifica se o dashboard administrativo
        é exibido corretamente.
        """

        self.client.force_login(
            self.administrador
        )

        resposta = self.client.get(
            reverse('inicio')
        )

        self.assertEqual(
            resposta.status_code,
            200
        )

        self.assertTemplateUsed(
            resposta,
            'estudante/dashboard_admin.html'
        )

        self.assertIn(
            'total_estudantes',
            resposta.context
        )

        self.assertIn(
            'total_administradores',
            resposta.context
        )

    def test_estudante_acessa_dashboard_proprio(self):
        """
        Verifica se o estudante consegue acessar
        seu próprio painel.
        """

        self.client.force_login(
            self.estudante
        )

        resposta = self.client.get(
            reverse('inicio')
        )

        self.assertEqual(
            resposta.status_code,
            200
        )

        self.assertTemplateUsed(
            resposta,
            'inicio.html'
        )
