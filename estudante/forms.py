from django import forms
from django.contrib.auth.models import User
from .models import Estudante


class EstudanteForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuário',
        max_length=150
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Estudante
        fields = ['username', 'senha', 'cpf', 'nome']

        labels = {
            'username': 'Usuário',
            'cpf': 'CPF',
            'nome': 'Nome',
        }


class PerfilEstudanteForm(forms.ModelForm):
    senha = forms.CharField(
        label='Nova senha (opcional)',
        widget=forms.PasswordInput,
        required=False,
        help_text='Deixe em branco para manter sua senha atual.'
    )

    class Meta:
        model = Estudante
        fields = ['nome', 'username', 'email', 'cpf']

        labels = {
            'nome': 'Nome completo',
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'cpf': 'CPF',
        }

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CadastroEstudanteForm(forms.ModelForm):
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Crie uma senha',
            'autocomplete': 'new-password',
        })
    )

    confirmar_senha = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha novamente',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = Estudante
        fields = ['nome', 'username', 'email', 'cpf']

        labels = {
            'nome': 'Nome completo',
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'cpf': 'CPF',
        }

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo',
                'autocomplete': 'name',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escolha um nome de usuário',
                'autocomplete': 'username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu e-mail',
                'autocomplete': 'email',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu CPF',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'Este nome de usuário já está em uso.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado.'
            )

        return email

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf'].strip()

        if Estudante.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError(
                'Este CPF já está cadastrado.'
            )

        return cpf

    def clean(self):
        dados = super().clean()
        senha = dados.get('senha')
        confirmar_senha = dados.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error(
                'confirmar_senha',
                'As senhas não são iguais.'
            )

        return dados
