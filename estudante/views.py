
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Estudante
from .forms import (
    EstudanteForm,
    PerfilEstudanteForm,
    CadastroEstudanteForm,
)

from disciplinas.models import Disciplina
from atividade.models import Atividade
from meta.models import Meta


def usuario_e_administrador(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name='administrador').exists()
        )
    )


# LOGIN
def login_estudante(request):
    if request.user.is_authenticated:
        request.session['is_admin'] = usuario_e_administrador(request.user)
        return redirect('inicio')

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

            request.session['is_admin'] = usuario_e_administrador(usuario)

            return redirect('inicio')

        return render(request, 'estudante/login.html', {
            'erro': 'Usuário ou senha inválidos.'
        })

    return render(request, 'estudante/login.html')


# LOGOUT
@login_required
def logout_estudante(request):
    logout(request)
    return redirect('login_estudante')


# CADASTRO DE ESTUDANTE
def criar_estudante(request):
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


# LISTAGEM DE ESTUDANTES — SOMENTE ADMINISTRADORES
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def listar_estudantes(request):
    estudantes = Estudante.objects.all()

    return render(request, 'estudante/listar.html', {
        'estudantes': estudantes
    })


# DETALHES DE UM ESTUDANTE — SOMENTE ADMINISTRADORES
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def detalhar_estudante(request, id):
    estudante = get_object_or_404(Estudante, pk=id)

    return render(request, 'estudante/detalhar.html', {
        'estudante': estudante
    })


# EDITAR ESTUDANTE — SOMENTE ADMINISTRADORES
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def editar_estudante(request, id):
    estudante = get_object_or_404(Estudante, pk=id)

    if request.method == 'POST':
        form = EstudanteForm(
            request.POST,
            instance=estudante
        )

        if form.is_valid():
            estudante = form.save(commit=False)
            senha = form.cleaned_data.get('senha')

            if senha:
                estudante.set_password(senha)

            estudante.save()

            messages.success(
                request,
                'Estudante atualizado com sucesso!'
            )

            return redirect(
                'detalhar_estudante',
                id=estudante.pk
            )

    else:
        form = EstudanteForm(instance=estudante)

    return render(request, 'estudante/editar.html', {
        'form': form,
        'estudante': estudante
    })


# EXCLUIR ESTUDANTE — SOMENTE ADMINISTRADORES
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def excluir_estudante(request, id):
    estudante = get_object_or_404(Estudante, pk=id)

    if request.method == 'POST':
        estudante.delete()

        messages.success(
            request,
            'Estudante excluído com sucesso!'
        )

        return redirect('listar_estudantes')

    return render(request, 'estudante/excluir.html', {
        'estudante': estudante
    })


# MEU PERFIL
@login_required
def meu_perfil(request):
    estudante = Estudante.objects.filter(
        pk=request.user.pk
    ).first()

    if estudante is None:
        messages.warning(
            request,
            'Seu usuário ainda não possui um perfil de estudante cadastrado.'
        )
        return redirect('inicio')

    return render(request, 'estudante/meu_perfil.html', {
        'estudante': estudante
    })


# EDITAR MEU PERFIL
@login_required
def editar_meu_perfil(request):
    estudante = Estudante.objects.filter(
        pk=request.user.pk
    ).first()

    if estudante is None:
        messages.warning(
            request,
            'Seu usuário ainda não possui um perfil de estudante cadastrado.'
        )
        return redirect('inicio')

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

            messages.success(
                request,
                'Seu perfil foi atualizado com sucesso!'
            )

            return redirect('meu_perfil')

    else:
        form = PerfilEstudanteForm(instance=estudante)

    return render(request, 'estudante/editar_meu_perfil.html', {
        'form': form,
        'estudante': estudante
    })


# PAINEL INICIAL — ADMINISTRADOR E ESTUDANTE
@login_required
def inicio(request):

    # Atualiza a identificação na sessão
    administrador = usuario_e_administrador(request.user)
    request.session['is_admin'] = administrador

    # PAINEL DO ADMINISTRADOR
    if administrador:

        estudantes_recentes = Estudante.objects.order_by(
            '-date_joined'
        )[:8]

        contexto = {
            'total_estudantes': Estudante.objects.count(),
            'total_disciplinas': Disciplina.objects.count(),
            'total_atividades': Atividade.objects.count(),
            'total_metas': Meta.objects.count(),
            'estudantes_recentes': estudantes_recentes,
        }

        return render(
            request,
            'estudante/dashboard_admin.html',
            contexto
        )

    # PAINEL DO ESTUDANTE
    estudante = Estudante.objects.filter(
        pk=request.user.pk
    ).first()

    if estudante:
        disciplinas = Disciplina.objects.filter(
            estudante=estudante
        ).order_by('nomedisciplina')

        atividades = Atividade.objects.filter(
            disciplinas__estudante=estudante
        ).distinct().order_by('data')

        metas = Meta.objects.filter(
            estudante=estudante
        ).order_by('data')

    else:
        disciplinas = Disciplina.objects.none()
        atividades = Atividade.objects.none()
        metas = Meta.objects.none()

    contexto = {
        'disciplinas': disciplinas,
        'atividades': atividades,
        'metas': metas,
        'total_disciplinas': disciplinas.count(),
        'total_atividades': atividades.count(),
        'total_metas': metas.count(),
    }

    return render(request, 'inicio.html', contexto)

# PÁGINA PÚBLICA
def index(request):
    return render(request, 'index.html')
