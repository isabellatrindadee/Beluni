
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .models import Estudante
from .forms import EstudanteForm, PerfilEstudanteForm, CadastroEstudanteForm


def login_estudante(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = authenticate(
            request,
            username=username,
            password=senha
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('listar_atividades')

        return render(request, 'estudante/login.html', {
            'erro': 'Usuário ou senha inválidos.'
        })

    return render(request, 'estudante/login.html')


@login_required
def logout_estudante(request):
    logout(request)
    return redirect('login_estudante')


def criar_estudante(request):
    """
    Cadastro público: qualquer pessoa pode criar uma conta.
    """
    if request.method == 'POST':
        form = CadastroEstudanteForm(request.POST)

        if form.is_valid():
            estudante = form.save(commit=False)
            estudante.set_password(form.cleaned_data['senha'])
            estudante.save()

            messages.success(
                request,
                'Conta criada com sucesso! Agora você pode entrar.'
            )
            return redirect('login_estudante')
    else:
        form = CadastroEstudanteForm()

    return render(request, 'estudante/criar.html', {
        'form': form
    })


@login_required
def listar_estudantes(request):
    estudantes = Estudante.objects.all()
    return render(request, 'estudante/listar.html', {
        'estudantes': estudantes
    })


@login_required
def detalhar_estudante(request, id):
    estudante = get_object_or_404(Estudante, pk=id)
    return render(request, 'estudante/detalhar.html', {
        'estudante': estudante
    })


@login_required
@permission_required('estudante.change_estudante', raise_exception=True)
def editar_estudante(request, id):
    estudante = get_object_or_404(Estudante, pk=id)

    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)

        if form.is_valid():
            estudante = form.save(commit=False)
            senha = form.cleaned_data.get('senha')

            if senha:
                estudante.set_password(senha)

            estudante.save()
            messages.success(request, 'Estudante atualizado com sucesso!')
            return redirect('detalhar_estudante', id=estudante.pk)
    else:
        form = EstudanteForm(instance=estudante)

    return render(request, 'estudante/editar.html', {
        'form': form,
        'estudante': estudante
    })


@login_required
@permission_required('estudante.delete_estudante', raise_exception=True)
def excluir_estudante(request, id):
    estudante = get_object_or_404(Estudante, pk=id)

    if request.method == 'POST':
        estudante.delete()
        messages.success(request, 'Estudante excluído com sucesso!')
        return redirect('listar_estudantes')

    return render(request, 'estudante/excluir.html', {
        'estudante': estudante
    })



@login_required
def meu_perfil(request):
    estudante = Estudante.objects.filter(pk=request.user.pk).first()

    if estudante is None:
        messages.warning(
            request,
            'Seu usuário ainda não possui um perfil de estudante cadastrado.'
        )
        return redirect('criar_estudante')

    return render(request, 'estudante/meu_perfil.html', {
        'estudante': estudante
    })

@login_required
def editar_meu_perfil(request):
    estudante = get_object_or_404(
        Estudante,
        pk=request.user.pk
    )

    if request.method == 'POST':
        form = PerfilEstudanteForm(
            request.POST,
            instance=estudante
        )

        if form.is_valid():
            estudante = form.save(commit=False)
            senha = form.cleaned_data.get('senha')

            if senha:
                estudante.set_password(senha)

            estudante.save()

            if senha:
                update_session_auth_hash(request, estudante)

            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('meu_perfil')
    else:
        form = PerfilEstudanteForm(instance=estudante)

    return render(request, 'estudante/editar_meu_perfil.html', {
        'form': form,
        'estudante': estudante
    })
