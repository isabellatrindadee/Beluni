
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Disciplina
from .forms import DisciplinaForm
from estudante.models import Estudante


def obter_estudante(usuario):
    return get_object_or_404(
        Estudante,
        pk=usuario.pk
    )


@login_required
@permission_required('disciplinas.view_disciplina')
def listar_disciplinas(request):
    estudante = obter_estudante(request.user)

    disciplinas = Disciplina.objects.filter(
        estudante=estudante
    )

    return render(
        request,
        'disciplinas/listar.html',
        {'disciplinas': disciplinas}
    )


@login_required
@permission_required('disciplinas.add_disciplina')
def criar_disciplina(request):
    estudante = obter_estudante(request.user)

    if request.method == 'POST':
        form = DisciplinaForm(request.POST)

        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.estudante = estudante
            disciplina.save()

            return redirect('listar_disciplinas')
    else:
        form = DisciplinaForm()

    # Se o formulário tiver um campo estudante, não permita
    # que ele apresente ou aceite estudantes de outras contas.
    if 'estudante' in form.fields:
        form.fields['estudante'].queryset = Estudante.objects.filter(
            pk=estudante.pk
        )
        form.fields['estudante'].widget = form.fields[
            'estudante'
        ].hidden_widget()

    return render(
        request,
        'disciplinas/criar.html',
        {'form': form}
    )


@login_required
@permission_required('disciplinas.view_disciplina')
def detalhar_disciplina(request, id):
    estudante = obter_estudante(request.user)

    disciplina = get_object_or_404(
        Disciplina.objects.filter(
            estudante=estudante
        ).prefetch_related('atividades'),
        id=id
    )

    atividades = disciplina.atividades.filter(
        disciplinas__estudante=estudante
    ).distinct().order_by('data')

    return render(
        request,
        'disciplinas/detalhar.html',
        {
            'disciplina': disciplina,
            'atividades': atividades,
        }
    )


@login_required
@permission_required('disciplinas.change_disciplina')
def editar_disciplina(request, id):
    estudante = obter_estudante(request.user)

    disciplina = get_object_or_404(
        Disciplina,
        id=id,
        estudante=estudante
    )

    if request.method == 'POST':
        form = DisciplinaForm(
            request.POST,
            instance=disciplina
        )

        if form.is_valid():
            disciplina_editada = form.save(commit=False)

            # Impede que o proprietário seja alterado pelo formulário.
            disciplina_editada.estudante = estudante
            disciplina_editada.save()

            return redirect('listar_disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)

    if 'estudante' in form.fields:
        form.fields['estudante'].queryset = Estudante.objects.filter(
            pk=estudante.pk
        )
        form.fields['estudante'].widget = form.fields[
            'estudante'
        ].hidden_widget()

    return render(
        request,
        'disciplinas/editar.html',
        {
            'form': form,
            'disciplina': disciplina
        }
    )


@login_required
@permission_required('disciplinas.delete_disciplina')
def excluir_disciplina(request, id):
    estudante = obter_estudante(request.user)

    disciplina = get_object_or_404(
        Disciplina,
        id=id,
        estudante=estudante
    )

    if request.method == 'POST':
        disciplina.delete()
        return redirect('listar_disciplinas')

    return render(
        request,
        'disciplinas/excluir.html',
        {'disciplina': disciplina}
    )
