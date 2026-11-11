
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Estudante
from .forms import (
    EstudanteForm,
    PerfilEstudanteForm,
    CadastroEstudanteForm,
)

from disciplinas.models import Disciplina
from atividade.models import Atividade
from meta.models import Meta


# VERIFICAR SE É ADMINISTRADOR
def usuario_e_administrador(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name='Administrador').exists()
        )
    )


# LOGIN
def login_estudante(request):
    if request.user.is_authenticated:
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

            estudante.set_password(
                form.cleaned_data['senha']
            )

            estudante.save()

            grupo = get_object_or_404(
                Group,
                name='estudante'
            )

            estudante.groups.add(grupo)

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


# LISTAR ESTUDANTES E ADMINISTRADORES
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def listar_estudantes(request):

    # Estudantes que não pertencem ao grupo Administrador
    estudantes = Estudante.objects.exclude(
        groups__name='Administrador'
    ).exclude(
        is_superuser=True
    ).distinct().order_by('nome')

    # Administradores, incluindo superusuários
    usuarios_admin = User.objects.filter(
        Q(groups__name='Administrador') | Q(is_superuser=True)
    ).distinct().order_by('username')

    # Recuperar os perfis associados aos administradores,
    # caso existam
    perfis_admin = {
        estudante.pk: estudante
        for estudante in Estudante.objects.filter(
            pk__in=usuarios_admin.values_list('pk', flat=True)
        )
    }

    administradores = []

    for usuario in usuarios_admin:
        perfil = perfis_admin.get(usuario.pk)

        administradores.append({
            'usuario': usuario,
            'nome': (
                perfil.nome
                if perfil
                else usuario.get_full_name() or usuario.username
            ),
            'cpf': perfil.cpf if perfil else '',
            'possui_perfil': perfil is not None,
        })

    return render(request, 'estudante/listar.html', {
        'estudantes': estudantes,
        'administradores': administradores,
        'total_estudantes': estudantes.count(),
        'total_administradores': len(administradores),
    })


# DETALHAR ESTUDANTE
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def detalhar_estudante(request, id):

    estudante = get_object_or_404(
        Estudante.objects.exclude(groups__name='Administrador'),
        pk=id
    )

    return render(request, 'estudante/detalhar.html', {
        'estudante': estudante
    })


# EDITAR ESTUDANTE
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def editar_estudante(request, id):

    estudante = get_object_or_404(
        Estudante.objects.exclude(groups__name='Administrador'),
        pk=id
    )

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


# EXCLUIR ESTUDANTE
@login_required
@user_passes_test(
    usuario_e_administrador,
    login_url='login_estudante'
)
def excluir_estudante(request, id):

    estudante = get_object_or_404(
        Estudante.objects.exclude(groups__name='Administrador'),
        pk=id
    )

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

    eh_admin = usuario_e_administrador(request.user)

    return render(request, 'estudante/meu_perfil.html', {
        'estudante': estudante,
        'eh_administrador': eh_admin,
        'url_retorno': 'inicio' if eh_admin else 'listar_atividades',
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
                update_session_auth_hash(
                    request,
                    estudante
                )

            messages.success(
                request,
                'Seu perfil foi atualizado com sucesso!'
            )

            return redirect('meu_perfil')

    else:
        form = PerfilEstudanteForm(instance=estudante)

    eh_admin = usuario_e_administrador(request.user)

    return render(request, 'estudante/editar_meu_perfil.html', {
        'form': form,
        'estudante': estudante,
        'url_retorno': 'inicio' if eh_admin else 'listar_atividades',
    })


# DASHBOARD
@login_required
def inicio(request):

    # ==========================================
    # PAINEL ADMINISTRATIVO
    # ==========================================
    if usuario_e_administrador(request.user):

        # Buscar estudantes, excluindo administradores
        estudantes_recentes = Estudante.objects.exclude(
            groups__name='Administrador'
        ).exclude(
            is_superuser=True
        ).distinct().order_by('-date_joined')[:8]

        # Buscar todos os administradores
        administradores = User.objects.filter(
            Q(groups__name='Administrador') | Q(is_superuser=True)
        ).distinct().order_by('username')

        # Administradores mais recentes
        administradores_recentes = administradores.order_by(
            '-date_joined'
        )[:8]

        # Totais
        total_estudantes = Estudante.objects.exclude(
            groups__name='Administrador'
        ).exclude(
            is_superuser=True
        ).distinct().count()

        total_administradores = administradores.count()

        contexto = {
            'total_estudantes': total_estudantes,
            'total_administradores': total_administradores,
            'total_disciplinas': Disciplina.objects.count(),
            'total_atividades': Atividade.objects.count(),
            'total_metas': Meta.objects.count(),

            'estudantes_recentes': estudantes_recentes,
            'administradores': administradores,
            'administradores_recentes': administradores_recentes,
        }

        return render(
            request,
            'estudante/dashboard_admin.html',
            contexto
        )

    # ==========================================
    # PAINEL DO ESTUDANTE
    # ==========================================

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


# TORNAR ESTUDANTE ADMINISTRADOR
@login_required
@user_passes_test(usuario_e_administrador)
@permission_required('estudante.change_estudante', raise_exception=True)
@require_POST
def tornar_administrador(request, id):

    estudante = get_object_or_404(
        Estudante.objects.exclude(groups__name='Administrador'),
        pk=id
    )

    grupo_administrador = get_object_or_404(
        Group,
        name='Administrador'
    )

    grupo_estudante = get_object_or_404(
        Group,
        name='estudante'
    )

    estudante.groups.remove(grupo_estudante)
    estudante.groups.add(grupo_administrador)

    messages.success(
        request,
        f'{estudante.username} agora é administrador!'
    )

    return redirect('listar_estudantes')


# TORNAR ADMINISTRADOR EM ESTUDANTE
@login_required
@user_passes_test(usuario_e_administrador)
@permission_required('estudante.change_estudante', raise_exception=True)
@require_POST
def tornar_estudante(request, id):

    estudante = get_object_or_404(
        Estudante,
        pk=id
    )

    if estudante.pk == request.user.pk:
        messages.error(
            request,
            'Você não pode retirar seu próprio acesso de administrador.'
        )
        return redirect('listar_estudantes')

    grupo_estudante = get_object_or_404(
        Group,
        name='estudante'
    )

    grupo_administrador = get_object_or_404(
        Group,
        name='Administrador'
    )

    if not estudante.groups.filter(
        pk=grupo_administrador.pk
    ).exists():
        messages.info(
            request,
            'Este usuário não pertence ao grupo Administrador.'
        )
        return redirect('listar_estudantes')

    estudante.groups.remove(grupo_administrador)
    estudante.groups.add(grupo_estudante)

    messages.success(
        request,
        f'{estudante.username} agora pertence ao grupo estudante!'
    )

    return redirect('listar_estudantes')


# EXCLUIR MEU PERFIL
@login_required
@require_POST
def excluir_meu_perfil(request):

    senha = request.POST.get('senha_exclusao')

    if not senha or not request.user.check_password(senha):
        messages.error(
            request,
            'Senha incorreta. Sua conta não foi excluída.'
        )
        return redirect('meu_perfil')

    usuario = request.user

    usuario.delete()

    logout(request)

    messages.success(
        request,
        'Sua conta foi excluída com sucesso.'
    )

    return redirect('index')
