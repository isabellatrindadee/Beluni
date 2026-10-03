from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Estudante
from .forms import EstudanteForm


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

        return render(
            request,
            'estudante/login.html',
            {'erro': 'Usuário ou senha inválidos.'}
        )

    return render(request, 'estudante/login.html')


def logout_estudante(request):
    logout(request)
    return redirect('login_estudante')


def criar_estudante(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST)

        if form.is_valid():
            estudante = form.save(commit=False)
            estudante.username = form.cleaned_data['username']

            senha = form.cleaned_data['senha']

            if senha:
                estudante.set_password(senha)

            estudante.save()

            return redirect('login_estudante')
    else:
        form = EstudanteForm()

    return render(
        request,
        'estudante/criar.html',
        {'form': form}
    )


@login_required
def listar_estudantes(request):
    estudantes = Estudante.objects.all()

    return render(
        request,
        'estudante/listar.html',
        {'estudantes': estudantes}
    )


@login_required
def detalhar_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)

    return render(
        request,
        'estudante/detalhar.html',
        {'estudante': estudante}
    )


@login_required
def editar_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)

    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)

        if form.is_valid():
            estudante = form.save(commit=False)
            estudante.username = form.cleaned_data['username']

            senha = form.cleaned_data['senha']

            if senha:
                estudante.set_password(senha)

            estudante.save()

            return redirect('listar_estudantes')
    else:
        form = EstudanteForm(instance=estudante)

    return render(
        request,
        'estudante/editar.html',
        {
            'form': form,
            'estudante': estudante
        }
    )


@login_required
def excluir_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)

    if request.method == 'POST':
        estudante.delete()
        return redirect('listar_estudantes')

    return render(
        request,
        'estudante/excluir.html',
        {'estudante': estudante}
    )